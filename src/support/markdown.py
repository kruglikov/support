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
