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
