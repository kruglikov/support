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
        rendered = f"{'#' * level} {title}{toggle_suffix}"
    elif block_type == "paragraph":
        rendered = rich_text_to_markdown(payload.get("rich_text", []))
    elif block_type == "bulleted_list_item":
        rendered = f"- {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "numbered_list_item":
        rendered = f"1. {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "to_do":
        checkbox = "x" if payload.get("checked") else " "
        rendered = f"- [{checkbox}] {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "quote":
        rendered = f"> {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "callout":
        rendered = f"> {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "toggle":
        rendered = f"- {rich_text_to_markdown(payload.get('rich_text', []))}"
    elif block_type == "code":
        language = payload.get("language", "")
        body = rich_text_to_markdown(payload.get("rich_text", []))
        rendered = f"```{language}\n{body}\n```"
    elif block_type == "divider":
        rendered = "---"
    elif block_type == "child_page":
        rendered = f"[{payload.get('title', 'Untitled')}](notion://{block.get('id', '')})"
    elif block_type == "child_database":
        rendered = f"[{payload.get('title', 'Database')}](notion://{block.get('id', '')})"
    else:
        warnings.append(
            f"unsupported block type '{block_type}' (id {block.get('id', 'unknown')})"
        )
        rendered = ""

    children = block.get("children", [])
    if children:
        children_rendered = []
        for child in children:
            child_output = _render_block(child, warnings)
            if child_output:
                children_rendered.append(child_output)
        if children_rendered:
            if rendered:
                rendered = rendered + "\n\n" + "\n\n".join(children_rendered)
            else:
                rendered = "\n\n".join(children_rendered)

    return rendered


def blocks_to_markdown(blocks):
    warnings = []
    rendered_blocks = []

    for block in blocks:
        rendered = _render_block(block, warnings)
        if rendered:
            rendered_blocks.append(rendered)

    result = ConversionResult(markdown="\n\n".join(rendered_blocks), warnings=warnings)
    return result
