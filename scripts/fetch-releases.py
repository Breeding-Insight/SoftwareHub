#!/usr/bin/env python3
"""Generate the news/ listing entries from GitHub Releases and NEWS.md.

GitHub Releases drive the feed: they carry the publication date the Quarto
listing sorts on, they cover the Shiny apps that ship no NEWS.md, and they never
expose an unreleased development section the way the top of a NEWS.md can.

The notes themselves prefer the matching NEWS.md section, because a hand-written
changelog entry reads far better than GitHub's auto-generated "What's Changed"
dump of pull request titles — and several releases here have an empty body but a
good NEWS.md entry. The release body is the fallback.

A version with a NEWS.md entry but no release cannot be dated, so it is skipped
and reported. Cutting a release for it on GitHub is the fix.

Everything in news/ is generated. Do not hand-edit it; edit the release notes or
NEWS.md upstream and re-run this script.

Usage:  python3 scripts/fetch-releases.py
Set GITHUB_TOKEN to lift the unauthenticated API rate limit.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG = "Breeding-Insight"

# repo -> (software page slug, logo asset). The slug doubles as the news
# filename prefix and the link back into the software catalog.
PACKAGES = {
    "BIGr": ("bigr", "software-bigr.png"),
    "BIGapp": ("bigapp", "software-bigapp.png"),
    "BIGpopA": ("bigpopa", "software-bigpopa.png"),
    "Familia": ("familia", "software-familia.png"),
    "AlloMate": ("allomate", "software-allomate.png"),
    "Qploidy2": ("qploidy2", "software-qploidy2.png"),
}

ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = ROOT / "news"


def fetch_releases(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/releases?per_page=100"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "SoftwareHub-news-generator",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_news_sections(repo):
    """Map version -> notes, parsed from the repo's NEWS.md if it has one.

    Sections are the R convention: `# <Package> <version>`, running until the
    next level-one heading.
    """
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/main/NEWS.md"
    request = urllib.request.Request(
        url, headers={"User-Agent": "SoftwareHub-news-generator"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return {}
        raise

    sections = {}
    version = None
    buffer = []
    for line in text.replace("\r\n", "\n").split("\n"):
        heading = re.match(r"^#\s+\S+\s+v?([0-9][0-9A-Za-z.\-]*)\s*$", line)
        if heading:
            if version:
                sections[version] = "\n".join(buffer).strip()
            version = heading.group(1)
            buffer = []
            continue
        if version:
            buffer.append(line)
    if version:
        sections[version] = "\n".join(buffer).strip()
    return {k: v for k, v in sections.items() if v}


def demote_headings(body):
    """Shift ATX headings down two levels so they sit under the page title.

    Fenced code blocks are skipped so a shell comment is not mistaken for a
    heading.
    """
    lines = []
    fence = None
    for line in body.split("\n"):
        fence_match = re.match(r"^\s*(```+|~~~+)", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            lines.append(line)
            continue

        if fence is None:
            heading = re.match(r"^(#{1,4})(\s+)(.*)$", line)
            if heading:
                line = "#" * min(len(heading.group(1)) + 2, 6) + heading.group(2) + heading.group(3)
        lines.append(line)
    return "\n".join(lines)


def reflow(body):
    """Join hard-wrapped continuation lines back into one logical line each.

    NEWS.md files here wrap bullets at ~75 columns, so reading a bullet one
    physical line at a time truncates it mid-sentence.
    """
    items = []
    for raw in body.split("\n"):
        starts_block = (
            not raw.strip()
            or re.match(r"^\s*([-*+]|\d+\.)\s+", raw)
            or raw.lstrip().startswith(("#", "```", "~~~", "|", ">"))
        )
        if starts_block or not items or not items[-1].strip():
            items.append(raw)
        else:
            items[-1] = items[-1].rstrip() + " " + raw.strip()
    return items


def summarize(body, fallback):
    """First prose sentence of the notes, for the listing description."""
    for raw in reflow(body):
        line = raw.strip()
        if not line or line.startswith(("#", "```", "~~~", "|", ">")):
            continue
        # Bullet marker. Some upstream entries omit the space after "*", so
        # allow that too -- but not when the "*" is opening emphasis instead.
        if re.match(r"^\*\S", line) and line.count("*") == 1:
            line = line[1:]
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^\d+\.\s+", "", line)          # ordered marker
        line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)   # bold
        line = re.sub(r"`(.+?)`", r"\1", line)         # code spans
        line = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", line)  # links
        # GitHub's generated bullets end "by @user in <pull request url>", which
        # is attribution noise in a one-line summary.
        line = re.sub(r"\s+by\s+@[\w-]+\s+in\s+\S+\s*$", "", line)
        line = line.strip()
        if line.lower().startswith("full changelog"):
            continue
        if not line:
            continue
        # Prefer ending on a sentence boundary over a hard character cut.
        sentence = re.match(r"^(.+?[.!?])(?:\s|$)", line)
        if sentence and len(sentence.group(1)) >= 40:
            line = sentence.group(1)
        if len(line) > 180:
            line = line[:177].rstrip() + "..."
        return line
    return fallback


def yaml_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_entry(repo, slug, logo, release, news_sections):
    version = release["tag_name"].lstrip("vV")
    title = f"{repo} {version}"
    published = release["published_at"][:10]

    # Prefer the hand-written changelog entry; fall back to the release body.
    body = news_sections.get(version, "").strip()
    if not body:
        body = (release.get("body") or "").replace("\r\n", "\n").strip()

    description = summarize(body, f"Release notes for {title}.")
    front = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {published}",
        f"description: {yaml_quote(description)}",
        f"categories: [{repo}]",
        f"image: ../assets/{logo}",
        f"image-alt: {yaml_quote(repo + ' logo')}",
        "toc: false",
        "---",
        "",
    ]

    parts = ["\n".join(front)]
    parts.append(demote_headings(body) if body else "_No release notes were provided._")
    parts.append("")
    parts.append(
        f"[Release on GitHub]({release['html_url']}) · "
        f"[About {repo}](../software/{slug}.qmd)"
    )
    parts.append("")

    path = NEWS_DIR / f"{slug}-{version}.qmd"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def main():
    NEWS_DIR.mkdir(exist_ok=True)
    # Regenerate from scratch so releases deleted upstream do not linger.
    for stale in NEWS_DIR.glob("*.qmd"):
        stale.unlink()

    written = 0
    skipped = []
    for repo, (slug, logo) in PACKAGES.items():
        try:
            releases = fetch_releases(repo)
        except urllib.error.HTTPError as error:
            print(f"  {repo}: HTTP {error.code} — skipped", file=sys.stderr)
            skipped.append(repo)
            continue
        except urllib.error.URLError as error:
            print(f"  {repo}: {error.reason} — skipped", file=sys.stderr)
            skipped.append(repo)
            continue

        news_sections = fetch_news_sections(repo)
        published = [r for r in releases if not r.get("draft") and not r.get("prerelease")]
        for release in published:
            write_entry(repo, slug, logo, release, news_sections)
        written += len(published)

        notes = []
        if not published:
            notes.append("no published releases")
        undated = sorted(set(news_sections) - {r["tag_name"].lstrip("vV") for r in published})
        if undated:
            notes.append(f"NEWS.md but no release: {', '.join(undated)}")
        suffix = f"  ({'; '.join(notes)})" if notes else ""
        print(f"  {repo}: {len(published)} release(s){suffix}")

    print(f"Wrote {written} entries to {NEWS_DIR.relative_to(ROOT)}/")
    if skipped:
        # Fail loudly: a silent partial run would quietly drop a package's
        # history from the site on the next commit.
        print(f"Failed to fetch: {', '.join(skipped)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
