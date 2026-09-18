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

## Setup and command policy

There is no requirements file. Install the documented build dependencies
explicitly:

```bash
python -m pip install mkdocs-material==9.7.7 mkdocs-awesome-pages-plugin==2.10.1 mkdocs-roamlinks-plugin==0.3.2 mkdocs-rss-plugin==1.19.0
```

The following commands are reference commands for the site owner:

```bash
mkdocs serve                         # local preview with live reload
mkdocs build                         # production-equivalent local build
python -m py_compile hooks/obsidian_compat.py
```

Agents must not install build dependencies or run actual preview, build, or
deployment commands. In particular, do not run `mkdocs serve`, `mkdocs build`,
or `mkdocs gh-deploy`. Site builds and deployment belong to the site owner and
GitHub Actions.

### Dangerous command approval

Agents must obtain separate, explicit user approval immediately before running
any command that can cause destructive, difficult-to-reverse, privileged, or
externally visible changes. A general request to edit the repository does not
count as approval for these commands.

Commands that require approval include, but are not limited to:

- permanent or recursive deletion, destructive overwrites, and bulk moves or
  renames whose targets cannot be recovered reliably;
- `git reset --hard`, `git clean`, force pushes, history rewrites, and deleting
  branches or tags;
- recursive permission or ownership changes and commands that modify system
  configuration, services, packages, credentials, or access controls;
- deployment, publication, remote data mutation, and other commands that
  affect external systems or people;
- arbitrary code execution through Obsidian `eval` or `command`, and permanent
  Obsidian deletion or sync-history restoration;
- destructive commands that depend on unresolved variables, command
  substitution, globs, or broad targets such as a vault root or repository
  root.

Before requesting approval, inspect the target with read-only commands where
possible. The approval request must state the exact command or operation,
resolved targets, expected effect, and whether recovery is possible. Approval
is valid only for the described operation; do not infer approval for similar
commands or additional targets. Do not create reusable approval prefixes for
destructive commands. Prefer a recoverable alternative, such as Obsidian's
default trash behavior, whenever it can satisfy the task.

## Obsidian CLI authorization

These rules are standing authorization for every agent session in this
repository. The Obsidian desktop app must be running before using its CLI.

- Agents may use the Obsidian CLI without asking again to read, search, or
  inspect the `priv` vault and to create, append, prepend, move, rename, or edit
  files and properties in that vault. Task updates, template insertion, Base
  item creation, and local file-history restoration count as file edits.
- Agents may delete files without asking again only through Obsidian's default
  recoverable trash behavior. Resolve and report the exact target first. Never
  pass the `permanent` flag without separate explicit approval.
- Run every Obsidian CLI command through
  `/bin/sh .codex/bin/obsidian-priv` on the native host from the first attempt.
  Do not call `obsidian` directly. Omit `vault=` and prefer exact `path=`
  values over ambiguous `file=` names.
- Never invoke `obsidian` from the sandbox or a `PreToolUse` hook, and never
  access `.obsidian-cli.sock` directly. The sandbox has an isolated IPC
  namespace: the socket pathname can be visible while the running app remains
  unreachable. Invoking the CLI there can fall back to starting a new GUI.
- The wrapper first checks for an existing Obsidian GUI process. It then runs
  `obsidian vault info=path` from a neutral directory outside every Vault, so
  the CLI reports the active Vault instead of selecting one from the working
  directory. It runs the requested command only when that path exactly equals
  this working root. If either check fails, stop without launching the app or
  opening or switching Vaults.
- Reusable approval prefixes must end at one exact subcommand, for example
  `["/bin/sh", ".codex/bin/obsidian-priv", "read"]`,
  `["/bin/sh", ".codex/bin/obsidian-priv", "create"]`, or
  `["/bin/sh", ".codex/bin/obsidian-priv", "property:set"]`. Never request
  or use the broader `["/bin/sh", ".codex/bin/obsidian-priv"]` prefix.
- Do not create a reusable prefix for `delete` or `history:restore`; execute
  each only after a read-only target/version check and without widening the
  command prefix.
- This standing authorization excludes permanent deletion, arbitrary `eval`
  or `command` execution, plugin or theme changes, sync state or sync-history
  restoration, and app reload/restart. Obtain separate explicit approval for
  those operations.

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

- Do not run MkDocs or other actual builds as part of verification.
- For content, navigation, or MkDocs configuration changes, review the scoped
  diff, run whitespace checks, parse edited YAML/frontmatter, and search for
  stale links or references without building the site.
- For Python hook changes, use static inspection only unless the user
  explicitly requests a separate runtime check.
- Report checks that could not be performed; do not install dependencies or
  suppress warnings to make verification appear complete.

## Change discipline

- Keep changes scoped to the request and preserve unrelated user edits.
- Avoid adding dependencies unless the requested behavior requires them.
- If dependencies change, update both this file's setup command and the CI
  installation steps so local and deployed builds remain aligned.
