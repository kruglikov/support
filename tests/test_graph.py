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
