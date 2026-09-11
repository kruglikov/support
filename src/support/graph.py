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

    node_ids_by_lowercase_title = {}
    for target_node in section_nodes:
        target_title = target_node["title"]
        if len(target_title) < MINIMUM_MENTION_LENGTH:
            continue
        lowercase_title = target_title.lower()
        node_ids_by_lowercase_title.setdefault(lowercase_title, []).append(target_node["id"])

    qualifying_titles = sorted(
        node_ids_by_lowercase_title, key=len, reverse=True
    )
    if not qualifying_titles:
        return []

    alternation = "|".join(re.escape(title) for title in qualifying_titles)
    mention_pattern = re.compile(r"\b(?:" + alternation + r")\b", re.IGNORECASE)

    mention_edges = []
    for source_node in section_nodes:
        source_text = source_node["content_md"]
        if not source_text:
            continue

        matched_titles = []
        seen_titles = set()
        for match in mention_pattern.finditer(source_text):
            matched_title = match.group(0).lower()
            if matched_title not in seen_titles:
                seen_titles.add(matched_title)
                matched_titles.append(matched_title)

        for matched_title in matched_titles:
            for target_node_id in node_ids_by_lowercase_title[matched_title]:
                if target_node_id == source_node["id"]:
                    continue
                mention_edges.append(
                    {
                        "source": source_node["id"],
                        "target": target_node_id,
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
