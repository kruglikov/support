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
