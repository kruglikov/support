import httpx
import pytest
from notion_client import APIErrorCode, APIResponseError

from support.notion_api import NotionGateway, PageNode, extract_title


def make_api_response_error(code):
    return APIResponseError(
        code=code,
        status=429 if code == APIErrorCode.RateLimited else 401,
        message="boom",
        headers=httpx.Headers(),
        raw_body_text="",
    )


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


def test_fetch_all_blocks_terminates_when_next_cursor_is_null():
    class FakeBlocksChildrenWithNullCursor:
        def __init__(self):
            self.requested_cursors = []

        def list(self, block_id, start_cursor=None, page_size=100):
            self.requested_cursors.append(start_cursor)
            if len(self.requested_cursors) > 1:
                raise AssertionError("Should not request a second time with cursor None")
            return {"results": [{"id": "b1"}], "has_more": True, "next_cursor": None}

    blocks_children = FakeBlocksChildrenWithNullCursor()
    gateway = NotionGateway(FakeClient(blocks_children), min_seconds_between_calls=0)

    blocks = gateway.fetch_all_blocks("page-1")

    assert [block["id"] for block in blocks] == ["b1"]
    assert blocks_children.requested_cursors == [None]


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


def test_fetch_all_blocks_recursively_fetches_children():
    class FakeBlocksChildrenWithBlockIdSupport:
        def __init__(self):
            self.requested_cursors = []

        def list(self, block_id, start_cursor=None, page_size=100):
            self.requested_cursors.append((block_id, start_cursor))
            if block_id == "page-1" and start_cursor is None:
                return {
                    "results": [
                        {"id": "b1", "has_children": True},
                        {"id": "b2", "has_children": False},
                    ],
                    "has_more": False,
                    "next_cursor": None,
                }
            elif block_id == "b1" and start_cursor is None:
                return {
                    "results": [
                        {"id": "child1"},
                        {"id": "child2"},
                    ],
                    "has_more": False,
                    "next_cursor": None,
                }
            else:
                return {"results": [], "has_more": False, "next_cursor": None}

    blocks_children = FakeBlocksChildrenWithBlockIdSupport()
    gateway = NotionGateway(FakeClient(blocks_children), min_seconds_between_calls=0)

    blocks = gateway.fetch_all_blocks("page-1")

    assert len(blocks) == 2
    assert blocks[0]["id"] == "b1"
    assert blocks[0]["children"] == [{"id": "child1"}, {"id": "child2"}]
    assert blocks[1]["id"] == "b2"
    assert "children" not in blocks[1]


def test_fetch_all_blocks_does_not_recurse_into_child_page_boundaries():
    class FakeBlocksChildrenThatFailsIfAskedForSubpageContent:
        def list(self, block_id, start_cursor=None, page_size=100):
            if block_id == "root":
                return {
                    "results": [
                        {"id": "sub", "type": "child_page", "has_children": True},
                    ],
                    "has_more": False,
                    "next_cursor": None,
                }
            raise AssertionError(
                "must not fetch children of a child_page boundary block"
            )

    blocks_children = FakeBlocksChildrenThatFailsIfAskedForSubpageContent()
    gateway = NotionGateway(FakeClient(blocks_children), min_seconds_between_calls=0)

    blocks = gateway.fetch_all_blocks("root")

    assert len(blocks) == 1
    assert "children" not in blocks[0]


def test_fetch_all_blocks_does_not_recurse_into_child_database_boundaries():
    class FakeBlocksChildrenThatFailsIfAskedForDatabaseContent:
        def list(self, block_id, start_cursor=None, page_size=100):
            if block_id == "root":
                return {
                    "results": [
                        {"id": "sub", "type": "child_database", "has_children": True},
                    ],
                    "has_more": False,
                    "next_cursor": None,
                }
            raise AssertionError(
                "must not fetch children of a child_database boundary block"
            )

    blocks_children = FakeBlocksChildrenThatFailsIfAskedForDatabaseContent()
    gateway = NotionGateway(FakeClient(blocks_children), min_seconds_between_calls=0)

    blocks = gateway.fetch_all_blocks("root")

    assert len(blocks) == 1
    assert "children" not in blocks[0]


def test_walk_page_tree_finds_a_child_page_nested_inside_a_toggle():
    blocks_children = FakeBlocksChildren({
        None: {"results": [], "has_more": False, "next_cursor": None},
    })
    client = FakeClient(blocks_children)
    gateway = NotionGateway(client, min_seconds_between_calls=0)

    child_blocks = {
        "root": [
            {
                "type": "toggle",
                "id": "toggle-1",
                "has_children": True,
                "children": [
                    {"type": "child_page", "id": "nested", "child_page": {"title": "Nested"}},
                ],
            },
        ],
        "nested": [],
    }
    last_edited = {
        "root": "2026-01-01T00:00:00.000Z",
        "nested": "2026-01-02T00:00:00.000Z",
    }
    gateway.fetch_all_blocks = lambda block_id: child_blocks[block_id]
    gateway.fetch_page = lambda page_id: {
        "id": page_id,
        "last_edited_time": last_edited[page_id],
        "properties": {"title": {"title": [{"plain_text": "Software Development"}]}},
    }

    nodes = gateway.walk_page_tree("root")

    assert [node.page_id for node in nodes] == ["root", "nested"]
    assert nodes[1].title == "Nested"


def test_walk_page_tree_falls_back_to_untitled_for_a_blank_child_page_title():
    blocks_children = FakeBlocksChildren({
        None: {"results": [], "has_more": False, "next_cursor": None},
    })
    client = FakeClient(blocks_children)
    gateway = NotionGateway(client, min_seconds_between_calls=0)

    child_blocks = {
        "root": [
            {"type": "child_page", "id": "a", "child_page": {"title": ""}},
        ],
        "a": [],
    }
    last_edited = {
        "root": "2026-01-01T00:00:00.000Z",
        "a": "2026-01-02T00:00:00.000Z",
    }
    gateway.fetch_all_blocks = lambda block_id: child_blocks[block_id]
    gateway.fetch_page = lambda page_id: {
        "id": page_id,
        "last_edited_time": last_edited[page_id],
        "properties": {"title": {"title": [{"plain_text": "Software Development"}]}},
    }

    nodes = gateway.walk_page_tree("root")

    assert nodes[1].title == "Untitled"


def test_rate_limited_calls_are_retried_with_backoff(monkeypatch):
    sleeps = []
    monkeypatch.setattr("support.notion_api.time.sleep", lambda seconds: sleeps.append(seconds))

    attempts = []

    class FlakyBlocksChildren:
        def list(self, block_id, start_cursor=None, page_size=100):
            attempts.append(1)
            if len(attempts) < 3:
                raise make_api_response_error(APIErrorCode.RateLimited)
            return {"results": [{"id": "b1"}], "has_more": False, "next_cursor": None}

    gateway = NotionGateway(
        FakeClient(FlakyBlocksChildren()),
        min_seconds_between_calls=0,
        initial_backoff_seconds=0.01,
    )

    blocks = gateway.fetch_all_blocks("page-1")

    assert [block["id"] for block in blocks] == ["b1"]
    assert len(attempts) == 3
    assert len(sleeps) == 2


def test_rate_limited_calls_re_raise_once_retries_are_exhausted(monkeypatch):
    monkeypatch.setattr("support.notion_api.time.sleep", lambda seconds: None)

    class AlwaysRateLimitedBlocksChildren:
        def list(self, block_id, start_cursor=None, page_size=100):
            raise make_api_response_error(APIErrorCode.RateLimited)

    gateway = NotionGateway(
        FakeClient(AlwaysRateLimitedBlocksChildren()),
        min_seconds_between_calls=0,
        max_rate_limit_retries=2,
        initial_backoff_seconds=0.01,
    )

    with pytest.raises(APIResponseError):
        gateway.fetch_all_blocks("page-1")


def test_a_non_rate_limit_api_error_is_not_retried(monkeypatch):
    monkeypatch.setattr("support.notion_api.time.sleep", lambda seconds: None)
    attempts = []

    class UnauthorizedBlocksChildren:
        def list(self, block_id, start_cursor=None, page_size=100):
            attempts.append(1)
            raise make_api_response_error(APIErrorCode.Unauthorized)

    gateway = NotionGateway(
        FakeClient(UnauthorizedBlocksChildren()), min_seconds_between_calls=0
    )

    with pytest.raises(APIResponseError):
        gateway.fetch_all_blocks("page-1")
    assert len(attempts) == 1
