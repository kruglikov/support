# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

    python3 -m pip install -e ".[dev]"            # install
    python3 -m pytest                             # all tests
    python3 -m pytest tests/test_headings.py -v   # one module
    python3 -m pytest tests/test_headings.py::test_heading_like_lines_inside_code_fences_are_ignored -v   # one test

    support status        # what a sync would change; writes nothing
    support sync          # incremental fetch into mirror/
    support sync --full   # ignore the manifest, refetch everything
    support build-graph   # rebuild graph/graph.json from mirror/
    support serve         # http://127.0.0.1:8765/viewer/index.html

`support <subcommand>` works once the package is installed on `PATH`; `python3 -m support.cli <subcommand>` works identically via `src/support/cli.py`'s `__main__` guard, without depending on the console script being on `PATH`.

`support sync` and `support status` need `NOTION_TOKEN` and `NOTION_ROOT_PAGE_ID` in the environment. Every other command works offline.

## Architecture

Three layers that communicate only through files. No layer imports another layer's code, and each can be replaced by honouring its output format alone.

1. **Mirror** (`src/support/notion_api.py`, `src/support/markdown.py`, `src/support/sync.py`) — reads Notion, writes `mirror/<slug>.md`, `mirror/.raw/<page-id>.json`, and `mirror/manifest.json`. Incremental by `last_edited_time`. A page's manifest entry is written only after that page's files, so an interrupted sync resumes rather than corrupts. `src/support/notion_api.py` recurses into nested blocks and attaches them as `block["children"]`, and `src/support/markdown.py` renders those children flat, because a toggleable Notion heading stores its body as child blocks — without this, every toggle section would mirror with an empty body. `src/support/sync.py` deletes a page's previous mirror file when a rename gives it a new slug, so no orphaned files accumulate.
2. **Graph** (`src/support/graph.py`, `src/support/headings.py`) — a pure function from `mirror/` to `graph/graph.json`. Never calls Notion. Regenerated whole on every build. Mention edges are built with one alternation regex over all section titles, sorted longest-first, so a longer title wins over a shorter prefix; matches are bounded by `(?<!\w)` and `(?!\w)` rather than `\b`, so a title with leading or trailing punctuation such as `.NET` still matches.
3. **Viewer** (`viewer/`) — vanilla JavaScript, no build step. Reads `graph/graph.json` and nothing else. No network at view time, no text input. `support serve` (`src/support/cli.py`) serves only paths under `/viewer/` and `/graph/`; every other path, including `/.env` and `/.git/...`, returns 404. Request paths are percent-decoded before that check, matching what the standard library's HTTP handler does, so an encoded traversal attempt such as `/viewer/%2e%2e/.env` is rejected too. This is what keeps `.env` (which holds `NOTION_TOKEN`) and `.git` from ever being served.

## What the content actually looks like

The Notion page tree is shallow — roughly 35 topic pages — but individual pages are enormous; `OOP\Principles\Patterns` is over 200,000 characters. **The tree a user clicks is the heading hierarchy inside pages, not the Notion page tree.**

Three properties of that content drive the design:

- **Code fences contain heading-like lines.** One sampled page has 36 real headings and 9 `#` comments inside Python and bash code blocks. `src/support/headings.py` tracks fence state; breaking that fills the tree with garbage nodes. `tests/test_headings.py` guards it.
- **Heading levels skip.** H1 is followed by H3, H2 by H4. Nesting is computed from relative rank order using a stack, never from absolute heading level.
- **Toggle headings and red spans are user signals.** `{toggle="true"}` marks a section the user treats as a hidden answer, and `<span color="red">` marks a priority topic. Both survive into `graph.json` as `is_toggle` and `is_priority`, and the viewer renders them differently. Do not strip either as formatting noise.

## Conventions

A section owns only its own content — the lines between its heading and the next heading of any rank. Descendant content is reached through `contains` edges, never duplicated into ancestors.

Node identifiers are `<page-id>` for pages and `<page-id>#<section-index>` for sections.

Edge kinds are `contains` (the tree), `links_to` (Notion links), and `mentions` (a section title occurring in another section's text). Only `contains` is load-bearing; the other two can be removed without affecting anything else.
