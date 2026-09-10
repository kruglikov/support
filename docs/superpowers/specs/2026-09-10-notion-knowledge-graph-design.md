# Notion Knowledge Graph — Design

**Date:** 2026-09-10
**Status:** Approved for planning
**Scope:** Sub-project 1 of the Support project — Notion mirror, graph extraction, and a click-only viewer.

## Purpose

Two goals, in priority order:

1. **Interview support.** During a software interview, navigate a knowledge tree by clicking alone — no typing — to find a hint fast. Must work offline and feel instant.
2. **Memorization.** Study the same content between interviews, using the toggle sections already present in Notion as hidden-answer prompts.

Notion remains the single source of truth. Nothing in this system writes back to Notion.

## Constraints

| Constraint | Source | Consequence |
|---|---|---|
| Click-only navigation | Interview use; typing is visible and slow | Tree is the primary interface. Search is optional, never required. |
| Fully offline at view time | Cannot depend on the network mid-interview | Viewer reads local files only. No Notion API call during viewing. |
| Three separately replaceable layers | Explicit user requirement | Mirror, graph, and viewer communicate through files on disk, never through shared code. |
| Manual sync only | User choice | No daemon, no polling, no background process. |
| Boring stack | Value is in the content, not the tooling | Python + Notion SDK for sync/extract; vanilla JS static viewer, no build step. |

## Findings from the real content

Observed by inspecting the live workspace on 2026-09-10 via the Notion MCP connector. Root page:
`https://app.notion.com/p/kruglikov/Software-Development-9bbf3c16e12041f3996bae0eb316cd78`

Sample page analyzed in depth — `OOP\Principles\Patterns`:
`https://app.notion.com/p/3649c92c96f5805b9c4ff011b3d65977`

1. **The page tree is shallow; the mass is inside pages.** The root has ~35 child pages. The sampled page is 200,332 characters across 3,964 lines with only 2 subpages of its own.

2. **Code fences generate false headings.** The sampled page has 36 real headings and 9 heading-like lines *inside* code blocks (e.g. `# Professors created independently`, `# rooms are only accessible through house`). A line-based extractor that ignores fence state pollutes the tree with 9 bogus top-level topics on this page alone.

3. **Toggle headings are the memorization unit.** 17 headings carry `{toggle="true"}` — including `IoC`, `DDD`, `DDD Layers`, `CQRS`, `Event Sourcing`, `Hexagonal Architecture`, and `Interview questions`. A collapsed toggle is already a prompt with a concealed answer.

4. **Red spans encode user-assigned priority.** 13 occurrences of `<span color="red">` on entries such as `GoF (Design) patterns`, `Distributed System Patterns`, and `Microservices\Distributed Architecture`.

5. **Heading levels skip.** `OOP` is H1 with H3 children; `Distributed System Patterns` is H2 with an H4 child. Nesting must be computed from relative rank order within a page, not absolute heading level.

6. **The API returns partial data.** The root fetch reported `truncated: true` with 1 unknown block, and the page contains an inline database and a `<columns>` block.

**Central design consequence:** the tree the user clicks is not the Notion page tree. It is the heading hierarchy *inside* pages, with page titles forming the upper levels.

## Architecture

Three layers, each a separate directory, each communicating only through files:

```
Notion API
    │  (sync — manual, incremental)
    ▼
mirror/                     ← layer 1 output: Markdown + raw JSON + manifest
    │  (extract — pure, deterministic, rebuilt from scratch)
    ▼
graph/graph.json            ← layer 2 output: nodes + edges
    │  (read-only, at view time)
    ▼
viewer/                     ← layer 3: static local web app
```

Rules that keep the layers replaceable:

- The graph layer reads only `mirror/`. It never calls the Notion API.
- The viewer reads only `graph/graph.json`. Section content is carried inline in the node, so the viewer never touches `mirror/` and never imports graph-layer code.
- `graph.json` is regenerated whole on every build and is never edited in place.
- Replacing any layer requires honoring only its output file format, documented below.

### Layer 1 — mirror

**Command surface:**

```
sync            fetch changed pages, update mirror and manifest, report changes
sync --full     ignore the manifest, refetch everything
status          report what would change; write nothing
```

**Output layout** (paths relative to `/home/viktar/Projects/Support/mirror/`):

- `<page-slug>.md` — one Markdown file per Notion page, in a directory tree mirroring the page tree.
- `.raw/<page-id>.json` — the untouched API response for that page.
- `manifest.json` — per page: Notion ID, `last_edited_time`, parent ID, title, output path, content hash.

Keeping `.raw/` alongside the Markdown means a future graph extractor can reach for block-level detail the Markdown conversion dropped without forcing a re-sync. This is the hedge that buys back most of the losslessness a pure-Markdown mirror gives up.

**Change detection.** Compare each page's `last_edited_time` against `manifest.json`; fetch only pages that moved. Pages that disappear or lose sharing are pruned from the mirror and the manifest.

**Reliability.** The Notion API rate-limits at roughly 3 requests/second; the sync throttles itself. The manifest entry for a page is written only *after* that page's files are written, so an interrupted sync resumes cleanly rather than leaving the manifest ahead of the mirror.

**Partial data.** Paginated responses are followed to completion. Block types the converter does not understand are skipped and recorded as warnings in the sync report — never dropped silently.

### Layer 2 — graph

A pure function from `mirror/` to `graph/graph.json`. No network, no state, deterministic.

**Nodes.** One node per page, plus one per heading section. A heading section owns the content between its heading and the next heading of equal or higher rank.

```json
{
  "id": "<page-id>#<heading-slug>",
  "type": "page | section",
  "title": "CQRS",
  "level": 2,
  "page_id": "...",
  "page_title": "OOP\\Principles\\Patterns",
  "is_toggle": true,
  "is_priority": false,
  "content_md": "..."
}
```

`is_toggle` comes from finding 3, `is_priority` from finding 4.

**Edges**, three kinds, independently removable:

- `contains` — page→section and section→subsection. Built from **relative rank order** within the page (finding 5), not absolute heading level. This is what the viewer renders as the tree.
- `links_to` — Notion page links found in section content.
- `mentions` — a section whose title appears verbatim in another section's text.

`contains` alone yields a usable tree. `links_to` and `mentions` enrich it. If `mentions` proves noisy in practice, removing it affects nothing else.

**Extraction rules:**

- Heading detection **must** track code-fence state and ignore heading-like lines inside fences (finding 2). This is the layer's most important correctness requirement.
- Heading titles are stripped of inline markup (`**`, `<span>`) for display, with the priority flag preserved separately.
- Nesting is computed with a stack of open headings, popping until the top has a rank strictly higher than the current heading.

### Layer 3 — viewer

A static local web app — plain HTML, CSS, and JavaScript, no build step — served from `/home/viktar/Projects/Support/viewer/`, reading `graph/graph.json` and nothing else.

Inlining content in `graph.json` puts the whole corpus in one file — on the order of several megabytes given the observed page sizes. That parses in well under a second locally and buys a viewer with a single dependency, which matters more than file size for an offline tool.

- **Left pane:** the full `contains` tree, collapsed to top level on load. Click to expand a branch, click a leaf to load it. Nodes with `is_priority` carry extra visual weight.
- **Right pane:** rendered content for the selected node. Sections with `is_toggle` render collapsed, their title acting as a clickable prompt that reveals the answer — the memorization and interview flow.
- **Related strip:** `links_to` and `mentions` targets for the current node, as clickable chips. One click to a related topic.
- **No text input anywhere in the MVP.**

**Deliberately out of the MVP:** graph visualization. Under interview pressure a familiar tree beats a force-directed layout that has to be read. A graph view can be added later as a second surface over the same `graph.json` without touching the other layers.

## Error handling

| Failure | Behavior |
|---|---|
| Notion auth invalid or expired | `sync` fails immediately with a clear message; the mirror is left untouched and the viewer keeps working on existing data. |
| Network unavailable during sync | Same — fail fast, leave the mirror intact. |
| Rate limit hit | Back off and retry; the sync is resumable. |
| Sync interrupted mid-run | Manifest lags the mirror by at most one page; the next `sync` refetches that page. No corruption. |
| Unknown or unsupported block type | Skipped, recorded as a warning in the sync report, raw JSON still preserved in `.raw/`. |
| Malformed Markdown breaks extraction | The graph build fails loudly for that page and reports it; the previous `graph.json` stays in place. |
| `graph.json` missing when the viewer loads | The viewer shows an explicit "run the graph build" message rather than an empty tree. |

## Testing

- **Mirror:** change detection against a fixture manifest — unchanged pages are skipped, edited pages refetched, removed pages pruned. Interrupted-sync resumption.
- **Graph:** the code-fence case from finding 2 is a required regression test — a fixture page with heading-like comments inside fences must produce zero nodes from them. Level-skipping nesting (H1→H3, H2→H4) from finding 5 is a second required test. Toggle and priority flag extraction.
- **Viewer:** loads a fixture `graph.json`, renders the tree, expands and selects without any network request.

The two extraction tests are non-negotiable: both correspond to defects confirmed present in the real content.

## Out of scope

Writing back to Notion. Background or scheduled sync. Graph visualization. Full-text search. Spaced-repetition scheduling. Multi-user or hosted deployment. Non-Notion sources.

## Open items for implementation planning

**Decided, for the plan to implement:**

- **Slug collisions.** Page slugs derive from the title; on collision, append the first 8 characters of the Notion page ID. Deterministic, stable across syncs, and readable.
- **Mirror under git.** `mirror/` is committed to the project repository. Every `sync` therefore produces a reviewable diff of what changed in Notion — directly useful for study, and free.

**Prerequisite, not a code task:**

- Notion integration setup: create an internal integration, copy the token, share the root `Software Development` page with it. The token is read from the environment, never committed.
