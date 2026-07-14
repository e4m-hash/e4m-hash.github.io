# Repository Guidelines

## Project Structure & Module Organization

This repository is a Material for MkDocs site backed by an Obsidian vault. Publishable Markdown lives under `docs/`; this directory contains the Linear Algebra notes (`1강.md` through `5강.md`, `Q1.md`, and `Q2.md`). Keep images in `attachments/`, the section landing page in `index.md`, and navigation metadata in `.pages`.

Site-wide behavior is configured in `mkdocs.yml`. `hooks/obsidian_compat.py` adapts Obsidian math and tables for Python-Markdown, while `.github/workflows/ci.yml` builds and deploys GitHub Pages. Do not edit generated or local-only directories such as `site/`, `.cache/`, `.trash/`, or `__pycache__/`.

## Build, Test, and Development Commands

Run commands from the repository root:

```bash
python -m pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-roamlinks-plugin mkdocs-rss-plugin
mkdocs serve
mkdocs build
python -m py_compile hooks/obsidian_compat.py
```

`mkdocs serve` starts a local preview. `mkdocs build` performs the production-equivalent static-site build. Compile the hook after Python changes. Do not run `mkdocs gh-deploy`; deployment is handled by GitHub Actions.

## Content Style & Naming Conventions

Match the surrounding Korean prose and preserve established filenames and Obsidian wikilinks. Use `$$...$$` for display math and fenced `mermaid` blocks for diagrams. Store note-specific assets under `attachments/`. Use four-space indentation in Python and keep hook transformations narrow: fenced code and table content must remain unchanged.

Use `.pages` for section titles and ordering, ending curated `nav` lists with `...` so new notes remain visible.

## Testing Guidelines

There is no dedicated unit-test suite or coverage threshold. For content, navigation, hooks, or MkDocs configuration, run `mkdocs build` and review all warnings, especially broken links and anchors. For hook changes, also run the Python compile check. Verify math changes in both Obsidian and the generated site when practical.

## Commit & Pull Request Guidelines

Recent history uses short, imperative subjects with prefixes such as `Fix:` and `Add:`. Keep each commit scoped, for example `Fix: LaTeX color rendering`. Pull requests should explain the affected notes or configuration, list validation performed, link related issues, and include screenshots when rendered output changes.
