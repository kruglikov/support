"""Write the Синодальный перевод text under every `reference` and `kjv-verse` block of pages/NNN.md.

The Russian line of a block is written only when it is still empty, so a manual correction is never overwritten.
Each English verse is compared with the same verse of bible/en_kjv.json first; a verse whose English text does not
match (a wrong reference, or a block that is not the verse it claims to be) is reported and left empty.

Run from the project root:
  python3 God/tools/fill_synodal.py
"""

import difflib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extract_pages import BIBLE_BOOKS, BOOK_BY_ALIAS, kjv_to_synodal, normalize_book_name, numbering_note  # noqa: E402

GOD_DIR = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = GOD_DIR / "pages"
SYNODAL_BIBLE_PATH = GOD_DIR / "bible" / "ru_synod.json"
KJV_BIBLE_PATH = GOD_DIR / "bible" / "en_kjv.json"
MIN_KJV_SIMILARITY = 0.8

MARKER_RE = re.compile(r"^<!-- block (?P<block_id>\d+) · (?P<block_type>[\w-]+) · (?P<english_ref>[^·]+?) → (?P<synodal_ref>[^·]+?)(?: · (?P<tags>.*))? -->$")
REF_RE = re.compile(r"^(?P<book>.+?) (?P<chapter>\d+):(?P<verses>[\d\s,–-]+)$")


def load_bible(bible_path):
    bible_books = json.loads(bible_path.read_text(encoding="utf-8-sig"))
    chapters_by_abbrev = {bible_book["abbrev"]: bible_book["chapters"] for bible_book in bible_books}

    return chapters_by_abbrev


def build_dataset_abbrev_by_english_name():
    """The KJV file lists all 66 books in the same canonical order as BIBLE_BOOKS, so its abbreviations map one to one."""
    kjv_books = json.loads(KJV_BIBLE_PATH.read_text(encoding="utf-8-sig"))
    dataset_abbrevs = [kjv_book["abbrev"] for kjv_book in kjv_books]
    dataset_abbrev_by_english_name = {
        english_name: dataset_abbrev
        for (_aliases, english_name, _synodal_abbreviation), dataset_abbrev in zip(BIBLE_BOOKS, dataset_abbrevs)
    }

    return dataset_abbrev_by_english_name


def comparable_text(text):
    letters_only = re.sub(r"[^a-z]+", " ", text.lower()).strip()

    return letters_only


VERSION_LABEL = "(Синод.)"


def add_version_label(english_line, russian_line):
    """Put «(Синод.)» at the end of the Russian line when the English line ends with the KJV marker (glossary.md §2, rule 8)."""
    has_kjv_marker = bool(re.search(r"\bKJV\s*$", english_line.replace("*", "")))
    if not has_kjv_marker or russian_line.rstrip().endswith(VERSION_LABEL):
        return russian_line
    labelled_line = f"{russian_line.rstrip()} {VERSION_LABEL}"

    return labelled_line


def english_verse_body(english_line, english_ref):
    """The English verse text of a page file line, without the inline reference, the verse number, KJV and markdown."""
    verse_body = english_line[2:].replace("*", "")
    verse_body = re.sub(r"^" + re.escape(english_ref) + r"\s+", "", verse_body)
    verse_body = re.sub(r"^\d{1,3}\s+", "", verse_body)
    verse_body = re.sub(r"\s*\bKJV\b\s*$", "", verse_body)

    return verse_body


def fill_page(page_path, synodal_chapters, kjv_chapters, dataset_abbrev_by_english_name, report):
    page_lines = page_path.read_text(encoding="utf-8").split("\n")
    has_changes = False
    for line_index, page_line in enumerate(page_lines):
        marker_match = MARKER_RE.match(page_line)
        if not marker_match or marker_match["block_type"] not in ("reference", "kjv-verse"):
            continue
        english_line = page_lines[line_index + 1]
        russian_line_index = line_index + 2
        if page_lines[russian_line_index].strip():
            labelled_line = add_version_label(english_line, page_lines[russian_line_index])
            if labelled_line != page_lines[russian_line_index]:
                page_lines[russian_line_index] = labelled_line
                has_changes = True
                report["labelled"] += 1
            report["kept"] += 1
            continue
        location = f"{page_path.name} block {marker_match['block_id']}"
        english_ref_match = REF_RE.match(marker_match["english_ref"])
        english_book_name = BOOK_BY_ALIAS[normalize_book_name(english_ref_match["book"])][0]
        dataset_abbrev = dataset_abbrev_by_english_name[english_book_name]
        if dataset_abbrev not in synodal_chapters:
            report["missing_book"].append(f"{location}: {marker_match['english_ref']} ({english_book_name} is not in {SYNODAL_BIBLE_PATH.name})")
            continue
        if marker_match["block_type"] == "reference":
            page_lines[russian_line_index] = add_version_label(english_line, marker_match["synodal_ref"])
            has_changes = True
            report["references"] += 1
            continue
        chapter = int(english_ref_match["chapter"])
        verse = int(english_ref_match["verses"])
        kjv_chapter_verses = kjv_chapters[dataset_abbrev][chapter - 1]
        kjv_verse = kjv_chapter_verses[verse - 1] if verse <= len(kjv_chapter_verses) else ""
        english_body = english_verse_body(english_line, english_ref_match["book"] + f" {chapter}:{verse}")
        similarity = difflib.SequenceMatcher(None, comparable_text(english_body), comparable_text(kjv_verse)).ratio()
        tags = marker_match["tags"] or ""
        # the author's insertion inside a verse lowers the similarity without the verse being wrong
        min_similarity = MIN_KJV_SIMILARITY - (0.3 if "insertion" in tags else 0)
        if "partial" in tags:
            min_similarity = 0
        if similarity < min_similarity:
            report["mismatch"].append(f"{location}: {marker_match['english_ref']} matches the KJV verse only {similarity:.0%}")
            continue
        synodal_chapter, synodal_verse = kjv_to_synodal(english_book_name, chapter, verse)
        check_note = numbering_note(english_book_name, chapter, verse)
        synodal_chapter_verses = synodal_chapters[dataset_abbrev][synodal_chapter - 1]
        if synodal_verse > len(synodal_chapter_verses):
            report["missing_verse"].append(f"{location}: {synodal_chapter}:{synodal_verse} of {english_book_name} is not in {SYNODAL_BIBLE_PATH.name}")
            continue
        synodal_text = synodal_chapter_verses[synodal_verse - 1]
        is_inline_reference = "inline-reference" in tags
        has_verse_number = "no-verse-number" not in tags
        if is_inline_reference:
            verse_prefix = f"{marker_match['synodal_ref']} "
        elif has_verse_number:
            verse_prefix = f"{synodal_verse} "
        else:
            verse_prefix = ""
        russian_line = add_version_label(english_line, verse_prefix + synodal_text)
        if "partial" in tags:
            check_note = "the book quotes only part of this verse; shorten the Синодальный перевод verse to the matching part"
        if check_note:
            russian_line += f"\n<!-- check: {check_note} -->"
            report["check"].append(f"{location}: {check_note}")
        page_lines[russian_line_index] = russian_line
        has_changes = True
        report["verses"] += 1
    if has_changes:
        page_path.write_text("\n".join(page_lines), encoding="utf-8")


def main():
    synodal_chapters = load_bible(SYNODAL_BIBLE_PATH)
    kjv_chapters = load_bible(KJV_BIBLE_PATH)
    dataset_abbrev_by_english_name = build_dataset_abbrev_by_english_name()
    report = {"references": 0, "verses": 0, "kept": 0, "labelled": 0, "missing_book": [], "missing_verse": [], "mismatch": [], "check": []}
    page_paths = sorted(PAGES_DIR.glob("*.md"))
    for page_path in page_paths:
        fill_page(page_path, synodal_chapters, kjv_chapters, dataset_abbrev_by_english_name, report)
    print(f"filled {report['references']} references and {report['verses']} verses; kept {report['kept']} already filled, of which {report['labelled']} got the {VERSION_LABEL} label")
    for report_key in ("missing_book", "missing_verse", "mismatch", "check"):
        print(f"{report_key}: {len(report[report_key])}")
        for report_line in report[report_key]:
            print("  " + report_line)


if __name__ == "__main__":
    main()
