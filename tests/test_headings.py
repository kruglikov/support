from support.headings import build_sections, leading_content, parse_headings


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


def test_italic_and_underscore_emphasis_are_stripped_from_headings():
    markdown_text = "\n".join([
        "# *Foo*",
        "# _Bar_",
    ])

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == ["Foo", "Bar"]


def test_markdown_link_syntax_is_reduced_to_its_text_in_headings():
    markdown_text = "# [Foo](notion://abc-123)"

    headings = parse_headings(markdown_text)

    assert [heading.title for heading in headings] == ["Foo"]


def test_leading_content_returns_text_before_the_first_heading():
    markdown_text = "\n".join([
        "intro line one",
        "intro line two",
        "",
        "# Basics",
        "body",
    ])

    assert leading_content(markdown_text) == "intro line one\nintro line two"


def test_leading_content_is_the_whole_document_when_there_is_no_heading():
    markdown_text = "just some text\nwith no headings at all"

    assert leading_content(markdown_text) == markdown_text


def test_leading_content_ignores_heading_like_lines_inside_a_fence():
    markdown_text = "\n".join([
        "```python",
        "# not a heading",
        "```",
        "# Real Heading",
        "body",
    ])

    assert leading_content(markdown_text) == "```python\n# not a heading\n```"
