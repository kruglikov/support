import json
from dataclasses import dataclass, field
from pathlib import Path

from support.manifest import (
    PageRecord,
    content_hash,
    load_manifest,
    page_slug,
    plan_sync,
    save_manifest,
)
from support.markdown import blocks_to_markdown


@dataclass
class SyncReport:
    written_page_ids: list[str] = field(default_factory=list)
    skipped_page_ids: list[str] = field(default_factory=list)
    pruned_page_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _remote_last_edited(nodes):
    remote_last_edited = {node.page_id: node.last_edited_time for node in nodes}
    return remote_last_edited


def run_status(gateway, root_page_id, manifest_path):
    nodes = gateway.walk_page_tree(root_page_id)
    records = load_manifest(manifest_path)
    plan = plan_sync(_remote_last_edited(nodes), records)
    return plan


def run_sync(gateway, root_page_id, mirror_dir, raw_dir, manifest_path, force_full=False):
    mirror_dir = Path(mirror_dir)
    raw_dir = Path(raw_dir)
    mirror_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    nodes = gateway.walk_page_tree(root_page_id)
    records = load_manifest(manifest_path)
    plan = plan_sync(_remote_last_edited(nodes), records, force_full=force_full)

    page_ids_to_write = set(plan.new_page_ids) | set(plan.changed_page_ids)
    report = SyncReport(skipped_page_ids=list(plan.unchanged_page_ids))

    taken_slugs = {
        record.output_path.removesuffix(".md")
        for page_id, record in records.items()
        if page_id not in page_ids_to_write
    }

    for node in nodes:
        if node.page_id not in page_ids_to_write:
            continue

        blocks = gateway.fetch_all_blocks(node.page_id)
        conversion = blocks_to_markdown(blocks)

        slug = page_slug(node.title, node.page_id, taken_slugs)
        taken_slugs.add(slug)

        existing_record = records.get(node.page_id)
        if existing_record is not None and existing_record.output_path != f"{slug}.md":
            (mirror_dir / existing_record.output_path).unlink(missing_ok=True)

        (mirror_dir / f"{slug}.md").write_text(conversion.markdown, encoding="utf-8")
        (raw_dir / f"{node.page_id}.json").write_text(
            json.dumps(blocks, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        records[node.page_id] = PageRecord(
            page_id=node.page_id,
            title=node.title,
            parent_id=node.parent_id,
            last_edited_time=node.last_edited_time,
            output_path=f"{slug}.md",
            content_hash=content_hash(conversion.markdown),
        )
        save_manifest(manifest_path, records)

        report.written_page_ids.append(node.page_id)
        report.warnings.extend(
            f"{node.title}: {warning}" for warning in conversion.warnings
        )

    for page_id in plan.removed_page_ids:
        stale_record = records.pop(page_id)
        (mirror_dir / stale_record.output_path).unlink(missing_ok=True)
        (raw_dir / f"{page_id}.json").unlink(missing_ok=True)
        report.pruned_page_ids.append(page_id)

    save_manifest(manifest_path, records)
    return report
