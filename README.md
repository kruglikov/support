# Support

A local mirror of a Notion knowledge base, a knowledge graph extracted from it, and a click-only viewer for use during interviews.

Notion is the source of truth. Nothing here writes back to Notion.

## Setup

    python3 -m pip install -e ".[dev]"
    cp .env.example .env   # then fill in both values and export them

`NOTION_TOKEN` is an internal integration secret; the integration must be connected to the root page. `NOTION_ROOT_PAGE_ID` is the ID of that root page.

## Commands

    support status        # report what a sync would change; writes nothing
    support sync          # fetch changed pages into mirror/
    support sync --full   # refetch every page
    support build-graph   # rebuild graph/graph.json from mirror/
    support serve         # serve the viewer at http://127.0.0.1:8765/viewer/index.html

`support <subcommand>` works once the package is installed; `python3 -m support.cli <subcommand>` works the same way without relying on the console script being on `PATH`.

Run `support sync` then `support build-graph` after editing Notion.

## Tests

    python3 -m pytest
    python3 -m pytest tests/test_headings.py -v   # the correctness core

71 tests currently pass.

## Layout

- `mirror/` — Markdown per page, raw API JSON under `mirror/.raw/`, and `mirror/manifest.json`. Committed, so each sync produces a reviewable diff of what changed in Notion.
- `graph/graph.json` — regenerated whole on every build; never edited by hand.
- `viewer/` — static HTML, CSS and JavaScript. Reads `graph/graph.json` and nothing else.

## Serving the viewer safely

`support serve` only serves paths under `/viewer/` and `/graph/`; every other request returns 404. This keeps the local server from ever handing out `.env` (which holds `NOTION_TOKEN`) or `.git`. Request paths are percent-decoded before that check, matching what the Python standard library's HTTP handler does, so an encoded traversal attempt such as `/viewer/%2e%2e/.env` is rejected too.
