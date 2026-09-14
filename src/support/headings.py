import re
from dataclasses import dataclass

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
FENCE_PATTERN = re.compile(r"^\s*(?:```|~~~)")
TOGGLE_PATTERN = re.compile(r'\{toggle="true"\}')
PRIORITY_PATTERN = re.compile(r'<span[^>]*color="red"[^>]*>')
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\([^)]*\)")
NON_EMPHASIS_MARKUP_PATTERN = re.compile(r'<[^>]+>|\{toggle="[^"]*"\}')
# Asterisks are never part of an identifier, so paired asterisk emphasis is
# stripped anywhere in a title, and any unpaired "**" left over by Notion's
# own uneven bold runs is removed too. Underscores DO appear in identifiers
# (snake_case_name, __init__, $_SERVER), so underscore emphasis is stripped
# only when the pair wraps the entire title.
DOUBLE_ASTERISK_EMPHASIS_PATTERN = re.compile(r"\*\*(\S(?:.*?\S)?)\*\*")
LEFTOVER_DOUBLE_ASTERISK_PATTERN = re.compile(r"\*\*")
SINGLE_ASTERISK_EMPHASIS_PATTERN = re.compile(r"\*(\S(?:.*?\S)?)\*")
UNDERSCORE_EMPHASIS_PATTERN = re.compile(r"^(__|_)(\S(?:.*\S)?)\1$")


def strip_paired_emphasis(text):
    without_double_pairs = DOUBLE_ASTERISK_EMPHASIS_PATTERN.sub(r"\1", text)
    without_stray_doubles = LEFTOVER_DOUBLE_ASTERISK_PATTERN.sub("", without_double_pairs)
    without_asterisks = SINGLE_ASTERISK_EMPHASIS_PATTERN.sub(r"\1", without_stray_doubles)

    underscore_match = UNDERSCORE_EMPHASIS_PATTERN.match(without_asterisks)
    if underscore_match:
        return underscore_match.group(2)

    return without_asterisks


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
    delinked_title = LINK_PATTERN.sub(r"\1", raw_title)
    stripped_title = NON_EMPHASIS_MARKUP_PATTERN.sub("", delinked_title).strip()
    cleaned_title = strip_paired_emphasis(stripped_title).strip()
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


def leading_content(markdown_text):
    """Return the text before the first real heading, fence-aware.

    Returns the whole document, stripped, when there is no heading.
    """
    headings = parse_headings(markdown_text)
    if not headings:
        return markdown_text.strip()

    lines = markdown_text.split("\n")
    first_heading_line_index = headings[0].line_index
    content = "\n".join(lines[:first_heading_line_index]).strip()
    return content


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
