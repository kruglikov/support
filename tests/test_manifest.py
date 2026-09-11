from support.manifest import (
    PageRecord,
    content_hash,
    load_manifest,
    page_slug,
    plan_sync,
    save_manifest,
)


def make_record(page_id, last_edited_time):
    return PageRecord(
        page_id=page_id,
        title="Databases",
        parent_id="root",
        last_edited_time=last_edited_time,
        output_path="databases.md",
        content_hash="abc",
    )


def test_manifest_round_trips_through_disk(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    records = {"page-1": make_record("page-1", "2026-08-26T14:42:09.249Z")}

    save_manifest(manifest_path, records)

    assert load_manifest(manifest_path) == records


def test_load_manifest_returns_empty_mapping_when_file_absent(tmp_path):
    assert load_manifest(tmp_path / "missing.json") == {}


def test_plan_sync_classifies_new_changed_unchanged_and_removed():
    records = {
        "unchanged": make_record("unchanged", "2026-01-01T00:00:00.000Z"),
        "changed": make_record("changed", "2026-01-01T00:00:00.000Z"),
        "removed": make_record("removed", "2026-01-01T00:00:00.000Z"),
    }
    remote_last_edited = {
        "unchanged": "2026-01-01T00:00:00.000Z",
        "changed": "2026-02-02T00:00:00.000Z",
        "new": "2026-03-03T00:00:00.000Z",
    }

    plan = plan_sync(remote_last_edited, records)

    assert plan.new_page_ids == ["new"]
    assert plan.changed_page_ids == ["changed"]
    assert plan.unchanged_page_ids == ["unchanged"]
    assert plan.removed_page_ids == ["removed"]


def test_plan_sync_with_force_full_treats_every_known_page_as_changed():
    records = {"unchanged": make_record("unchanged", "2026-01-01T00:00:00.000Z")}
    remote_last_edited = {"unchanged": "2026-01-01T00:00:00.000Z"}

    plan = plan_sync(remote_last_edited, records, force_full=True)

    assert plan.changed_page_ids == ["unchanged"]
    assert plan.unchanged_page_ids == []


def test_page_slug_is_derived_from_the_title():
    assert page_slug("OOP\\Principles\\Patterns", "3649c92c96f5805b", set()) == "oop-principles-patterns"


def test_page_slug_appends_page_id_prefix_on_collision():
    taken_slugs = {"security"}

    slug = page_slug("Security", "3b39c92c-96f5-8034-bb16-e53185347a59", taken_slugs)

    assert slug == "security-3b39c92c"


def test_page_slug_falls_back_for_a_title_with_no_usable_characters():
    assert page_slug("...", "3b39c92c96f58034", set()) == "untitled"


def test_content_hash_is_stable_and_differs_per_content():
    assert content_hash("same") == content_hash("same")
    assert content_hash("one") != content_hash("two")
