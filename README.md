# Breeding Insight Software Hub: Quarto starter

A repo-ready starter for a unified Breeding Insight software, tutorial, workshop, and documentation portal.

## Design intent

- **Tidyverse-inspired software directory:** concise tool descriptions with direct routes to docs, source, installation, and tutorials.
- **Workflow-first learning:** tutorials are organized around outcomes and may span packages.
- **Durable workshops:** each event can bundle setup, modules, exercises, solutions, and recordings.
- **One BI visual system:** shared colors, typography, logo, and UI patterns.

## Local preview

Requires Quarto 1.6+ for `_brand.yml`; a current Quarto release is recommended.

```bash
quarto preview
```

## Render

```bash
quarto render
```

The site is written to `_site/`.

## Add software

1. Copy an existing file in `software/`.
2. Update `title`, `description`, `categories`, and `image` in YAML.
3. Add installation and canonical links.
4. Render. The `software.qmd` listing updates automatically.

## Add learning material

1. Create a `.qmd` file in `learn/`.
2. Include `title`, `description`, topic-only `categories`, `image`, `order`, `learning-type`, `software`, `level`, and `keywords`.
3. Use the controlled vocabulary documented in `CONTRIBUTING.md`.
4. Follow the tutorial pattern in `resources.qmd`.
5. For a concept page, use the concise explanatory pattern in `learn/what-is-allele-dosage.qmd`.
6. Render. The `learn.qmd` listing and topic discovery system update from page metadata.

The Learn page is task-first. Broad scientific topics drive visible categories; package names, difficulty, content type, and precise search terms remain separate metadata dimensions. Goal cards can pre-filter the Quarto listing through shareable `?filter=` URLs. A custom metadata-driven listing template renders `learning-type`, `software`, and `level` as distinct badges while retaining searchable topic tags.

## Deployment

The included GitHub Actions workflow renders the site and publishes the `_site/` artifact with GitHub Pages.

Before first deployment:

1. Update `website.site-url` in `_quarto.yml`.
2. Update `website.repo-url` to the actual repository.
3. In GitHub repository settings, set Pages source to **GitHub Actions**.

## Migration strategy

- Keep package API reference canonical in package-specific docs/pkgdown sites.
- Move durable tutorials and workshops into this portal.
- Link to release notes and function reference rather than copying them.
- Add redirects from old URLs where possible.
