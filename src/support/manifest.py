import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

SLUG_SEPARATOR_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class PageRecord:
    page_id: str
    title: str
    parent_id: str | None
    last_edited_time: str
    output_path: str
    content_hash: str


@dataclass(frozen=True)
class SyncPlan:
    new_page_ids: list[str]
    changed_page_ids: list[str]
    unchanged_page_ids: list[str]
    removed_page_ids: list[str]


def load_manifest(manifest_path):
    path = Path(manifest_path)
    if not path.exists():
        return {}

    raw_records = json.loads(path.read_text(encoding="utf-8"))
    records = {
        page_id: PageRecord(**fields) for page_id, fields in raw_records.items()
    }
    return records


def save_manifest(manifest_path, records):
    payload = {page_id: asdict(record) for page_id, record in records.items()}
    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )


def plan_sync(remote_last_edited, records, force_full=False):
    new_page_ids = []
    changed_page_ids = []
    unchanged_page_ids = []

    for page_id, last_edited_time in remote_last_edited.items():
        known_record = records.get(page_id)
        if known_record is None:
            new_page_ids.append(page_id)
        elif force_full or known_record.last_edited_time != last_edited_time:
            changed_page_ids.append(page_id)
        else:
            unchanged_page_ids.append(page_id)

    removed_page_ids = [
        page_id for page_id in records if page_id not in remote_last_edited
    ]

    plan = SyncPlan(
        new_page_ids=sorted(new_page_ids),
        changed_page_ids=sorted(changed_page_ids),
        unchanged_page_ids=sorted(unchanged_page_ids),
        removed_page_ids=sorted(removed_page_ids),
    )
    return plan


def page_slug(title, page_id, taken_slugs):
    base_slug = SLUG_SEPARATOR_PATTERN.sub("-", title.lower()).strip("-")
    if not base_slug:
        base_slug = "untitled"

    if base_slug not in taken_slugs:
        return base_slug

    disambiguated_slug = f"{base_slug}-{page_id.replace('-', '')[:8]}"
    return disambiguated_slug


def content_hash(text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return digest
