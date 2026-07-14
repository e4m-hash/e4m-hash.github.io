# Repository Guidelines

## Project overview

This repository is a personal portfolio and digital garden built with Material
for MkDocs. The source is an Obsidian vault under `docs/`, and the rendered
static site is the product. Most published content is written in Korean.

Pushing to `main` or `master` runs `.github/workflows/ci.yml`, which builds and
deploys the site to GitHub Pages.

## Repository map

- `docs/`: publishable notes, blog posts, projects, and assets.
- `docs/**/.pages`: section titles and navigation order for awesome-pages.
- `mkdocs.yml`: theme, Markdown extensions, plugins, hooks, and site settings.
- `hooks/obsidian_compat.py`: build-time compatibility fixes for Obsidian
  Markdown.
- `.github/workflows/ci.yml`: GitHub Pages deployment workflow.
- `.obsidian/`: local Obsidian state and plugins; do not edit unless the task
  explicitly concerns the vault configuration.

Do not edit generated or local-only content in `site/`, `.cache/`, `.trash/`,
or `__pycache__/`.

## Setup and commands

There is no requirements file. Install the documented build dependencies
explicitly:

```bash
python -m pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-roamlinks-plugin mkdocs-rss-plugin
```

Use these commands from the repository root:

```bash
mkdocs serve                         # local preview with live reload
mkdocs build                         # production-equivalent local build
python -m py_compile hooks/obsidian_compat.py
```

Do not run `mkdocs gh-deploy` manually. Deployment belongs to GitHub Actions.

## Navigation and content conventions

- Keep publishable content under `docs/`.
- There is intentionally no central `nav:` in `mkdocs.yml`. Directory layout
  and `.pages` files define the sidebar.
- Use `.pages` to set Korean section names and ordering. End a curated `nav:`
  list with `...` so unlisted pages are included automatically.
- Add an explicit label in `.pages` only when it should differ from the page's
  first H1 or filename.
- Keep Obsidian wikilinks such as `[[Note Name]]`; the roamlinks plugin resolves
  them. Do not mechanically replace them with relative Markdown links.
- Put blog posts in `docs/blog/posts/`. Preserve `date`, `categories`, and
  `tags` frontmatter used by the blog and RSS plugins.
- Use `$$...$$` blocks for display math and fenced `mermaid` blocks for
  diagrams.
- Attachment directories may contain images, but Markdown files under
  `**/attachments/` are excluded from the site by `exclude_docs`.
- Match the language and style of the surrounding page. Do not translate
  Korean content unless requested.

## Writing style: write like a person

Always aim for prose that reads as if the site owner wrote it. Before adding
or rewriting content, read the surrounding page and at least one nearby page
of the same type (blog post, project page, or study note), then follow their
voice, level of detail, terminology, and Korean/English mix.

- Prefer direct, concrete sentences over polished promotional copy. State what
  was done, learned, observed, or remains uncertain.
- Preserve the author's natural variation: short explanations, fragments in
  lists, technical shorthand, and occasional first-person reflection are valid
  when they fit the page.
- Do not make every section follow the same template or force introductions,
  summaries, conclusions, or transition sentences where the surrounding
  writing does not use them.
- Avoid generic AI-style phrases, inflated claims, rhetorical filler, repeated
  restatements, and vague judgments such as "important", "powerful", or
  "innovative" without specific evidence.
- Use headings, bold text, lists, and tables only when they make the content
  easier to read. Do not over-structure a short note.
- Keep claims grounded in information already present or sources actually
  checked. Never invent personal experience, motivation, results, opinions,
  citations, or biographical detail to make a passage feel human.
- When the author's intent or personal viewpoint is required but unavailable,
  leave a clearly marked placeholder or ask the user instead of fabricating
  one.
- Edit only as much as needed. Do not normalize the entire page's wording,
  spacing, terminology, or bilingual style unless the task explicitly asks for
  a full editorial rewrite.
- Read the finished passage aloud in spirit: vary sentence length naturally,
  remove anything that sounds like a stock answer, and keep details a real
  reader would find useful.

## Obsidian compatibility hook

`hooks/obsidian_compat.py` makes Obsidian-authored math and tables render under
Python-Markdown. When changing it, preserve these invariants:

- fenced code blocks are never rewritten;
- inline `$$...$$` mixed with prose remains inline;
- standalone display-math blocks receive the blank lines arithmatex needs;
- indented display math is dedented without changing the relative indentation
  inside the block;
- table spacing fixes do not alter table content.

## Verification

- For content, navigation, hook, or MkDocs configuration changes, run
  `mkdocs build` and inspect warnings, especially broken links and anchors.
- For Python hook changes, also run
  `python -m py_compile hooks/obsidian_compat.py`.
- For documentation-only changes outside the published site, review the diff;
  a site build is optional.
- Do not suppress validation warnings merely to make a build appear clean.

## Change discipline

- Keep changes scoped to the request and preserve unrelated user edits.
- Avoid adding dependencies unless the requested behavior requires them.
- If dependencies change, update both this file's setup command and the CI
  installation steps so local and deployed builds remain aligned.
