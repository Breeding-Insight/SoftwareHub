# Contributing documentation and training material

## Choose the content type first

- **Software page:** one concise landing page per maintained tool.
- **Tutorial:** a focused, reproducible task with a bounded outcome.
- **Workflow:** an end-to-end analysis that may span several tools or packages.
- **Guide:** decision support, orientation, or a recommended route through the ecosystem.
- **Concept:** a concise explanation of an analytical idea that supports multiple tutorials.
- **Workshop:** event-focused material; may later link to maintained tutorials and workflows.
- **Reference:** remains with the package unless it is genuinely cross-package.

## Required learning metadata

Every file in `learn/` should use the same metadata dimensions:

```yaml
---
title: "From MADC output to analysis-ready VCF"
description: "Use BIGr to filter targeted sequencing data and create a standards-compliant VCF."
categories:
  - Genotype Data
  - Data Quality
  - Ploidy & Dosage
image: ../assets/example.svg
order: 20
learning-type: Workflow
software:
  - BIGr
level: Intermediate
keywords:
  - DArTag
  - MADC
  - VCF
  - dosage
---
```

### `categories`: broad user-facing topics

Use these as the primary discovery system. Prefer the controlled vocabulary below:

- `Getting Started`
- `Genotype Data`
- `Data Quality`
- `Ploidy & Dosage`
- `Population Analysis`
- `Trait Mapping`
- `Genomic Prediction`

Add a new broad category only when multiple durable pages justify it. Do not put package names, difficulty levels, or one-off keywords in `categories`.

### `software`: tools used by the material

Examples:

- `BIGr`
- `BIGapp`
- `Qploidy2`
- `DeltaBreed`

A cross-package workflow may list several tools.

### `level`: expected learner experience

Use exactly one:

- `Beginner`
- `Intermediate`
- `Advanced`

### `learning-type`: instructional form

Use exactly one:

- `Tutorial`
- `Workflow`
- `Guide`
- `Concept`

### `keywords`: precise search terms

Use this for specific technologies, formats, methods, organisms, or analyses such as `MADC`, `VCF`, `DArTag`, `GWAS`, `PCA`, or `alfalfa`.

## Writing expectations

- State the biological or analytical goal before showing code.
- Name required inputs and assumptions.
- Provide a reproducible setup.
- Explain consequential analytical decisions rather than only listing commands.
- Use checkpoints after major transformations.
- Show expected outputs where interpretation matters.
- Document common failure modes.
- Link to the next logical workflow.
- Do not duplicate canonical API reference text.

## Discovery behavior on `learn.qmd`

The Learn page uses a custom Quarto listing template (`assets/learn-listing.ejs.md`) with native listing filtering and pagination. The template renders `learning-type`, `software`, and `level` as separate badges and keeps broad `categories` visible as topic tags. Goal cards and topic chips write a `?filter=` query parameter and use `assets/learn-filter.html` to apply that value to the listing filter. This keeps deep links shareable while allowing the underlying listing to remain metadata-driven.


## Concept page pattern

Concept pages should be concise enough to read before a workflow but substantial enough to prevent common analytical misunderstandings. Prefer this order:

1. One-sentence definition.
2. A small concrete example.
3. The distinction users most often miss.
4. Practical consequences for breeding/genomics analysis.
5. A short takeaway.
6. Links to the next tutorial or workflow.
7. A small set of primary or authoritative further-reading sources.

Do not turn a Concept page into package API reference. Package-specific function arguments remain canonical in the package documentation.
