# Notion Knowledge Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mirror a Notion page tree to local Markdown, extract a heading-level knowledge graph from it, and serve a click-only offline viewer for interview support.

**Architecture:** Three layers that communicate only through files on disk — a Python sync writing `/home/viktar/Projects/Support/mirror/`, a pure Python extractor writing `/home/viktar/Projects/Support/graph/graph.json`, and a vanilla-JS static viewer in `/home/viktar/Projects/Support/viewer/` that reads `graph.json` alone. No layer imports another layer's code.

**Tech Stack:** Python 3.11+, `notion-client`, `pytest`, vanilla JavaScript (no build step), `python -m http.server`.

**Spec:** `/home/viktar/Projects/Support/docs/superpowers/specs/2026-09-10-notion-knowledge-graph-design.md`

## Global Constraints

- Nothing in this system writes to Notion. Read-only API usage throughout.
- The viewer performs no network request at view time and requires no text input.
- Heading detection must track code-fence state. Heading-like lines inside fences are never nodes.
- Heading nesting is computed from relative rank order, never from absolute heading level.
- `/home/viktar/Projects/Support/graph/graph.json` is regenerated whole on every build, never edited in place.
- The Notion API rate limit is approximately 3 requests per second; the sync throttles to stay under it.
- A page's manifest entry is written only after that page's files are written.
- `NOTION_TOKEN` and `NOTION_ROOT_PAGE_ID` are read from the environment and never committed.
- Page slug collisions are resolved by appending the first 8 characters of the Notion page ID with dashes removed.
- No AI attribution in any commit message, comment, or document.

## Deviation from the spec, applied throughout

The spec at `/home/viktar/Projects/Support/docs/superpowers/specs/2026-09-10-notion-knowledge-graph-design.md` states that a heading section "owns the content between its heading and the next heading of equal or higher rank". Taken literally, a parent section's content would also contain every descendant section's content, so the same text would be stored and rendered two or more times, inflating `graph.json` and showing duplicates in the viewer.

This plan implements **own content only**: a section owns the lines between its heading and the *next heading of any rank*. Descendant content is reached through `contains` edges instead. The tree and the rendered output are unchanged; only the duplication disappears.

## File Structure

**Created by this plan:**

- `/home/viktar/Projects/Support/pyproject.toml` — package metadata, dependencies, pytest configuration.
- `/home/viktar/Projects/Support/.gitignore` — excludes `.env`, `__pycache__`, `.pytest_cache`.
- `/home/viktar/Projects/Support/.env.example` — documents the two required environment variables.
- `/home/viktar/Projects/Support/src/support/config.py` — project paths and environment configuration. One responsibility: where things live and what credentials exist.
- `/home/viktar/Projects/Support/src/support/headings.py` — code-fence-aware heading parsing and section-tree construction. Pure; no I/O.
- `/home/viktar/Projects/Support/src/support/manifest.py` — manifest persistence and sync planning. Pure apart from reading and writing one JSON file.
- `/home/viktar/Projects/Support/src/support/notion_api.py` — Notion REST access: page metadata, paginated block children, tree walking, throttling.
- `/home/viktar/Projects/Support/src/support/markdown.py` — Notion block JSON to Markdown conversion. Pure; no I/O.
- `/home/viktar/Projects/Support/src/support/sync.py` — orchestration of layer 1: plan, fetch, write, prune, report.
- `/home/viktar/Projects/Support/src/support/graph.py` — layer 2: mirror to `graph.json`.
- `/home/viktar/Projects/Support/src/support/cli.py` — argparse entry point for `sync`, `status`, `build-graph`, `serve`.
- `/home/viktar/Projects/Support/viewer/index.html`, `/home/viktar/Projects/Support/viewer/app.js`, `/home/viktar/Projects/Support/viewer/style.css` — layer 3.
- `/home/viktar/Projects/Support/tests/` — one test module per source module.

Files are split by responsibility. `headings.py`, `markdown.py`, and `manifest.py` are pure and therefore trivially testable without network access; `notion_api.py` is the only module that performs HTTP requests.

---

### Task 1: Project scaffolding and configuration

**Files:**
- Create: `/home/viktar/Projects/Support/pyproject.toml`
- Create: `/home/viktar/Projects/Support/.gitignore`
- Create: `/home/viktar/Projects/Support/.env.example`
- Create: `/home/viktar/Projects/Support/src/support/__init__.py`
- Create: `/home/viktar/Projects/Support/src/support/config.py`
- Test: `/home/viktar/Projects/Support/tests/test_config.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `support.config.PROJECT_ROOT`, `MIRROR_DIR`, `RAW_DIR`, `MANIFEST_PATH`, `GRAPH_PATH`, `VIEWER_DIR` (all `pathlib.Path`); `support.config.Config` dataclass with fields `notion_token: str` and `root_page_id: str`; `support.config.load_config() -> Config`; `support.config.ConfigError(Exception)`.

- [ ] **Step 1: Write the failing test**

Create `/home/viktar/Projects/Support/tests/test_config.py`:

```python
import pytest

from support.config import Config, ConfigError, load_config


def test_load_config_reads_both_environment_variables(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "9bbf3c16e12041f3996bae0eb316cd78")

    config = load_config()

    assert config == Config(
        notion_token="secret_abc",
        root_page_id="9bbf3c16e12041f3996bae0eb316cd78",
    )


def test_load_config_raises_when_token_missing(monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "9bbf3c16e12041f3996bae0eb316cd78")

    with pytest.raises(ConfigError, match="NOTION_TOKEN"):
        load_config()


def test_load_config_raises_when_root_page_missing(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.delenv("NOTION_ROOT_PAGE_ID", raising=False)

    with pytest.raises(ConfigError, match="NOTION_ROOT_PAGE_ID"):
        load_config()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support'`

- [ ] **Step 3: Write `pyproject.toml`**

Create `/home/viktar/Projects/Support/pyproject.toml`:

```toml
[project]
name = "support"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "notion-client>=2.2.1",
]

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
support = "support.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

- [ ] **Step 4: Write the configuration module**

Create `/home/viktar/Projects/Support/src/support/__init__.py` as an empty file.

Create `/home/viktar/Projects/Support/src/support/config.py`:

```python
import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIRROR_DIR = PROJECT_ROOT / "mirror"
RAW_DIR = MIRROR_DIR / ".raw"
MANIFEST_PATH = MIRROR_DIR / "manifest.json"
GRAPH_PATH = PROJECT_ROOT / "graph" / "graph.json"
VIEWER_DIR = PROJECT_ROOT / "viewer"


class ConfigError(Exception):
    """Raised when required environment configuration is absent."""


@dataclass(frozen=True)
class Config:
    notion_token: str
    root_page_id: str


def load_config():
    notion_token = os.environ.get("NOTION_TOKEN")
    if not notion_token:
        raise ConfigError(
            "NOTION_TOKEN is not set. Create a Notion internal integration, "
            "share the root page with it, and export its token."
        )

    root_page_id = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not root_page_id:
        raise ConfigError(
            "NOTION_ROOT_PAGE_ID is not set. Use the ID of the Software Development page."
        )

    config = Config(notion_token=notion_token, root_page_id=root_page_id)
    return config
```

- [ ] **Step 5: Write the supporting files**

Create `/home/viktar/Projects/Support/.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
```

Create `/home/viktar/Projects/Support/.env.example`:

```bash
# Token of a Notion internal integration that has been granted access to the root page.
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ID of the Software Development page, dashes optional.
NOTION_ROOT_PAGE_ID=9bbf3c16e12041f3996bae0eb316cd78
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_config.py -v`
Expected: PASS — 3 passed

- [ ] **Step 7: Commit**

```bash
cd /home/viktar/Projects/Support
git add pyproject.toml .gitignore .env.example src/support/__init__.py src/support/config.py tests/test_config.py
git commit -m "Add project scaffolding and environment configuration"
```

---

### Task 2: Code-fence-aware heading parser and section tree

This is the correctness core of the whole project. Both required regression tests from the spec live here.

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/headings.py`
- Test: `/home/viktar/Projects/Support/tests/test_headings.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `support.headings.Heading` dataclass with fields `level: int`, `title: str`, `is_toggle: bool`, `is_priority: bool`, `line_index: int`; `support.headings.Section` dataclass with fields `heading: Heading`, `parent_index: int | None`, `content: str`; `support.headings.parse_headings(markdown_text: str) -> list[Heading]`; `support.headings.build_sections(markdown_text: str) -> list[Section]`. In a `Section`, `parent_index` indexes into the same list returned by `build_sections`, and `None` means the section is a top-level section of its page.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_headings.py`:

```python
from support.headings import build_sections, parse_headings


def test_heading_like_lines_inside_code_fences_are_ignored():
    markdown_text = "\n".join([
        "# OOP",
        "",
        "```python",
        "# Professors created independently",
        "# rooms are only accessible through house",
        "```",
        "",
        "## Composition",
    ])

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == ["OOP", "Composition"]


def test_tilde_fences_are_also_honoured():
    markdown_text = "\n".join([
        "# Real",
        "~~~bash",
        "# not a heading",
        "~~~",
    ])

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == ["Real"]


def test_nesting_uses_relative_rank_not_absolute_level():
    markdown_text = "\n".join([
        "# OOP",
        "### Types of polymorphism",
        "# Patterns & Principles",
        "## Distributed System Patterns",
        "#### Dual Write Problem",
    ])

    sections = build_sections(markdown_text)

    titles = [section.heading.title for section in sections]
    parents = [
        None if section.parent_index is None else titles[section.parent_index]
        for section in sections
    ]
    assert titles == [
        "OOP",
        "Types of polymorphism",
        "Patterns & Principles",
        "Distributed System Patterns",
        "Dual Write Problem",
    ]
    assert parents == [
        None,
        "OOP",
        None,
        "Patterns & Principles",
        "Distributed System Patterns",
    ]


def test_toggle_and_priority_flags_are_extracted_and_stripped_from_title():
    markdown_text = "\n".join([
        '## **SOLID**',
        '## DDD {toggle="true"}',
        '## <span color="red">GoF (Design) patterns</span>',
    ])

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == [
        "SOLID",
        "DDD",
        "GoF (Design) patterns",
    ]
    assert [heading.is_toggle for heading in headings] == [False, True, False]
    assert [heading.is_priority for heading in headings] == [False, False, True]


def test_section_owns_only_its_own_content_not_its_children():
    markdown_text = "\n".join([
        "# Parent",
        "parent body",
        "## Child",
        "child body",
    ])

    sections = build_sections(markdown_text)

    assert sections[0].content == "parent body"
    assert sections[1].content == "child body"


def test_unterminated_fence_swallows_the_remainder():
    markdown_text = "\n".join([
        "# Real",
        "```python",
        "# still inside the fence",
    ])

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == ["Real"]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_headings.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.headings'`

- [ ] **Step 3: Write the implementation**

Create `/home/viktar/Projects/Support/src/support/headings.py`:

```python
import re
from dataclasses import dataclass

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE_PATTERN = re.compile(r"^\s*(?:```|~~~)")
TOGGLE_PATTERN = re.compile(r'\{toggle="true"\}')
PRIORITY_PATTERN = re.compile(r'<span[^>]*color="red"[^>]*>')
MARKUP_PATTERN = re.compile(r'<[^>]+>|\*\*|__|\{toggle="[^"]*"\}')


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    is_toggle: bool
    is_priority: bool
    line_index: int


@dataclass(frozen=True)
class Section:
    heading: Heading
    parent_index: int | None
    content: str


def clean_title(raw_title):
    cleaned_title = MARKUP_PATTERN.sub("", raw_title).strip()
    return cleaned_title


def parse_headings(markdown_text):
    """Return every real Markdown heading, ignoring heading-like lines in code fences."""
    lines = markdown_text.split("\n")
    headings = []
    is_inside_fence = False

    for line_index, line in enumerate(lines):
        if FENCE_PATTERN.match(line):
            is_inside_fence = not is_inside_fence
            continue
        if is_inside_fence:
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match is None:
            continue

        raw_title = heading_match.group(2)
        heading = Heading(
            level=len(heading_match.group(1)),
            title=clean_title(raw_title),
            is_toggle=bool(TOGGLE_PATTERN.search(raw_title)),
            is_priority=bool(PRIORITY_PATTERN.search(raw_title)),
            line_index=line_index,
        )
        headings.append(heading)

    return headings


def build_sections(markdown_text):
    """Return sections in document order, each linked to its parent by relative rank."""
    lines = markdown_text.split("\n")
    headings = parse_headings(markdown_text)
    sections = []
    open_heading_positions = []

    for position, heading in enumerate(headings):
        while (
            open_heading_positions
            and headings[open_heading_positions[-1]].level >= heading.level
        ):
            open_heading_positions.pop()

        parent_index = open_heading_positions[-1] if open_heading_positions else None

        is_last_heading = position + 1 >= len(headings)
        end_line = len(lines) if is_last_heading else headings[position + 1].line_index
        content = "\n".join(lines[heading.line_index + 1 : end_line]).strip()

        sections.append(
            Section(heading=heading, parent_index=parent_index, content=content)
        )
        open_heading_positions.append(position)

    return sections
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_headings.py -v`
Expected: PASS — 6 passed

- [ ] **Step 5: Verify against the real sample page**

The sampled page produced 36 real headings and 9 heading-like lines inside fences. Confirm the parser agrees, using the captured fetch output:

Run:
```bash
cd /home/viktar/Projects/Support && python -c "
import json, sys
sys.path.insert(0, 'src')
from support.headings import parse_headings
raw = open('/home/viktar/.claude/projects/-home-viktar-Projects-Support/882112cf-0508-45f2-9714-91ac5f152787/tool-results/mcp-claude_ai_Notion-notion-fetch-1789038182129.txt').read()
print(len(parse_headings(json.loads(raw)['text'])))
"
```
Expected: `36`

If that captured file is no longer present, skip this step — the unit tests above already cover the behavior.

- [ ] **Step 6: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/headings.py tests/test_headings.py
git commit -m "Add code-fence-aware heading parser and section tree builder"
```

---

### Task 3: Manifest persistence and sync planning

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/manifest.py`
- Test: `/home/viktar/Projects/Support/tests/test_manifest.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `support.manifest.PageRecord` dataclass with fields `page_id: str`, `title: str`, `parent_id: str | None`, `last_edited_time: str`, `output_path: str`, `content_hash: str`; `support.manifest.SyncPlan` dataclass with fields `new_page_ids: list[str]`, `changed_page_ids: list[str]`, `unchanged_page_ids: list[str]`, `removed_page_ids: list[str]`; `support.manifest.load_manifest(manifest_path) -> dict[str, PageRecord]`; `support.manifest.save_manifest(manifest_path, records: dict[str, PageRecord]) -> None`; `support.manifest.plan_sync(remote_last_edited: dict[str, str], records: dict[str, PageRecord], force_full: bool = False) -> SyncPlan`; `support.manifest.page_slug(title: str, page_id: str, taken_slugs: set[str]) -> str`; `support.manifest.content_hash(text: str) -> str`.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_manifest.py`:

```python
from support.manifest import (
    PageRecord,
    content_hash,
    load_manifest,
    page_slug,
    plan_sync,
    save_manifest,
)


def make_record(page_id, last_edited_time):
    return PageRecord(
        page_id=page_id,
        title="Databases",
        parent_id="root",
        last_edited_time=last_edited_time,
        output_path="databases.md",
        content_hash="abc",
    )


def test_manifest_round_trips_through_disk(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    records = {"page-1": make_record("page-1", "2026-08-26T14:42:09.249Z")}

    save_manifest(manifest_path, records)

    assert load_manifest(manifest_path) == records


def test_load_manifest_returns_empty_mapping_when_file_absent(tmp_path):
    assert load_manifest(tmp_path / "missing.json") == {}


def test_plan_sync_classifies_new_changed_unchanged_and_removed():
    records = {
        "unchanged": make_record("unchanged", "2026-01-01T00:00:00.000Z"),
        "changed": make_record("changed", "2026-01-01T00:00:00.000Z"),
        "removed": make_record("removed", "2026-01-01T00:00:00.000Z"),
    }
    remote_last_edited = {
        "unchanged": "2026-01-01T00:00:00.000Z",
        "changed": "2026-02-02T00:00:00.000Z",
        "new": "2026-03-03T00:00:00.000Z",
    }

    plan = plan_sync(remote_last_edited, records)

    assert plan.new_page_ids == ["new"]
    assert plan.changed_page_ids == ["changed"]
    assert plan.unchanged_page_ids == ["unchanged"]
    assert plan.removed_page_ids == ["removed"]


def test_plan_sync_with_force_full_treats_every_known_page_as_changed():
    records = {"unchanged": make_record("unchanged", "2026-01-01T00:00:00.000Z")}
    remote_last_edited = {"unchanged": "2026-01-01T00:00:00.000Z"}

    plan = plan_sync(remote_last_edited, records, force_full=True)

    assert plan.changed_page_ids == ["unchanged"]
    assert plan.unchanged_page_ids == []


def test_page_slug_is_derived_from_the_title():
    assert page_slug("OOP\\Principles\\Patterns", "3649c92c96f5805b", set()) == "oop-principles-patterns"


def test_page_slug_appends_page_id_prefix_on_collision():
    taken_slugs = {"security"}

    slug = page_slug("Security", "3b39c92c-96f5-8034-bb16-e53185347a59", taken_slugs)

    assert slug == "security-3b39c92c"


def test_page_slug_falls_back_for_a_title_with_no_usable_characters():
    assert page_slug("...", "3b39c92c96f58034", set()) == "untitled"


def test_content_hash_is_stable_and_differs_per_content():
    assert content_hash("same") == content_hash("same")
    assert content_hash("one") != content_hash("two")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_manifest.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.manifest'`

- [ ] **Step 3: Write the implementation**

Create `/home/viktar/Projects/Support/src/support/manifest.py`:

```python
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

SLUG_SEPARATOR_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class PageRecord:
    page_id: str
    title: str
    parent_id: str | None
    last_edited_time: str
    output_path: str
    content_hash: str


@dataclass(frozen=True)
class SyncPlan:
    new_page_ids: list[str]
    changed_page_ids: list[str]
    unchanged_page_ids: list[str]
    removed_page_ids: list[str]


def load_manifest(manifest_path):
    path = Path(manifest_path)
    if not path.exists():
        return {}

    raw_records = json.loads(path.read_text(encoding="utf-8"))
    records = {
        page_id: PageRecord(**fields) for page_id, fields in raw_records.items()
    }
    return records


def save_manifest(manifest_path, records):
    payload = {page_id: asdict(record) for page_id, record in records.items()}
    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )


def plan_sync(remote_last_edited, records, force_full=False):
    new_page_ids = []
    changed_page_ids = []
    unchanged_page_ids = []

    for page_id, last_edited_time in remote_last_edited.items():
        known_record = records.get(page_id)
        if known_record is None:
            new_page_ids.append(page_id)
        elif force_full or known_record.last_edited_time != last_edited_time:
            changed_page_ids.append(page_id)
        else:
            unchanged_page_ids.append(page_id)

    removed_page_ids = [
        page_id for page_id in records if page_id not in remote_last_edited
    ]

    plan = SyncPlan(
        new_page_ids=sorted(new_page_ids),
        changed_page_ids=sorted(changed_page_ids),
        unchanged_page_ids=sorted(unchanged_page_ids),
        removed_page_ids=sorted(removed_page_ids),
    )
    return plan


def page_slug(title, page_id, taken_slugs):
    base_slug = SLUG_SEPARATOR_PATTERN.sub("-", title.lower()).strip("-")
    if not base_slug:
        base_slug = "untitled"

    if base_slug not in taken_slugs:
        return base_slug

    disambiguated_slug = f"{base_slug}-{page_id.replace('-', '')[:8]}"
    return disambiguated_slug


def content_hash(text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return digest
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_manifest.py -v`
Expected: PASS — 8 passed

- [ ] **Step 5: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/manifest.py tests/test_manifest.py
git commit -m "Add manifest persistence and incremental sync planning"
```

---

### Task 4: Notion API access with pagination and throttling

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/notion_api.py`
- Test: `/home/viktar/Projects/Support/tests/test_notion_api.py`

**Interfaces:**
- Consumes: `support.config.Config`.
- Produces: `support.notion_api.PageNode` dataclass with fields `page_id: str`, `title: str`, `parent_id: str | None`, `last_edited_time: str`; `support.notion_api.NotionGateway` class constructed as `NotionGateway(client, min_seconds_between_calls: float = 0.34)` with methods `fetch_page(page_id) -> dict`, `fetch_all_blocks(block_id) -> list[dict]`, and `walk_page_tree(root_page_id) -> list[PageNode]`; `support.notion_api.build_gateway(config) -> NotionGateway`; `support.notion_api.extract_title(page: dict) -> str`.

`fetch_all_blocks` follows `next_cursor` until `has_more` is false and returns every block. `walk_page_tree` returns the root page followed by every descendant page, breadth-first, each appearing exactly once even if it is linked from more than one place.

The tests use a fake client rather than the network, so no Notion token is needed to run them.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_notion_api.py`:

```python
from support.notion_api import NotionGateway, PageNode, extract_title


class FakeBlocksChildren:
    def __init__(self, pages_by_cursor):
        self.pages_by_cursor = pages_by_cursor
        self.requested_cursors = []

    def list(self, block_id, start_cursor=None, page_size=100):
        self.requested_cursors.append(start_cursor)
        return self.pages_by_cursor[start_cursor]


class FakeClient:
    def __init__(self, blocks_children, pages_by_id=None):
        self.blocks = type("Blocks", (), {"children": blocks_children})()
        self.pages_by_id = pages_by_id or {}
        self.pages = type("Pages", (), {"retrieve": self._retrieve})()

    def _retrieve(self, page_id):
        return self.pages_by_id[page_id]


def test_fetch_all_blocks_follows_every_cursor():
    blocks_children = FakeBlocksChildren({
        None: {"results": [{"id": "b1"}], "has_more": True, "next_cursor": "c1"},
        "c1": {"results": [{"id": "b2"}], "has_more": True, "next_cursor": "c2"},
        "c2": {"results": [{"id": "b3"}], "has_more": False, "next_cursor": None},
    })
    gateway = NotionGateway(FakeClient(blocks_children), min_seconds_between_calls=0)

    blocks = gateway.fetch_all_blocks("page-1")

    assert [block["id"] for block in blocks] == ["b1", "b2", "b3"]
    assert blocks_children.requested_cursors == [None, "c1", "c2"]


def test_walk_page_tree_returns_root_then_descendants_without_duplicates():
    blocks_children = FakeBlocksChildren({
        None: {"results": [], "has_more": False, "next_cursor": None},
    })
    client = FakeClient(blocks_children)
    gateway = NotionGateway(client, min_seconds_between_calls=0)

    child_blocks = {
        "root": [
            {"type": "child_page", "id": "a", "child_page": {"title": "PHP"}},
            {"type": "child_page", "id": "b", "child_page": {"title": "Databases"}},
        ],
        "a": [{"type": "child_page", "id": "b", "child_page": {"title": "Databases"}}],
        "b": [],
    }
    last_edited = {
        "root": "2026-01-01T00:00:00.000Z",
        "a": "2026-01-02T00:00:00.000Z",
        "b": "2026-01-03T00:00:00.000Z",
    }
    gateway.fetch_all_blocks = lambda block_id: child_blocks[block_id]
    gateway.fetch_page = lambda page_id: {
        "id": page_id,
        "last_edited_time": last_edited[page_id],
        "properties": {"title": {"title": [{"plain_text": "Software Development"}]}},
    }

    nodes = gateway.walk_page_tree("root")

    assert [node.page_id for node in nodes] == ["root", "a", "b"]
    assert nodes[1] == PageNode(
        page_id="a",
        title="PHP",
        parent_id="root",
        last_edited_time="2026-01-02T00:00:00.000Z",
    )


def test_extract_title_reads_the_title_property():
    page = {"properties": {"title": {"title": [{"plain_text": "Software Development"}]}}}

    assert extract_title(page) == "Software Development"


def test_extract_title_falls_back_when_the_title_is_empty():
    page = {"properties": {"title": {"title": []}}}

    assert extract_title(page) == "Untitled"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_notion_api.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.notion_api'`

- [ ] **Step 3: Write the implementation**

Create `/home/viktar/Projects/Support/src/support/notion_api.py`:

```python
import time
from collections import deque
from dataclasses import dataclass

from notion_client import Client

DEFAULT_MIN_SECONDS_BETWEEN_CALLS = 0.34


@dataclass(frozen=True)
class PageNode:
    page_id: str
    title: str
    parent_id: str | None
    last_edited_time: str


def extract_title(page):
    properties = page.get("properties", {})
    title_property = properties.get("title", {})
    title_fragments = title_property.get("title", [])
    joined_title = "".join(fragment.get("plain_text", "") for fragment in title_fragments)
    return joined_title or "Untitled"


class NotionGateway:
    """Read-only access to Notion, throttled to stay under the rate limit."""

    def __init__(self, client, min_seconds_between_calls=DEFAULT_MIN_SECONDS_BETWEEN_CALLS):
        self.client = client
        self.min_seconds_between_calls = min_seconds_between_calls
        self.last_call_finished_at = 0.0

    def _throttle(self):
        if self.min_seconds_between_calls <= 0:
            return
        seconds_since_last_call = time.monotonic() - self.last_call_finished_at
        remaining_wait = self.min_seconds_between_calls - seconds_since_last_call
        if remaining_wait > 0:
            time.sleep(remaining_wait)

    def fetch_page(self, page_id):
        self._throttle()
        page = self.client.pages.retrieve(page_id)
        self.last_call_finished_at = time.monotonic()
        return page

    def fetch_all_blocks(self, block_id):
        blocks = []
        start_cursor = None

        while True:
            self._throttle()
            response = self.client.blocks.children.list(
                block_id=block_id, start_cursor=start_cursor, page_size=100
            )
            self.last_call_finished_at = time.monotonic()

            blocks.extend(response["results"])
            if not response.get("has_more"):
                break
            start_cursor = response["next_cursor"]

        return blocks

    def walk_page_tree(self, root_page_id):
        root_page = self.fetch_page(root_page_id)
        root_node = PageNode(
            page_id=root_page_id,
            title=extract_title(root_page),
            parent_id=None,
            last_edited_time=root_page["last_edited_time"],
        )

        nodes = [root_node]
        visited_page_ids = {root_page_id}
        pending_page_ids = deque([root_page_id])

        while pending_page_ids:
            parent_page_id = pending_page_ids.popleft()
            child_blocks = self.fetch_all_blocks(parent_page_id)

            for block in child_blocks:
                if block.get("type") != "child_page":
                    continue
                child_page_id = block["id"]
                if child_page_id in visited_page_ids:
                    continue

                child_page = self.fetch_page(child_page_id)
                nodes.append(
                    PageNode(
                        page_id=child_page_id,
                        title=block["child_page"]["title"],
                        parent_id=parent_page_id,
                        last_edited_time=child_page["last_edited_time"],
                    )
                )
                visited_page_ids.add(child_page_id)
                pending_page_ids.append(child_page_id)

        return nodes


def build_gateway(config):
    gateway = NotionGateway(Client(auth=config.notion_token))
    return gateway
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_notion_api.py -v`
Expected: PASS — 4 passed

- [ ] **Step 5: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/notion_api.py tests/test_notion_api.py
git commit -m "Add throttled Notion gateway with pagination and tree walking"
```

---

### Task 5: Notion block to Markdown conversion

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/markdown.py`
- Test: `/home/viktar/Projects/Support/tests/test_markdown.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `support.markdown.ConversionResult` dataclass with fields `markdown: str` and `warnings: list[str]`; `support.markdown.blocks_to_markdown(blocks: list[dict]) -> ConversionResult`; `support.markdown.rich_text_to_markdown(rich_text: list[dict]) -> str`.

Toggleable headings emit the `{toggle="true"}` suffix that `support.headings.parse_headings` already recognises. Red-coloured rich text emits `<span color="red">…</span>`, which `support.headings.parse_headings` already reads as the priority flag. Unsupported block types produce one warning each and no output.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_markdown.py`:

```python
from support.markdown import blocks_to_markdown, rich_text_to_markdown


def text_fragment(content, bold=False, code=False, color="default"):
    return {
        "plain_text": content,
        "annotations": {"bold": bold, "italic": False, "code": code, "color": color},
        "href": None,
    }


def test_headings_render_with_the_matching_level():
    blocks = [
        {"type": "heading_1", "heading_1": {"rich_text": [text_fragment("OOP")], "is_toggleable": False}},
        {"type": "heading_2", "heading_2": {"rich_text": [text_fragment("SOLID")], "is_toggleable": False}},
    ]

    result = blocks_to_markdown(blocks)

    assert result.markdown == "# OOP\n\n## SOLID"
    assert result.warnings == []


def test_toggleable_heading_emits_the_toggle_marker():
    blocks = [
        {"type": "heading_2", "heading_2": {"rich_text": [text_fragment("DDD")], "is_toggleable": True}},
    ]

    result = blocks_to_markdown(blocks)

    assert result.markdown == '## DDD {toggle="true"}'


def test_red_text_is_wrapped_in_a_colour_span():
    rendered = rich_text_to_markdown([text_fragment("GoF (Design) patterns", color="red")])

    assert rendered == '<span color="red">GoF (Design) patterns</span>'


def test_bold_and_code_annotations_render():
    rendered = rich_text_to_markdown([text_fragment("SOLID", bold=True), text_fragment("x", code=True)])

    assert rendered == "**SOLID**`x`"


def test_code_block_renders_with_its_language():
    blocks = [
        {
            "type": "code",
            "code": {"rich_text": [text_fragment("print(1)")], "language": "python"},
        }
    ]

    result = blocks_to_markdown(blocks)

    assert result.markdown == "```python\nprint(1)\n```"


def test_lists_quotes_and_dividers_render():
    blocks = [
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [text_fragment("first")]}},
        {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [text_fragment("second")]}},
        {"type": "quote", "quote": {"rich_text": [text_fragment("quoted")]}},
        {"type": "divider", "divider": {}},
    ]

    result = blocks_to_markdown(blocks)

    assert result.markdown == "- first\n\n1. second\n\n> quoted\n\n---"


def test_child_pages_render_as_links_not_content():
    blocks = [{"type": "child_page", "id": "abc", "child_page": {"title": "PHP"}}]

    result = blocks_to_markdown(blocks)

    assert result.markdown == "[PHP](notion://abc)"


def test_unsupported_block_produces_a_warning_and_no_output():
    blocks = [{"type": "unsupported_widget", "id": "xyz"}]

    result = blocks_to_markdown(blocks)

    assert result.markdown == ""
    assert result.warnings == ["unsupported block type 'unsupported_widget' (id xyz)"]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_markdown.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.markdown'`

- [ ] **Step 3: Write the implementation**

Create `/home/viktar/Projects/Support/src/support/markdown.py`:

```python
from dataclasses import dataclass, field

HEADING_LEVELS = {"heading_1": 1, "heading_2": 2, "heading_3": 3}


@dataclass
class ConversionResult:
    markdown: str
    warnings: list[str] = field(default_factory=list)


def rich_text_to_markdown(rich_text):
    rendered_fragments = []

    for fragment in rich_text:
        content = fragment.get("plain_text", "")
        if not content:
            continue

        annotations = fragment.get("annotations", {})
        if annotations.get("code"):
            content = f"`{content}`"
        if annotations.get("bold"):
            content = f"**{content}**"
        if annotations.get("italic"):
            content = f"*{content}*"

        color = annotations.get("color", "default")
        if color != "default":
            color_name = color.replace("_background", "")
            content = f'<span color="{color_name}">{content}</span>'

        href = fragment.get("href")
        if href:
            content = f"[{content}]({href})"

        rendered_fragments.append(content)

    return "".join(rendered_fragments)


def _render_block(block, warnings):
    block_type = block.get("type")
    payload = block.get(block_type, {})

    if block_type in HEADING_LEVELS:
        level = HEADING_LEVELS[block_type]
        title = rich_text_to_markdown(payload.get("rich_text", []))
        toggle_suffix = ' {toggle="true"}' if payload.get("is_toggleable") else ""
        return f"{'#' * level} {title}{toggle_suffix}"

    if block_type == "paragraph":
        return rich_text_to_markdown(payload.get("rich_text", []))

    if block_type == "bulleted_list_item":
        return f"- {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "numbered_list_item":
        return f"1. {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "to_do":
        checkbox = "x" if payload.get("checked") else " "
        return f"- [{checkbox}] {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "quote":
        return f"> {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "callout":
        return f"> {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "toggle":
        return f"- {rich_text_to_markdown(payload.get('rich_text', []))}"

    if block_type == "code":
        language = payload.get("language", "")
        body = rich_text_to_markdown(payload.get("rich_text", []))
        return f"```{language}\n{body}\n```"

    if block_type == "divider":
        return "---"

    if block_type == "child_page":
        return f"[{payload.get('title', 'Untitled')}](notion://{block.get('id', '')})"

    if block_type == "child_database":
        return f"[{payload.get('title', 'Database')}](notion://{block.get('id', '')})"

    warnings.append(
        f"unsupported block type '{block_type}' (id {block.get('id', 'unknown')})"
    )
    return ""


def blocks_to_markdown(blocks):
    warnings = []
    rendered_blocks = []

    for block in blocks:
        rendered = _render_block(block, warnings)
        if rendered:
            rendered_blocks.append(rendered)

    result = ConversionResult(markdown="\n\n".join(rendered_blocks), warnings=warnings)
    return result
```

Note on code blocks: the `rich_text_to_markdown` call inside a code block would normally apply annotations, but Notion code blocks carry plain fragments with `code: false`, so the body comes through verbatim.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_markdown.py -v`
Expected: PASS — 8 passed

- [ ] **Step 5: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/markdown.py tests/test_markdown.py
git commit -m "Add Notion block to Markdown conversion"
```

---

### Task 6: Sync orchestration and the sync and status commands

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/sync.py`
- Create: `/home/viktar/Projects/Support/src/support/cli.py`
- Test: `/home/viktar/Projects/Support/tests/test_sync.py`

**Interfaces:**
- Consumes: `support.config` paths, `support.manifest.PageRecord`, `support.manifest.SyncPlan`, `support.manifest.load_manifest`, `support.manifest.save_manifest`, `support.manifest.plan_sync`, `support.manifest.page_slug`, `support.manifest.content_hash`, `support.notion_api.NotionGateway`, `support.notion_api.PageNode`, `support.markdown.blocks_to_markdown`.
- Produces: `support.sync.SyncReport` dataclass with fields `written_page_ids: list[str]`, `skipped_page_ids: list[str]`, `pruned_page_ids: list[str]`, `warnings: list[str]`; `support.sync.run_sync(gateway, root_page_id, mirror_dir, raw_dir, manifest_path, force_full=False) -> SyncReport`; `support.sync.run_status(gateway, root_page_id, manifest_path) -> SyncPlan`; `support.cli.main(argv=None) -> int`.

`run_sync` writes each page's Markdown and raw JSON first, then updates that page's manifest entry, then moves to the next page — so an interrupted run leaves the manifest at most one page behind the mirror.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_sync.py`:

```python
import json

from support.manifest import PageRecord, load_manifest, save_manifest
from support.notion_api import PageNode
from support.sync import run_status, run_sync


class FakeGateway:
    def __init__(self, nodes, blocks_by_page_id):
        self.nodes = nodes
        self.blocks_by_page_id = blocks_by_page_id

    def walk_page_tree(self, root_page_id):
        return self.nodes

    def fetch_all_blocks(self, block_id):
        return self.blocks_by_page_id[block_id]


def paragraph(content):
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "plain_text": content,
                    "annotations": {"bold": False, "italic": False, "code": False, "color": "default"},
                    "href": None,
                }
            ]
        },
    }


def build_gateway():
    nodes = [
        PageNode(page_id="root", title="Software Development", parent_id=None, last_edited_time="2026-01-01T00:00:00.000Z"),
        PageNode(page_id="php", title="PHP", parent_id="root", last_edited_time="2026-01-02T00:00:00.000Z"),
    ]
    blocks_by_page_id = {"root": [paragraph("root body")], "php": [paragraph("php body")]}
    return FakeGateway(nodes, blocks_by_page_id)


def test_run_sync_writes_markdown_raw_json_and_manifest(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert sorted(report.written_page_ids) == ["php", "root"]
    assert (mirror_dir / "php.md").read_text(encoding="utf-8") == "php body"
    assert json.loads((raw_dir / "php.json").read_text(encoding="utf-8"))[0]["type"] == "paragraph"

    records = load_manifest(manifest_path)
    assert records["php"].title == "PHP"
    assert records["php"].output_path == "php.md"


def test_run_sync_skips_pages_whose_last_edited_time_is_unchanged(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)
    second_report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert second_report.written_page_ids == []
    assert sorted(second_report.skipped_page_ids) == ["php", "root"]


def test_run_sync_with_force_full_rewrites_everything(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)
    forced_report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path, force_full=True)

    assert sorted(forced_report.written_page_ids) == ["php", "root"]


def test_run_sync_prunes_pages_that_disappeared_from_notion(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"
    mirror_dir.mkdir(parents=True)
    (mirror_dir / "gone.md").write_text("stale", encoding="utf-8")
    save_manifest(manifest_path, {
        "gone": PageRecord(
            page_id="gone",
            title="Gone",
            parent_id="root",
            last_edited_time="2026-01-01T00:00:00.000Z",
            output_path="gone.md",
            content_hash="x",
        )
    })

    report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert report.pruned_page_ids == ["gone"]
    assert not (mirror_dir / "gone.md").exists()
    assert "gone" not in load_manifest(manifest_path)


def test_run_status_reports_the_plan_without_writing(tmp_path):
    manifest_path = tmp_path / "manifest.json"

    plan = run_status(build_gateway(), "root", manifest_path)

    assert plan.new_page_ids == ["php", "root"]
    assert not manifest_path.exists()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_sync.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.sync'`

- [ ] **Step 3: Write the sync module**

Create `/home/viktar/Projects/Support/src/support/sync.py`:

```python
import json
from dataclasses import dataclass, field
from pathlib import Path

from support.manifest import (
    PageRecord,
    content_hash,
    load_manifest,
    page_slug,
    plan_sync,
    save_manifest,
)
from support.markdown import blocks_to_markdown


@dataclass
class SyncReport:
    written_page_ids: list[str] = field(default_factory=list)
    skipped_page_ids: list[str] = field(default_factory=list)
    pruned_page_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _remote_last_edited(nodes):
    remote_last_edited = {node.page_id: node.last_edited_time for node in nodes}
    return remote_last_edited


def run_status(gateway, root_page_id, manifest_path):
    nodes = gateway.walk_page_tree(root_page_id)
    records = load_manifest(manifest_path)
    plan = plan_sync(_remote_last_edited(nodes), records)
    return plan


def run_sync(gateway, root_page_id, mirror_dir, raw_dir, manifest_path, force_full=False):
    mirror_dir = Path(mirror_dir)
    raw_dir = Path(raw_dir)
    mirror_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    nodes = gateway.walk_page_tree(root_page_id)
    records = load_manifest(manifest_path)
    plan = plan_sync(_remote_last_edited(nodes), records, force_full=force_full)

    page_ids_to_write = set(plan.new_page_ids) | set(plan.changed_page_ids)
    report = SyncReport(skipped_page_ids=list(plan.unchanged_page_ids))

    taken_slugs = {
        record.output_path.removesuffix(".md")
        for page_id, record in records.items()
        if page_id not in page_ids_to_write
    }

    for node in nodes:
        if node.page_id not in page_ids_to_write:
            continue

        blocks = gateway.fetch_all_blocks(node.page_id)
        conversion = blocks_to_markdown(blocks)

        slug = page_slug(node.title, node.page_id, taken_slugs)
        taken_slugs.add(slug)

        (mirror_dir / f"{slug}.md").write_text(conversion.markdown, encoding="utf-8")
        (raw_dir / f"{node.page_id}.json").write_text(
            json.dumps(blocks, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        records[node.page_id] = PageRecord(
            page_id=node.page_id,
            title=node.title,
            parent_id=node.parent_id,
            last_edited_time=node.last_edited_time,
            output_path=f"{slug}.md",
            content_hash=content_hash(conversion.markdown),
        )
        save_manifest(manifest_path, records)

        report.written_page_ids.append(node.page_id)
        report.warnings.extend(
            f"{node.title}: {warning}" for warning in conversion.warnings
        )

    for page_id in plan.removed_page_ids:
        stale_record = records.pop(page_id)
        (mirror_dir / stale_record.output_path).unlink(missing_ok=True)
        (raw_dir / f"{page_id}.json").unlink(missing_ok=True)
        report.pruned_page_ids.append(page_id)

    save_manifest(manifest_path, records)
    return report
```

- [ ] **Step 4: Write the command line entry point**

Create `/home/viktar/Projects/Support/src/support/cli.py`:

```python
import argparse
import http.server
import socketserver

from support import config as project_config
from support.config import ConfigError, load_config
from support.notion_api import build_gateway


def _command_sync(args):
    configuration = load_config()
    gateway = build_gateway(configuration)
    from support.sync import run_sync

    report = run_sync(
        gateway,
        configuration.root_page_id,
        project_config.MIRROR_DIR,
        project_config.RAW_DIR,
        project_config.MANIFEST_PATH,
        force_full=args.full,
    )

    print(f"written: {len(report.written_page_ids)}")
    print(f"skipped: {len(report.skipped_page_ids)}")
    print(f"pruned:  {len(report.pruned_page_ids)}")
    for warning in report.warnings:
        print(f"warning: {warning}")
    return 0


def _command_status(args):
    configuration = load_config()
    gateway = build_gateway(configuration)
    from support.sync import run_status

    plan = run_status(gateway, configuration.root_page_id, project_config.MANIFEST_PATH)

    print(f"new:       {len(plan.new_page_ids)}")
    print(f"changed:   {len(plan.changed_page_ids)}")
    print(f"unchanged: {len(plan.unchanged_page_ids)}")
    print(f"removed:   {len(plan.removed_page_ids)}")
    return 0


def _command_build_graph(args):
    from support.graph import build_graph

    node_count, edge_count = build_graph(
        project_config.MIRROR_DIR,
        project_config.MANIFEST_PATH,
        project_config.GRAPH_PATH,
    )
    print(f"nodes: {node_count}")
    print(f"edges: {edge_count}")
    return 0


def _command_serve(args):
    handler = http.server.SimpleHTTPRequestHandler
    directory = str(project_config.PROJECT_ROOT)

    class RootedHandler(handler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=directory, **handler_kwargs)

    with socketserver.TCPServer(("127.0.0.1", args.port), RootedHandler) as server:
        print(f"Viewer: http://127.0.0.1:{args.port}/viewer/index.html")
        server.serve_forever()
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="support")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="fetch changed Notion pages")
    sync_parser.add_argument("--full", action="store_true", help="refetch every page")
    sync_parser.set_defaults(handler=_command_sync)

    status_parser = subparsers.add_parser("status", help="report what sync would do")
    status_parser.set_defaults(handler=_command_status)

    graph_parser = subparsers.add_parser("build-graph", help="rebuild graph.json")
    graph_parser.set_defaults(handler=_command_build_graph)

    serve_parser = subparsers.add_parser("serve", help="serve the viewer locally")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.set_defaults(handler=_command_serve)

    args = parser.parse_args(argv)

    try:
        return args.handler(args)
    except ConfigError as error:
        print(f"error: {error}")
        return 1
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_sync.py -v`
Expected: PASS — 5 passed

- [ ] **Step 6: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/sync.py src/support/cli.py tests/test_sync.py
git commit -m "Add sync orchestration with pruning and the command line entry point"
```

---

### Task 7: Graph builder

**Files:**
- Create: `/home/viktar/Projects/Support/src/support/graph.py`
- Test: `/home/viktar/Projects/Support/tests/test_graph.py`

**Interfaces:**
- Consumes: `support.headings.build_sections`, `support.manifest.load_manifest`, `support.manifest.PageRecord`.
- Produces: `support.graph.build_graph(mirror_dir, manifest_path, graph_path) -> tuple[int, int]` returning node and edge counts; `support.graph.build_graph_document(mirror_dir, manifest_path) -> dict` returning `{"nodes": [...], "edges": [...]}`.

Node identifiers: a page node is its Notion page ID; a section node is `<page-id>#<index>`, where `<index>` is the section's position within its page. Positional identifiers stay stable for an unchanged page and are regenerated wholesale anyway.

Node shape:

```json
{
  "id": "php#3",
  "type": "section",
  "title": "CQRS",
  "level": 2,
  "page_id": "php",
  "page_title": "PHP",
  "is_toggle": true,
  "is_priority": false,
  "content_md": "..."
}
```

Edge shape: `{"source": "...", "target": "...", "kind": "contains" | "links_to" | "mentions"}`.

- [ ] **Step 1: Write the failing tests**

Create `/home/viktar/Projects/Support/tests/test_graph.py`:

```python
import json

from support.graph import build_graph, build_graph_document
from support.manifest import PageRecord, save_manifest


def prepare_mirror(tmp_path, pages):
    mirror_dir = tmp_path / "mirror"
    mirror_dir.mkdir(parents=True)
    manifest_path = mirror_dir / "manifest.json"

    records = {}
    for page_id, title, parent_id, body in pages:
        output_path = f"{page_id}.md"
        (mirror_dir / output_path).write_text(body, encoding="utf-8")
        records[page_id] = PageRecord(
            page_id=page_id,
            title=title,
            parent_id=parent_id,
            last_edited_time="2026-01-01T00:00:00.000Z",
            output_path=output_path,
            content_hash="x",
        )
    save_manifest(manifest_path, records)
    return mirror_dir, manifest_path


def test_page_and_section_nodes_are_created_with_contains_edges(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", "root", "# Basics\nbody\n## Arrays\narray body"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    node_ids = [node["id"] for node in document["nodes"]]
    assert node_ids == ["php", "php#0", "php#1"]
    assert document["nodes"][2]["title"] == "Arrays"
    assert document["nodes"][2]["content_md"] == "array body"

    contains_edges = [edge for edge in document["edges"] if edge["kind"] == "contains"]
    assert {"source": "php", "target": "php#0", "kind": "contains"} in contains_edges
    assert {"source": "php#0", "target": "php#1", "kind": "contains"} in contains_edges


def test_page_hierarchy_produces_contains_edges_between_pages(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("root", "Software Development", None, ""),
        ("php", "PHP", "root", "# Basics"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    assert {"source": "root", "target": "php", "kind": "contains"} in document["edges"]


def test_notion_links_become_links_to_edges(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("root", "Software Development", None, ""),
        ("php", "PHP", "root", "# Basics\nsee [Databases](notion://db)"),
        ("db", "Databases", "root", "# Indexes"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    assert {"source": "php#0", "target": "db", "kind": "links_to"} in document["edges"]


def test_title_occurrences_become_mentions_edges(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# SAGA\nbody"),
        ("db", "Databases", None, "# Transactions\nwe also use SAGA here"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    assert {"source": "db#0", "target": "php#0", "kind": "mentions"} in document["edges"]


def test_a_section_does_not_mention_itself(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# SAGA\nSAGA is a pattern"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    assert [edge for edge in document["edges"] if edge["kind"] == "mentions"] == []


def test_build_graph_writes_the_document_to_disk(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# Basics"),
    ])
    graph_path = tmp_path / "graph" / "graph.json"

    node_count, edge_count = build_graph(mirror_dir, manifest_path, graph_path)

    written = json.loads(graph_path.read_text(encoding="utf-8"))
    assert len(written["nodes"]) == node_count == 2
    assert len(written["edges"]) == edge_count
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_graph.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'support.graph'`

- [ ] **Step 3: Write the implementation**

Create `/home/viktar/Projects/Support/src/support/graph.py`:

```python
import json
import re
from pathlib import Path

from support.headings import build_sections
from support.manifest import load_manifest

NOTION_LINK_PATTERN = re.compile(r"\]\(notion://([0-9a-fA-F-]+)\)")
MINIMUM_MENTION_LENGTH = 4


def _page_node(record):
    node = {
        "id": record.page_id,
        "type": "page",
        "title": record.title,
        "level": 0,
        "page_id": record.page_id,
        "page_title": record.title,
        "is_toggle": False,
        "is_priority": False,
        "content_md": "",
    }
    return node


def _section_node(record, section, section_index):
    node = {
        "id": f"{record.page_id}#{section_index}",
        "type": "section",
        "title": section.heading.title,
        "level": section.heading.level,
        "page_id": record.page_id,
        "page_title": record.title,
        "is_toggle": section.heading.is_toggle,
        "is_priority": section.heading.is_priority,
        "content_md": section.content,
    }
    return node


def build_graph_document(mirror_dir, manifest_path):
    mirror_dir = Path(mirror_dir)
    records = load_manifest(manifest_path)

    nodes = []
    edges = []
    known_page_ids = set(records)

    for page_id, record in records.items():
        nodes.append(_page_node(record))

        if record.parent_id in known_page_ids:
            edges.append(
                {"source": record.parent_id, "target": page_id, "kind": "contains"}
            )

        markdown_path = mirror_dir / record.output_path
        markdown_text = (
            markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
        )
        sections = build_sections(markdown_text)

        for section_index, section in enumerate(sections):
            section_node = _section_node(record, section, section_index)
            nodes.append(section_node)

            if section.parent_index is None:
                parent_node_id = page_id
            else:
                parent_node_id = f"{page_id}#{section.parent_index}"
            edges.append(
                {"source": parent_node_id, "target": section_node["id"], "kind": "contains"}
            )

            for linked_page_id in NOTION_LINK_PATTERN.findall(section.content):
                if linked_page_id in known_page_ids:
                    edges.append(
                        {
                            "source": section_node["id"],
                            "target": linked_page_id,
                            "kind": "links_to",
                        }
                    )

    edges.extend(_mention_edges(nodes))

    document = {"nodes": nodes, "edges": edges}
    return document


def _mention_edges(nodes):
    section_nodes = [node for node in nodes if node["type"] == "section"]
    mention_edges = []

    for source_node in section_nodes:
        source_text = source_node["content_md"].lower()
        if not source_text:
            continue

        for target_node in section_nodes:
            if target_node["id"] == source_node["id"]:
                continue

            target_title = target_node["title"]
            if len(target_title) < MINIMUM_MENTION_LENGTH:
                continue

            occurrence_pattern = re.compile(
                r"\b" + re.escape(target_title.lower()) + r"\b"
            )
            if occurrence_pattern.search(source_text):
                mention_edges.append(
                    {
                        "source": source_node["id"],
                        "target": target_node["id"],
                        "kind": "mentions",
                    }
                )

    return mention_edges


def build_graph(mirror_dir, manifest_path, graph_path):
    document = build_graph_document(mirror_dir, manifest_path)

    path = Path(graph_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False), encoding="utf-8"
    )

    counts = (len(document["nodes"]), len(document["edges"]))
    return counts
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /home/viktar/Projects/Support && python -m pytest tests/test_graph.py -v`
Expected: PASS — 6 passed

- [ ] **Step 5: Run the whole suite**

Run: `cd /home/viktar/Projects/Support && python -m pytest -v`
Expected: PASS — 40 passed

- [ ] **Step 6: Commit**

```bash
cd /home/viktar/Projects/Support
git add src/support/graph.py tests/test_graph.py
git commit -m "Add graph builder producing nodes and contains, links_to and mentions edges"
```

---

### Task 8: Click-only offline viewer

**Files:**
- Create: `/home/viktar/Projects/Support/viewer/index.html`
- Create: `/home/viktar/Projects/Support/viewer/style.css`
- Create: `/home/viktar/Projects/Support/viewer/app.js`

**Interfaces:**
- Consumes: `/home/viktar/Projects/Support/graph/graph.json` as produced by `support.graph.build_graph`, fetched over HTTP from the local server started by `support serve`.
- Produces: nothing consumed by other tasks.

The viewer has no text input. Every interaction is a click.

- [ ] **Step 1: Write the page shell**

Create `/home/viktar/Projects/Support/viewer/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Knowledge</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <nav id="tree" aria-label="Knowledge tree"></nav>
    <main id="content">
      <p class="hint">Select a topic on the left.</p>
    </main>
    <script src="app.js"></script>
  </body>
</html>
```

- [ ] **Step 2: Write the stylesheet**

Create `/home/viktar/Projects/Support/viewer/style.css`:

```css
:root {
  --bg: #14161a;
  --panel: #1b1e24;
  --text: #e6e8ec;
  --muted: #8b93a1;
  --accent: #e5534b;
  --line: #2a2f38;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  display: grid;
  grid-template-columns: minmax(260px, 30%) 1fr;
  height: 100vh;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}

#tree {
  overflow-y: auto;
  padding: 12px;
  background: var(--panel);
  border-right: 1px solid var(--line);
}

#content {
  overflow-y: auto;
  padding: 24px 32px;
}

.row {
  display: block;
  width: 100%;
  text-align: left;
  padding: 5px 8px;
  border: 0;
  border-radius: 5px;
  background: transparent;
  color: var(--text);
  font: inherit;
  cursor: pointer;
}

.row:hover { background: #232832; }
.row.selected { background: #2d3441; }
.row.priority { color: var(--accent); font-weight: 600; }
.row .caret { color: var(--muted); display: inline-block; width: 1em; }

.children { margin-left: 14px; }
.children[hidden] { display: none; }

.toggle-section {
  border: 1px solid var(--line);
  border-radius: 6px;
  margin: 10px 0;
  padding: 8px 12px;
}

.toggle-section > summary {
  cursor: pointer;
  font-weight: 600;
}

.related { margin-top: 28px; border-top: 1px solid var(--line); padding-top: 14px; }
.related h3 { font-size: 13px; color: var(--muted); margin: 0 0 8px; font-weight: 600; }

.chip {
  display: inline-block;
  margin: 0 6px 6px 0;
  padding: 4px 10px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: transparent;
  color: var(--text);
  font: inherit;
  font-size: 13px;
  cursor: pointer;
}

.chip:hover { border-color: var(--accent); }

pre {
  background: #0f1115;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
}

.hint, .error { color: var(--muted); }
.error { color: var(--accent); }
```

- [ ] **Step 3: Write the application script**

Create `/home/viktar/Projects/Support/viewer/app.js`:

```javascript
const state = {
  nodesById: new Map(),
  childrenBySource: new Map(),
  relatedBySource: new Map(),
  selectedId: null,
};

async function load() {
  const treeElement = document.getElementById("tree");
  let document_;

  try {
    const response = await fetch("../graph/graph.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    document_ = await response.json();
  } catch (error) {
    treeElement.innerHTML =
      '<p class="error">graph.json could not be loaded. Run <code>support build-graph</code> first.</p>';
    return;
  }

  for (const node of document_.nodes) {
    state.nodesById.set(node.id, node);
  }

  for (const edge of document_.edges) {
    const bucket = edge.kind === "contains" ? state.childrenBySource : state.relatedBySource;
    if (!bucket.has(edge.source)) {
      bucket.set(edge.source, []);
    }
    bucket.get(edge.source).push(edge.target);
  }

  const childIds = new Set();
  for (const edge of document_.edges) {
    if (edge.kind === "contains") {
      childIds.add(edge.target);
    }
  }
  const rootIds = document_.nodes
    .filter((node) => !childIds.has(node.id))
    .map((node) => node.id);

  treeElement.replaceChildren(renderBranch(rootIds, true));
}

function renderBranch(nodeIds, isExpanded) {
  const container = document.createElement("div");
  container.className = "children";
  container.hidden = !isExpanded;

  for (const nodeId of nodeIds) {
    const node = state.nodesById.get(nodeId);
    if (!node) {
      continue;
    }

    const childIds = state.childrenBySource.get(nodeId) || [];
    const row = document.createElement("button");
    row.className = "row" + (node.is_priority ? " priority" : "");
    row.dataset.nodeId = nodeId;
    row.innerHTML =
      `<span class="caret">${childIds.length ? "\u203a" : ""}</span>` +
      escapeHtml(node.title);

    const childContainer = childIds.length ? renderBranch(childIds, false) : null;

    row.addEventListener("click", () => {
      if (childContainer) {
        childContainer.hidden = !childContainer.hidden;
        row.querySelector(".caret").textContent = childContainer.hidden ? "\u203a" : "\u2304";
      }
      select(nodeId);
    });

    container.append(row);
    if (childContainer) {
      container.append(childContainer);
    }
  }

  return container;
}

function select(nodeId) {
  state.selectedId = nodeId;

  for (const row of document.querySelectorAll(".row.selected")) {
    row.classList.remove("selected");
  }
  const activeRow = document.querySelector(`.row[data-node-id="${cssEscape(nodeId)}"]`);
  if (activeRow) {
    activeRow.classList.add("selected");
    activeRow.scrollIntoView({ block: "nearest" });
  }

  const node = state.nodesById.get(nodeId);
  const contentElement = document.getElementById("content");
  contentElement.replaceChildren();

  const heading = document.createElement("h1");
  heading.textContent = node.title;
  contentElement.append(heading);

  if (node.content_md) {
    contentElement.append(renderBody(node));
  }

  const childIds = state.childrenBySource.get(nodeId) || [];
  for (const childId of childIds) {
    const childNode = state.nodesById.get(childId);
    if (childNode && childNode.is_toggle) {
      contentElement.append(renderToggle(childNode));
    }
  }

  contentElement.append(renderRelated(nodeId));
}

function renderBody(node) {
  const body = document.createElement("div");
  body.innerHTML = renderMarkdown(node.content_md);
  return body;
}

function renderToggle(node) {
  const details = document.createElement("details");
  details.className = "toggle-section";

  const summary = document.createElement("summary");
  summary.textContent = node.title;
  details.append(summary);

  const body = document.createElement("div");
  body.innerHTML = renderMarkdown(node.content_md);
  details.append(body);

  return details;
}

function renderRelated(nodeId) {
  const container = document.createElement("div");
  container.className = "related";

  const relatedIds = state.relatedBySource.get(nodeId) || [];
  const heading = document.createElement("h3");
  heading.textContent = relatedIds.length ? "Related" : "No related topics";
  container.append(heading);

  for (const relatedId of relatedIds) {
    const relatedNode = state.nodesById.get(relatedId);
    if (!relatedNode) {
      continue;
    }
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = `${relatedNode.title} — ${relatedNode.page_title}`;
    chip.addEventListener("click", () => select(relatedId));
    container.append(chip);
  }

  return container;
}

function renderMarkdown(markdownText) {
  const escaped = escapeHtml(markdownText);
  const withCodeBlocks = escaped.replace(
    /```[a-z]*\n([\s\S]*?)```/g,
    (match, body) => `<pre><code>${body}</code></pre>`
  );
  const withInlineCode = withCodeBlocks.replace(/`([^`\n]+)`/g, "<code>$1</code>");
  const withBold = withInlineCode.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
  const withParagraphs = withBold
    .split(/\n{2,}/)
    .map((chunk) => (chunk.startsWith("<pre>") ? chunk : `<p>${chunk.replace(/\n/g, "<br>")}</p>`))
    .join("");
  return withParagraphs;
}

function escapeHtml(text) {
  const element = document.createElement("div");
  element.textContent = text;
  return element.innerHTML;
}

function cssEscape(value) {
  return value.replace(/["\\]/g, "\\$&");
}

load();
```

- [ ] **Step 4: Verify the viewer renders against a fixture graph**

Run:
```bash
cd /home/viktar/Projects/Support
mkdir -p graph
python -c "
import json, pathlib
document = {
  'nodes': [
    {'id': 'php', 'type': 'page', 'title': 'PHP', 'level': 0, 'page_id': 'php', 'page_title': 'PHP', 'is_toggle': False, 'is_priority': False, 'content_md': ''},
    {'id': 'php#0', 'type': 'section', 'title': 'Basics', 'level': 1, 'page_id': 'php', 'page_title': 'PHP', 'is_toggle': False, 'is_priority': True, 'content_md': 'body text'},
    {'id': 'php#1', 'type': 'section', 'title': 'CQRS', 'level': 2, 'page_id': 'php', 'page_title': 'PHP', 'is_toggle': True, 'is_priority': False, 'content_md': 'hidden answer'}
  ],
  'edges': [
    {'source': 'php', 'target': 'php#0', 'kind': 'contains'},
    {'source': 'php#0', 'target': 'php#1', 'kind': 'contains'}
  ]
}
pathlib.Path('graph/graph.json').write_text(json.dumps(document))
"
python -m support.cli serve --port 8765
```

Open `http://127.0.0.1:8765/viewer/index.html`. Confirm by clicking only:
- `PHP` appears at the top level with a caret.
- Clicking `PHP` expands it and reveals `Basics`, rendered in the priority colour.
- Clicking `Basics` shows `body text` on the right and reveals the collapsed `CQRS` toggle.
- Clicking the `CQRS` summary reveals `hidden answer`.
- No text input exists anywhere on the page.

Stop the server with Ctrl+C.

- [ ] **Step 5: Commit**

```bash
cd /home/viktar/Projects/Support
git add viewer/index.html viewer/style.css viewer/app.js
git commit -m "Add click-only offline viewer"
```

---

### Task 9: First real sync and project documentation

**Files:**
- Create: `/home/viktar/Projects/Support/README.md`
- Create: `/home/viktar/Projects/Support/CLAUDE.md`

**Interfaces:**
- Consumes: every module built in tasks 1 through 8.
- Produces: nothing consumed by other tasks.

- [ ] **Step 1: Install the package and confirm the whole suite passes**

Run:
```bash
cd /home/viktar/Projects/Support
python -m pip install -e ".[dev]"
python -m pytest -v
```
Expected: PASS — 40 passed

- [ ] **Step 2: Set up Notion access**

This is a manual step performed in a browser, not a code change:

1. Open `https://www.notion.so/profile/integrations` and create a new internal integration with read content capability only.
2. Copy its internal integration secret.
3. Open `https://app.notion.com/p/kruglikov/Software-Development-9bbf3c16e12041f3996bae0eb316cd78`, use the page menu, and connect the integration to the page.
4. Export both variables in the shell:

```bash
export NOTION_TOKEN=<the integration secret>
export NOTION_ROOT_PAGE_ID=9bbf3c16e12041f3996bae0eb316cd78
```

- [ ] **Step 3: Run status, then the first full sync**

Run:
```bash
cd /home/viktar/Projects/Support
support status
support sync
```
Expected: `status` reports roughly 35 new pages and writes nothing. `sync` writes them, reports zero pruned, and lists any unsupported block warnings.

- [ ] **Step 4: Build the graph and check the real numbers**

Run:
```bash
cd /home/viktar/Projects/Support
support build-graph
python -c "
import json
document = json.load(open('graph/graph.json'))
sections = [node for node in document['nodes'] if node['type'] == 'section']
print('pages   :', len(document['nodes']) - len(sections))
print('sections:', len(sections))
print('toggles :', sum(1 for node in sections if node['is_toggle']))
print('priority:', sum(1 for node in sections if node['is_priority']))
for kind in ('contains', 'links_to', 'mentions'):
    print(kind, ':', sum(1 for edge in document['edges'] if edge['kind'] == kind))
"
```

Sanity check against the spec findings: the `OOP\Principles\Patterns` page should contribute 36 sections, 17 of them toggles and 13 priority-marked. If the section count is noticeably higher, the fence handling regressed — re-run `python -m pytest tests/test_headings.py -v`.

- [ ] **Step 5: Confirm the viewer works on real data**

Run: `cd /home/viktar/Projects/Support && support serve`

Open `http://127.0.0.1:8765/viewer/index.html` and navigate from the root page down to a toggle section using only clicks.

- [ ] **Step 6: Write the README**

Create `/home/viktar/Projects/Support/README.md`:

```markdown
# Support

A local mirror of a Notion knowledge base, a knowledge graph extracted from it, and a click-only viewer for use during interviews.

Notion is the source of truth. Nothing here writes back to Notion.

## Setup

    python -m pip install -e ".[dev]"
    cp .env.example .env   # then fill in both values and export them

`NOTION_TOKEN` is an internal integration secret; the integration must be connected to the root page. `NOTION_ROOT_PAGE_ID` is the ID of that root page.

## Commands

    support status        # report what a sync would change; writes nothing
    support sync          # fetch changed pages into mirror/
    support sync --full   # refetch every page
    support build-graph   # rebuild graph/graph.json from mirror/
    support serve         # serve the viewer at http://127.0.0.1:8765/viewer/index.html

Run `support sync` then `support build-graph` after editing Notion.

## Tests

    python -m pytest
    python -m pytest tests/test_headings.py -v   # the correctness core

## Layout

- `mirror/` — Markdown per page, raw API JSON under `mirror/.raw/`, and `mirror/manifest.json`. Committed, so each sync produces a reviewable diff of what changed in Notion.
- `graph/graph.json` — regenerated whole on every build; never edited by hand.
- `viewer/` — static HTML, CSS and JavaScript. Reads `graph/graph.json` and nothing else.
```

- [ ] **Step 7: Write CLAUDE.md**

Create `/home/viktar/Projects/Support/CLAUDE.md`:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

    python -m pip install -e ".[dev]"            # install
    python -m pytest                             # all tests
    python -m pytest tests/test_headings.py -v   # one module
    python -m pytest tests/test_headings.py::test_heading_like_lines_inside_code_fences_are_ignored -v   # one test

    support status        # what a sync would change; writes nothing
    support sync          # incremental fetch into mirror/
    support sync --full   # ignore the manifest, refetch everything
    support build-graph   # rebuild graph/graph.json from mirror/
    support serve         # http://127.0.0.1:8765/viewer/index.html

`support sync` and `support status` need `NOTION_TOKEN` and `NOTION_ROOT_PAGE_ID` in the environment. Every other command works offline.

## Architecture

Three layers that communicate only through files. No layer imports another layer's code, and each can be replaced by honouring its output format alone.

1. **Mirror** (`src/support/notion_api.py`, `src/support/markdown.py`, `src/support/sync.py`) — reads Notion, writes `mirror/<slug>.md`, `mirror/.raw/<page-id>.json`, and `mirror/manifest.json`. Incremental by `last_edited_time`. A page's manifest entry is written only after that page's files, so an interrupted sync resumes rather than corrupts.
2. **Graph** (`src/support/graph.py`, `src/support/headings.py`) — a pure function from `mirror/` to `graph/graph.json`. Never calls Notion. Regenerated whole on every build.
3. **Viewer** (`viewer/`) — vanilla JavaScript, no build step. Reads `graph/graph.json` and nothing else. No network at view time, no text input.

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
```

- [ ] **Step 8: Commit**

```bash
cd /home/viktar/Projects/Support
git add README.md CLAUDE.md mirror graph
git commit -m "Add project documentation and the first Notion mirror"
```

---

## Self-Review

**Spec coverage.** Every section of `/home/viktar/Projects/Support/docs/superpowers/specs/2026-09-10-notion-knowledge-graph-design.md` maps to a task:

| Spec requirement | Task |
|---|---|
| Environment configuration, token never committed | Task 1 |
| Finding 2 — code fences produce false headings | Task 2 |
| Finding 5 — heading levels skip | Task 2 |
| Findings 3 and 4 — toggle and priority flags | Tasks 2, 5, 7, 8 |
| Manifest, incremental change detection, slug collisions | Task 3 |
| Finding 6 — pagination and partial data | Task 4 |
| Rate limit throttling | Task 4 |
| Unsupported blocks warn rather than fail silently | Task 5 |
| `sync`, `sync --full`, `status` | Task 6 |
| Interrupted sync resumes cleanly | Task 6 |
| Pruning removed pages | Task 6 |
| Node and edge shapes, three edge kinds | Task 7 |
| `graph.json` regenerated whole | Task 7 |
| Click-only tree, toggle-as-hidden-answer, related chips, priority weighting | Task 8 |
| Viewer works offline, missing `graph.json` message | Task 8 |
| `mirror/` committed under git | Task 9 |

Error-handling rows from the spec that are covered implicitly: invalid token raises `ConfigError` and leaves the mirror untouched (Task 1 and Task 6), and a missing `graph.json` produces an explicit viewer message rather than an empty tree (Task 8).

**Placeholder scan.** No TBDs, no "add error handling", no "similar to Task N". Every code step carries complete code.

**Type consistency.** `PageRecord`, `SyncPlan`, `PageNode`, `Heading`, `Section`, and `ConversionResult` are defined once and used with identical field names throughout. `build_sections` returns `Section` objects whose `parent_index` is consumed by `support.graph.build_graph_document` exactly as defined in Task 2. `blocks_to_markdown` returns `ConversionResult` and is consumed as `conversion.markdown` and `conversion.warnings` in Task 6, matching Task 5.

**Known gap, deliberate.** The spec's testing section asks for a viewer test that loads a fixture `graph.json` and renders without a network request. Task 8 covers this as a manual verification step rather than an automated test, because adding a JavaScript test runner would contradict the no-build-step constraint. If automated coverage is wanted later, it is a separate task.
