"""End-to-end seam test: notion_api -> markdown -> headings.

Seam finding 1 slipped through per-module tests: fetch_all_blocks inlined an
entire subpage into its parent's Markdown because it recursed into any block
with has_children, including child_page/child_database boundaries. This test
drives a realistic block tree straight through fetch_all_blocks,
blocks_to_markdown and build_sections/parse_headings, and fails against the
pre-fix fetch_all_blocks because the fake client raises if anything ever asks
for the child page's own content.
"""

from support.headings import build_sections
from support.markdown import blocks_to_markdown
from support.notion_api import NotionGateway


def text_fragment(content, color="default"):
    return {
        "plain_text": content,
        "annotations": {"bold": False, "italic": False, "code": False, "color": color},
        "href": None,
    }


class StrictFakeBlocksChildren:
    """Serves a fixed block tree; raises if asked for a page-boundary's content."""

    def __init__(self, blocks_by_id):
        self.blocks_by_id = blocks_by_id

    def list(self, block_id, start_cursor=None, page_size=100):
        if block_id == "sub-1":
            raise AssertionError(
                "fetch_all_blocks must not recurse into a child_page boundary"
            )
        return {"results": self.blocks_by_id[block_id], "has_more": False, "next_cursor": None}


class FakeClient:
    def __init__(self, blocks_children):
        self.blocks = type("Blocks", (), {"children": blocks_children})()


def test_full_pipeline_preserves_flags_skips_code_comments_and_does_not_inline_a_subpage():
    blocks_by_id = {
        "root": [
            {
                "id": "h-toggle",
                "type": "heading_2",
                "has_children": True,
                "heading_2": {
                    "rich_text": [text_fragment("Interview questions")],
                    "is_toggleable": True,
                },
            },
            {
                "id": "h-priority",
                "type": "heading_2",
                "has_children": False,
                "heading_2": {
                    "rich_text": [text_fragment("GoF (Design) patterns", color="red")],
                    "is_toggleable": False,
                },
            },
            {
                "id": "code-1",
                "type": "code",
                "has_children": False,
                "code": {
                    "rich_text": [
                        text_fragment("# not a heading\n# still not a heading")
                    ],
                    "language": "python",
                },
            },
            {
                "id": "sub-1",
                "type": "child_page",
                "has_children": True,
                "child_page": {"title": "PHP"},
            },
        ],
        "h-toggle": [
            {
                "id": "answer-1",
                "type": "paragraph",
                "has_children": False,
                "paragraph": {
                    "rich_text": [text_fragment("Encapsulation, inheritance, polymorphism.")]
                },
            }
        ],
        # A pre-fix fetch_all_blocks would also request this for "sub-1" since
        # it has has_children True; the fake raises if that ever happens.
        "sub-1": [
            {
                "id": "leaked",
                "type": "paragraph",
                "has_children": False,
                "paragraph": {
                    "rich_text": [text_fragment("This lives on the PHP page, not here.")]
                },
            }
        ],
    }

    gateway = NotionGateway(
        FakeClient(StrictFakeBlocksChildren(blocks_by_id)), min_seconds_between_calls=0
    )

    blocks = gateway.fetch_all_blocks("root")
    conversion = blocks_to_markdown(blocks)
    sections = build_sections(conversion.markdown)

    titles = [section.heading.title for section in sections]
    assert titles == ["Interview questions", "GoF (Design) patterns"]

    toggle_section, priority_section = sections
    assert toggle_section.heading.is_toggle is True
    assert "Encapsulation" in toggle_section.content

    assert priority_section.heading.is_priority is True

    assert "not a heading" not in titles
    assert "This lives on the PHP page" not in conversion.markdown
    assert "[PHP](notion://sub-1)" in conversion.markdown
