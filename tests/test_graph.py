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


def test_punctuation_titles_are_mentioned(tmp_path):
    # "C++" (3 chars) is below MINIMUM_MENTION_LENGTH and would never qualify
    # as a mention target regardless of the boundary bug, so "Visual C++" is
    # used here: it is long enough to qualify and still ends in punctuation,
    # exercising the same trailing (?!\w) case; ".NET" exercises the leading
    # (?<!\w) case.
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("langs", "Languages", None,
         "# Visual C++\nbody\n# .NET\nbody\n# Intro\nwe love Visual C++ and .NET a lot"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    mentions_edges = [edge for edge in document["edges"] if edge["kind"] == "mentions"]
    assert {"source": "langs#2", "target": "langs#0", "kind": "mentions"} in mentions_edges
    assert {"source": "langs#2", "target": "langs#1", "kind": "mentions"} in mentions_edges


def test_longest_title_wins_over_a_shorter_prefix(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("patterns", "Patterns", None,
         "# SAGA\nbody\n# SAGA Pattern\nbody\n# Intro\nwe use the SAGA Pattern here\n"
         "# Noise\nancient SAGAS are still studied today"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    mentions_edges = [edge for edge in document["edges"] if edge["kind"] == "mentions"]
    assert {"source": "patterns#2", "target": "patterns#1", "kind": "mentions"} in mentions_edges
    assert {"source": "patterns#2", "target": "patterns#0", "kind": "mentions"} not in mentions_edges
    # "SAGAS" embeds "SAGA" as a substring but is followed by a word character
    # ("s"), so the lookahead must still reject it, exactly as \b did.
    assert {"source": "patterns#3", "target": "patterns#0", "kind": "mentions"} not in mentions_edges
    assert {"source": "patterns#3", "target": "patterns#1", "kind": "mentions"} not in mentions_edges


def test_mention_matching_is_case_insensitive(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("infra", "Infra", None, "# API Gateway\nbody\n# Intro\nwe use the api GATEWAY here"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    mentions_edges = [edge for edge in document["edges"] if edge["kind"] == "mentions"]
    assert {"source": "infra#1", "target": "infra#0", "kind": "mentions"} in mentions_edges


def test_duplicate_titles_across_pages_each_get_a_mention_edge(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("db", "Databases", None, "# Transactions\nbody"),
        ("php", "PHP", None, "# Transactions\nbody"),
        ("intro", "Intro", None, "# Overview\nTransactions matter a lot"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    mentions_edges = [edge for edge in document["edges"] if edge["kind"] == "mentions"]
    assert {"source": "intro#0", "target": "db#0", "kind": "mentions"} in mentions_edges
    assert {"source": "intro#0", "target": "php#0", "kind": "mentions"} in mentions_edges
    assert len(mentions_edges) == 2

    mirror_dir, manifest_path = prepare_mirror(tmp_path.joinpath("other"), [
        ("db", "Databases", None, "# Transactions\nbody"),
        ("php", "PHP", None, "# Transactions\nWe rely on Transactions heavily"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    mentions_edges = [edge for edge in document["edges"] if edge["kind"] == "mentions"]
    assert {"source": "php#0", "target": "db#0", "kind": "mentions"} in mentions_edges
    assert {"source": "php#0", "target": "php#0", "kind": "mentions"} not in mentions_edges
    assert len(mentions_edges) == 1


def test_page_node_gets_the_intro_content_before_the_first_heading(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "intro text\n\n# Basics\nbody"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    page_node = next(node for node in document["nodes"] if node["id"] == "php")
    assert page_node["content_md"] == "intro text"


def test_page_node_gets_the_whole_body_when_there_are_no_headings(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "just a body with no headings at all"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    page_node = next(node for node in document["nodes"] if node["id"] == "php")
    assert page_node["content_md"] == "just a body with no headings at all"


def test_a_notion_link_in_leading_content_becomes_a_links_to_edge_from_the_page(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("root", "Software Development", None, ""),
        ("php", "PHP", "root", "see [Databases](notion://db)\n\n# Basics"),
        ("db", "Databases", "root", "# Indexes"),
    ])

    document = build_graph_document(mirror_dir, manifest_path)

    assert {"source": "php", "target": "db", "kind": "links_to"} in document["edges"]


def test_a_missing_mirror_file_is_reported_as_a_warning_not_raised(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# Basics"),
    ])
    (mirror_dir / "php.md").unlink()

    document = build_graph_document(mirror_dir, manifest_path)

    assert len(document["warnings"]) == 1
    assert "PHP" in document["warnings"][0]
    assert str(mirror_dir / "php.md") in document["warnings"][0]
    page_node = next(node for node in document["nodes"] if node["id"] == "php")
    assert page_node["content_md"] == ""


def test_mention_lookup_never_raises_when_ignorecase_disagrees_with_str_lower(tmp_path, monkeypatch):
    """Reproduces re.IGNORECASE matching text whose .lower() is not a dict key.

    Real Unicode text can trigger this (re.IGNORECASE and str.lower() do not
    always agree), but it's simplest to force the exact scenario directly:
    fake the mention regex so it reports a match whose lowered text was never
    added to node_ids_by_lowercase_title, and assert this yields no edges
    instead of raising KeyError.
    """
    from support import graph as graph_module

    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# SAGA\nbody mentions SAGA here"),
    ])

    real_compile = graph_module.re.compile

    class FakeMatch:
        def group(self, index):
            return "a title that was never indexed"

    class FakeMentionPattern:
        def finditer(self, text):
            yield FakeMatch()

    def fake_compile(pattern, flags=0):
        if flags == graph_module.re.IGNORECASE:
            return FakeMentionPattern()
        return real_compile(pattern, flags)

    monkeypatch.setattr(graph_module.re, "compile", fake_compile)

    document = build_graph_document(mirror_dir, manifest_path)

    assert [edge for edge in document["edges"] if edge["kind"] == "mentions"] == []


def test_build_graph_writes_the_document_to_disk(tmp_path):
    mirror_dir, manifest_path = prepare_mirror(tmp_path, [
        ("php", "PHP", None, "# Basics"),
    ])
    graph_path = tmp_path / "graph" / "graph.json"

    node_count, edge_count, warnings = build_graph(mirror_dir, manifest_path, graph_path)

    written = json.loads(graph_path.read_text(encoding="utf-8"))
    assert len(written["nodes"]) == node_count == 2
    assert len(written["edges"]) == edge_count
    assert warnings == []
