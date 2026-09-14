import json

from support.manifest import PageRecord, load_manifest, save_manifest
from support.notion_api import PageNode
from support.sync import run_status, run_sync


class FakeGateway:
    def __init__(self, nodes, blocks_by_page_id):
        self.nodes = nodes
        self.blocks_by_page_id = blocks_by_page_id

    def walk_page_tree(self, root_page_id):
        return self.nodes

    def fetch_all_blocks(self, block_id):
        return self.blocks_by_page_id[block_id]


def paragraph(content):
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "plain_text": content,
                    "annotations": {"bold": False, "italic": False, "code": False, "color": "default"},
                    "href": None,
                }
            ]
        },
    }


def build_gateway():
    nodes = [
        PageNode(page_id="root", title="Software Development", parent_id=None, last_edited_time="2026-01-01T00:00:00.000Z"),
        PageNode(page_id="php", title="PHP", parent_id="root", last_edited_time="2026-01-02T00:00:00.000Z"),
    ]
    blocks_by_page_id = {"root": [paragraph("root body")], "php": [paragraph("php body")]}
    return FakeGateway(nodes, blocks_by_page_id)


def test_run_sync_writes_markdown_raw_json_and_manifest(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert sorted(report.written_page_ids) == ["php", "root"]
    assert (mirror_dir / "php.md").read_text(encoding="utf-8") == "php body"
    assert json.loads((raw_dir / "php.json").read_text(encoding="utf-8"))[0]["type"] == "paragraph"

    records = load_manifest(manifest_path)
    assert records["php"].title == "PHP"
    assert records["php"].output_path == "php.md"


def test_run_sync_skips_pages_whose_last_edited_time_is_unchanged(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)
    second_report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert second_report.written_page_ids == []
    assert sorted(second_report.skipped_page_ids) == ["php", "root"]


def test_run_sync_with_force_full_rewrites_everything(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)
    forced_report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path, force_full=True)

    assert sorted(forced_report.written_page_ids) == ["php", "root"]


def test_run_sync_prunes_pages_that_disappeared_from_notion(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"
    mirror_dir.mkdir(parents=True)
    (mirror_dir / "gone.md").write_text("stale", encoding="utf-8")
    save_manifest(manifest_path, {
        "gone": PageRecord(
            page_id="gone",
            title="Gone",
            parent_id="root",
            last_edited_time="2026-01-01T00:00:00.000Z",
            output_path="gone.md",
            content_hash="x",
        )
    })

    report = run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    assert report.pruned_page_ids == ["gone"]
    assert not (mirror_dir / "gone.md").exists()
    assert "gone" not in load_manifest(manifest_path)


def test_run_sync_removes_the_old_mirror_file_when_a_page_is_renamed(tmp_path):
    mirror_dir = tmp_path / "mirror"
    raw_dir = mirror_dir / ".raw"
    manifest_path = mirror_dir / "manifest.json"

    run_sync(build_gateway(), "root", mirror_dir, raw_dir, manifest_path)

    renamed_nodes = [
        PageNode(page_id="root", title="Software Development", parent_id=None, last_edited_time="2026-01-01T00:00:00.000Z"),
        PageNode(page_id="php", title="PHP Renamed", parent_id="root", last_edited_time="2026-01-03T00:00:00.000Z"),
    ]
    blocks_by_page_id = {"root": [paragraph("root body")], "php": [paragraph("php body")]}
    gateway = FakeGateway(renamed_nodes, blocks_by_page_id)

    run_sync(gateway, "root", mirror_dir, raw_dir, manifest_path)

    assert (mirror_dir / "php-renamed.md").exists()
    assert not (mirror_dir / "php.md").exists()

    records = load_manifest(manifest_path)
    assert records["php"].output_path == "php-renamed.md"


def test_run_status_reports_the_plan_without_writing(tmp_path):
    manifest_path = tmp_path / "manifest.json"

    plan = run_status(build_gateway(), "root", manifest_path)

    assert plan.new_page_ids == ["php", "root"]
    assert not manifest_path.exists()
