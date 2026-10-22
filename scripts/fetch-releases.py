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

Every news/*.qmd is generated. Do not hand-edit them; edit the release notes or
NEWS.md upstream and re-run this script. news/_metadata.yml (page styling) is
hand-written and left alone.

The script also syncs each software page's `version`, `version-date`, and
`version-url` front matter from the latest published release of the repository in
its `links.source`, or in `release-repo` when the releases are published elsewhere
(DeltaBreed's are in bi-web). Pages whose repository has no published release get no
version. A page with `version-source: manual` keeps its hand-set version and is skipped.
Those three fields are generated too; do not hand-edit them.

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
SOFTWARE_DIR = ROOT / "software"
VERSION_FIELDS = ("version", "version-date", "version-url")


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


def normalize_version(tag):
    """Release tag -> version number: "v2.1.0" and "v.2.1.0" both become "2.1.0"."""
    return re.sub(r"^[vV]\.?", "", tag.strip())


def latest_release(releases):
    published = [r for r in releases if not r.get("draft") and not r.get("prerelease")]
    if not published:
        return None
    return max(published, key=lambda r: r["published_at"])


def source_repo(page_text):
    """The repository whose releases give a software page its version.

    `release-repo: <name>` in the front matter wins; otherwise the Breeding-Insight
    repository named in links.source.
    """
    override = re.search(r"^release-repo:\s*([\w.\-]+)\s*$", page_text, re.M)
    if override:
        return override.group(1)
    match = re.search(
        rf"^\s+source:\s*https://github\.com/{ORG}/([\w.\-]+?)/?\s*$", page_text, re.M
    )
    return match.group(1) if match else None


def set_version_fields(page_text, release):
    """Replace the generated version fields in a page's front matter.

    They sit right after the `status:` line, so the hand-written fields stay as they are.
    """
    end = page_text.index("\n---", 3)
    front, rest = page_text[:end], page_text[end:]
    front = "\n".join(
        line for line in front.split("\n")
        if not any(line.startswith(f"{field}:") for field in VERSION_FIELDS)
    )
    if release:
        fields = "\n".join([
            f"version: {yaml_quote(normalize_version(release['tag_name']))}",
            f"version-date: {release['published_at'][:10]}",
            f"version-url: {release['html_url']}",
        ])
        front, count = re.subn(r"^(status: .*)$", lambda m: m.group(1) + "\n" + fields, front, count=1, flags=re.M)
        if not count:
            front += "\n" + fields
    return front + rest


def sync_versions(release_cache):
    """Write the latest release of each software page's repository into its front matter."""
    for page in sorted(SOFTWARE_DIR.glob("*.qmd")):
        text = page.read_text(encoding="utf-8")
        if re.search(r"^version-source:\s*manual\s*$", text, re.M):
            print(f"  {page.name}: manual")
            continue
        repo = source_repo(text)
        release = None
        if repo:
            if repo not in release_cache:
                release_cache[repo] = fetch_releases(repo)
            release = latest_release(release_cache[repo])
        updated = set_version_fields(text, release)
        if updated != text:
            page.write_text(updated, encoding="utf-8")
        label = normalize_version(release["tag_name"]) if release else "no release"
        print(f"  {page.name}: {label}")


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
    version = normalize_version(release["tag_name"])
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
    release_cache = {}
    for repo, (slug, logo) in PACKAGES.items():
        try:
            releases = fetch_releases(repo)
            release_cache[repo] = releases
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
        undated = sorted(set(news_sections) - {normalize_version(r["tag_name"]) for r in published})
        if undated:
            notes.append(f"NEWS.md but no release: {', '.join(undated)}")
        suffix = f"  ({'; '.join(notes)})" if notes else ""
        print(f"  {repo}: {len(published)} release(s){suffix}")

    print(f"Wrote {written} entries to {NEWS_DIR.relative_to(ROOT)}/")

    if skipped:
        # Leave the page versions alone rather than clearing them for a failed repository.
        print("Skipping version sync because some releases could not be fetched.", file=sys.stderr)
    else:
        print("Software page versions:")
        try:
            sync_versions(release_cache)
        except urllib.error.URLError as error:
            print(f"Version sync failed: {error}", file=sys.stderr)
            return 1

    if skipped:
        # Fail loudly: a silent partial run would quietly drop a package's
        # history from the site on the next commit.
        print(f"Failed to fetch: {', '.join(skipped)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
