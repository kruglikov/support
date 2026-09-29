"""Split the Dominion Life PDF into tagged per-page Markdown files and write the translation plan.

Writes, next to the PDF:
  pages/NNN.md           one file per PDF page; every text block is tagged with its type and quoted with "> "
  pages/NNN.blocks.json  the geometry of every block, used later to write the Russian text back into the PDF
  translation-plan.md    the decisions to review before translating, and the inventory of every page

A pages/NNN.md that already contains translated text is never overwritten.

Run with the interpreter that has PyMuPDF:
  ~/.local/share/pipx/venvs/pymupdf/bin/python God/tools/extract_pages.py
"""

import datetime
import json
import pathlib
import re

import pymupdf

GOD_DIR = pathlib.Path(__file__).resolve().parent.parent
SOURCE_PDF_PATH = GOD_DIR / "Dominion_Life_Manual_Updates_2024.pdf"
GLOSSARY_PATH = GOD_DIR / "glossary.md"
PAGES_DIR = GOD_DIR / "pages"
PLAN_PATH = GOD_DIR / "translation-plan.md"

TOC_PDF_PAGE = 4
KEEP_ENGLISH_PDF_PAGES = {3}
FOOTER_MARKER = "Reproduction Prohibited"
FOOTER_TOP_Y = 740
HEADING_MIN_SIZE = 16
PARAGRAPH_GAP_RATIO = 0.6
FULL_PAGE_BOTTOM_Y = 700
FULL_PAGE_MIN_WORDS = 200
FRONT_MATTER_CHAPTER = "Front matter"

# Quotations that end with "KJV" but carry no reference line, identified by searching bible/en_kjv.json.
# (PDF page, block number) -> (book, chapter, verse, the block quotes only part of the verse)
IDENTIFIED_KJV_QUOTES = {
    (19, 10): ("Ps", 138, 2, False),
    (34, 6): ("Col", 2, 15, False),
    (44, 3): ("Rom", 5, 17, False),
    (44, 5): ("Eccl", 8, 4, False),
    (61, 8): ("Mark", 11, 23, False),
    (65, 2): ("1 Cor", 14, 33, False),
    (74, 3): ("Gal", 2, 20, False),
    (77, 12): ("Matt", 8, 17, False),
    (96, 4): ("Acts", 3, 16, True),
    (96, 6): ("Acts", 3, 6, False),
}

SEPARATOR_RE = re.compile(r"^_{5,}$")
# the PDF sets "fi", "fl", "ff" as single ligature characters, which would break word matching ("sacriﬁce" ≠ "sacrifice")
LIGATURE_TABLE = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"})
REFERENCE_RE = re.compile(
    r"^(?P<book>(?:[1-3]\s?)?[A-Z][a-z]+\.?(?:\s(?:of\s)?[A-Z][a-z]+)?)\s+"
    r"(?P<chapter>\d+):(?P<verses>\d+(?:\s?[-–]\s?\d+)?(?:,\s?\d+(?:\s?[-–]\s?\d+)?)*)(?:\s+KJV)?$"
)
VERSE_START_RE = re.compile(r"^(?P<verse>\d{1,3})\s")
STRONGS_RE = re.compile(
    r"^(?:(?P<headword>[A-Z][\w ]*?)\s+(?:-\s+)?)?(?P<testament>OT|NT):\s?(?P<number>\d+)"
    r"(?:\s+(?:OT|NT):\s?\d+)?\s+(?:-\s+)?(?P<word>[a-z][^\s(;]*)"
)
INLINE_REFERENCE_RE = re.compile(r"^(?P<book>(?:[1-3]\s?)?[A-Z][a-z]+\.?)\s+(?P<chapter>\d+):(?P<verse>\d+)\s+(?=[A-Z])")
INLINE_STRONGS_RE = re.compile(r"\b(?P<testament>OT|NT):\s?(?P<number>\d+)\s+-\s+(?P<word>[a-z][^\s(;]*)")
KJV_ENDING_RE = re.compile(r"\bKJV\s*$")
TOC_ENTRY_RE = re.compile(r"^(?P<title>.+?)\s*\.{4,}\s*(?P<printed_page>\d+)$")

# (aliases as the book may write them, English name, Синодальный перевод abbreviation)
BIBLE_BOOKS = [
    (("Gen", "Genesis"), "Genesis", "Быт."),
    (("Ex", "Exo", "Exod", "Exodus"), "Exodus", "Исх."),
    (("Lev", "Leviticus"), "Leviticus", "Лев."),
    (("Num", "Numbers"), "Numbers", "Чис."),
    (("Deut", "Deu", "Deuteronomy"), "Deuteronomy", "Втор."),
    (("Josh", "Joshua"), "Joshua", "Нав."),
    (("Judg", "Judges"), "Judges", "Суд."),
    (("Ruth",), "Ruth", "Руфь"),
    (("1 Sam", "1 Samuel"), "1 Samuel", "1 Цар."),
    (("2 Sam", "2 Samuel"), "2 Samuel", "2 Цар."),
    (("1 Kgs", "1 Kings"), "1 Kings", "3 Цар."),
    (("2 Kgs", "2 Kings"), "2 Kings", "4 Цар."),
    (("1 Chr", "1 Chron", "1 Chronicles"), "1 Chronicles", "1 Пар."),
    (("2 Chr", "2 Chron", "2 Chronicles"), "2 Chronicles", "2 Пар."),
    (("Ezra",), "Ezra", "Езд."),
    (("Neh", "Nehemiah"), "Nehemiah", "Неем."),
    (("Esth", "Esther"), "Esther", "Есф."),
    (("Job",), "Job", "Иов"),
    (("Ps", "Psa", "Psalm", "Psalms"), "Psalms", "Пс."),
    (("Prov", "Proverbs"), "Proverbs", "Притч."),
    (("Eccl", "Eccles", "Ecclesiastes"), "Ecclesiastes", "Еккл."),
    (("Song", "Song of Solomon"), "Song of Solomon", "Песн."),
    (("Isa", "Isaiah"), "Isaiah", "Ис."),
    (("Jer", "Jeremiah"), "Jeremiah", "Иер."),
    (("Lam", "Lamentations"), "Lamentations", "Плач."),
    (("Ezek", "Ezekiel"), "Ezekiel", "Иез."),
    (("Dan", "Daniel"), "Daniel", "Дан."),
    (("Hos", "Hosea"), "Hosea", "Ос."),
    (("Joel",), "Joel", "Иоил."),
    (("Amos",), "Amos", "Ам."),
    (("Obad", "Obadiah"), "Obadiah", "Авд."),
    (("Jonah",), "Jonah", "Ион."),
    (("Mic", "Micah"), "Micah", "Мих."),
    (("Nah", "Nahum"), "Nahum", "Наум."),
    (("Hab", "Habakkuk"), "Habakkuk", "Авв."),
    (("Zeph", "Zephaniah"), "Zephaniah", "Соф."),
    (("Hag", "Haggai"), "Haggai", "Агг."),
    (("Zech", "Zechariah"), "Zechariah", "Зах."),
    (("Mal", "Malachi"), "Malachi", "Мал."),
    (("Matt", "Mat", "Mt", "Matthew"), "Matthew", "Мф."),
    (("Mark", "Mk"), "Mark", "Мк."),
    (("Luke", "Lk"), "Luke", "Лк."),
    (("John", "Jn"), "John", "Ин."),
    (("Acts",), "Acts", "Деян."),
    (("Rom", "Romans"), "Romans", "Рим."),
    (("1 Cor", "1 Corinthians"), "1 Corinthians", "1 Кор."),
    (("2 Cor", "2 Corinthians"), "2 Corinthians", "2 Кор."),
    (("Gal", "Galatians"), "Galatians", "Гал."),
    (("Eph", "Ephesians"), "Ephesians", "Еф."),
    (("Phil", "Philippians"), "Philippians", "Флп."),
    (("Col", "Colossians"), "Colossians", "Кол."),
    (("1 Thess", "1 Thessalonians"), "1 Thessalonians", "1 Фес."),
    (("2 Thess", "2 Thessalonians"), "2 Thessalonians", "2 Фес."),
    (("1 Tim", "1 Timothy"), "1 Timothy", "1 Тим."),
    (("2 Tim", "2 Timothy"), "2 Timothy", "2 Тим."),
    (("Titus", "Tit"), "Titus", "Тит."),
    (("Philem", "Phlm", "Philemon"), "Philemon", "Флм."),
    (("Heb", "Hebrews"), "Hebrews", "Евр."),
    (("Jas", "James"), "James", "Иак."),
    (("1 Pet", "1 Peter"), "1 Peter", "1 Пет."),
    (("2 Pet", "2 Peter"), "2 Peter", "2 Пет."),
    (("1 John", "1 Jn"), "1 John", "1 Ин."),
    (("2 John", "2 Jn"), "2 John", "2 Ин."),
    (("3 John", "3 Jn"), "3 John", "3 Ин."),
    (("Jude",), "Jude", "Иуд."),
    (("Rev", "Revelation"), "Revelation", "Откр."),
]


def normalize_book_name(book_name):
    normalized_name = re.sub(r"[\s.]", "", book_name).lower()

    return normalized_name


BOOK_BY_ALIAS = {
    normalize_book_name(alias): (english_name, synodal_abbreviation)
    for aliases, english_name, synodal_abbreviation in BIBLE_BOOKS
    for alias in aliases
}


def kjv_to_synodal(english_book_name, chapter, verse):
    """KJV chapter and verse → Синодальный перевод chapter and verse; a psalm title can still shift a Psalm verse."""
    if english_book_name == "Psalms":
        if chapter <= 8 or chapter >= 148:
            return chapter, verse
        if chapter == 9:
            return 9, verse + 1
        if chapter == 10:
            return 9, verse + 21
        if chapter == 114:
            return 113, verse
        if chapter == 115:
            return 113, verse + 8
        if chapter == 116:
            return (114, verse) if verse <= 9 else (115, verse - 9)
        if chapter == 147:
            return (146, verse) if verse <= 11 else (147, verse - 11)
        return chapter - 1, verse
    if english_book_name == "Romans" and chapter == 16 and verse >= 25:
        return 14, verse - 1
    if english_book_name == "2 Corinthians" and chapter == 13 and verse >= 13:
        return 13, verse - 1

    return chapter, verse


def numbering_note(english_book_name, chapter, first_verse):
    """A note for every verse the Синодальный перевод numbers differently, and for every Psalm verse."""
    synodal_chapter, synodal_verse = kjv_to_synodal(english_book_name, chapter, first_verse)
    if english_book_name == "Psalms":
        return f"KJV Psalm {chapter}:{first_verse} is Пс. {synodal_chapter}:{synodal_verse}; a psalm title can shift the verse, confirm it"
    if (synodal_chapter, synodal_verse) != (chapter, first_verse):
        return f"KJV {english_book_name} {chapter}:{first_verse} is {synodal_chapter}:{synodal_verse} in the Синодальный перевод"

    return None


def span_markdown(span):
    span_text = span["text"]
    stripped_text = span_text.strip()
    if not stripped_text:
        return span_text
    is_bold = "Bold" in span["font"] or bool(span["flags"] & 16)
    is_italic = "Italic" in span["font"] or bool(span["flags"] & 2)
    style_marker = ("**" if is_bold else "") + ("*" if is_italic else "")
    if not style_marker:
        return span_text
    leading_space = span_text[: len(span_text) - len(span_text.lstrip())]
    trailing_space = span_text[len(span_text.rstrip()):]
    marked_text = f"{leading_space}{style_marker}{stripped_text}{style_marker[::-1]}{trailing_space}"

    return marked_text


def join_markdown(fragments):
    joined_text = "".join(fragments)
    # "**a** **b**" -> "**a b**": neighbouring spans with the same style become one marked run
    merged_text = re.sub(r"\*\*(\s*)\*\*", r"\1", joined_text)
    merged_text = re.sub(r"(?<!\*)\*(\s+)\*(?!\*)", r"\1", merged_text)

    return merged_text.strip()


def read_page_lines(page):
    """Every non-empty text line of the page, top to bottom, with its markdown text and geometry."""
    page_lines = []
    page_dict = page.get_text("dict")
    text_blocks = [block for block in page_dict["blocks"] if block["type"] == 0]
    for block in text_blocks:
        for line in block["lines"]:
            line_spans = line["spans"]
            for span in line_spans:
                span["text"] = span["text"].translate(LIGATURE_TABLE)
            plain_text = "".join(span["text"] for span in line_spans).strip()
            if not plain_text:
                continue
            visible_spans = [span for span in line_spans if span["text"].strip()]
            first_span = visible_spans[0]
            page_lines.append({
                "plain": re.sub(r"\s+", " ", plain_text),
                "markdown": join_markdown(span_markdown(span) for span in line_spans),
                "bbox": [round(value, 2) for value in line["bbox"]],
                "origin": [round(value, 2) for value in first_span["origin"]],
                "size": round(max(span["size"] for span in visible_spans), 2),
                "font": first_span["font"],
                "color": first_span["color"],
                "is_bold": all("Bold" in span["font"] or span["flags"] & 16 for span in visible_spans),
            })
    page_lines.sort(key=lambda page_line: (round(page_line["bbox"][1]), page_line["bbox"][0]))

    return page_lines


def is_reference_line(plain_text):
    reference_match = REFERENCE_RE.match(plain_text)
    is_reference = bool(reference_match) and normalize_book_name(reference_match["book"]) in BOOK_BY_ALIAS

    return is_reference


def is_inline_reference_line(plain_text):
    inline_reference_match = INLINE_REFERENCE_RE.match(plain_text)
    is_inline_reference = bool(inline_reference_match) and normalize_book_name(inline_reference_match["book"]) in BOOK_BY_ALIAS

    return is_inline_reference


def split_paragraphs(content_lines):
    paragraphs = []
    current_lines = []
    previous_line = None
    for line in content_lines:
        if SEPARATOR_RE.match(line["plain"]):
            if current_lines:
                paragraphs.append(current_lines)
            current_lines = []
            previous_line = None
            continue
        starts_new_paragraph = (
            previous_line is None
            or line["bbox"][1] - previous_line["bbox"][3] > PARAGRAPH_GAP_RATIO * line["size"]
            or abs(line["size"] - previous_line["size"]) > 1
            or is_reference_line(line["plain"])
            or is_reference_line(previous_line["plain"])
            or bool(STRONGS_RE.match(line["plain"]))
            or is_inline_reference_line(line["plain"])
        )
        if starts_new_paragraph and current_lines:
            paragraphs.append(current_lines)
            current_lines = []
        current_lines.append(line)
        previous_line = line
    if current_lines:
        paragraphs.append(current_lines)

    return paragraphs


def read_pdf_pages(document):
    pdf_pages = []
    for page_index, page in enumerate(document):
        page_lines = read_page_lines(page)
        printed_page = None
        content_lines = []
        for line in page_lines:
            if FOOTER_MARKER in line["plain"]:
                continue
            if line["plain"].isdigit() and line["bbox"][1] > FOOTER_TOP_Y:
                printed_page = int(line["plain"])
                continue
            content_lines.append(line)
        pdf_pages.append({
            "pdf_page": page_index + 1,
            "printed_page": printed_page,
            "image_count": len(page.get_images()),
            "paragraphs": split_paragraphs(content_lines),
        })

    return pdf_pages


def read_chapters(pdf_pages):
    """Chapter start pages from the table of contents, converted from printed to PDF page numbers."""
    pdf_page_by_printed_page = {
        pdf_page["printed_page"]: pdf_page["pdf_page"] for pdf_page in pdf_pages if pdf_page["printed_page"]
    }
    toc_page = pdf_pages[TOC_PDF_PAGE - 1]
    chapters = []
    for paragraph_lines in toc_page["paragraphs"]:
        toc_text = " ".join(line["plain"] for line in paragraph_lines)
        toc_match = TOC_ENTRY_RE.match(toc_text)
        if not toc_match:
            continue
        printed_page = int(toc_match["printed_page"])
        chapters.append({
            "title": re.sub(r"\s+", " ", toc_match["title"]).strip(),
            "printed_page": printed_page,
            "pdf_page": pdf_page_by_printed_page.get(printed_page, printed_page + 1),
        })

    return chapters


def chapter_title_for_page(chapters, pdf_page_number):
    started_chapters = [chapter for chapter in chapters if chapter["pdf_page"] <= pdf_page_number]
    chapter_title = started_chapters[-1]["title"] if started_chapters else FRONT_MATTER_CHAPTER

    return chapter_title


def synodal_verses_text(english_book_name, chapter, verses_text):
    """The chapter and verses of a KJV reference, renumbered to the Синодальный перевод where the numbering differs."""
    verse_numbers = [int(number) for number in re.findall(r"\d+", verses_text)]
    first_chapter, first_verse = kjv_to_synodal(english_book_name, chapter, verse_numbers[0])
    last_chapter, last_verse = kjv_to_synodal(english_book_name, chapter, verse_numbers[-1])
    is_renumbered = (first_chapter, first_verse, last_chapter, last_verse) != (chapter, verse_numbers[0], chapter, verse_numbers[-1])
    if not is_renumbered:
        synodal_text = f"{chapter}:{verses_text}"
    elif len(verse_numbers) == 1:
        synodal_text = f"{first_chapter}:{first_verse}"
    elif first_chapter == last_chapter:
        synodal_text = f"{first_chapter}:{first_verse}-{last_verse}"
    else:
        synodal_text = f"{first_chapter}:{first_verse}–{last_chapter}:{last_verse}"

    return synodal_text


def passage_label(passage, verses_text):
    english_label = f"{passage['book_alias']} {passage['chapter']}:{verses_text}"
    synodal_chapter_and_verses = synodal_verses_text(passage["english_book_name"], passage["chapter"], verses_text)
    synodal_label = f"{passage['synodal_abbreviation']} {synodal_chapter_and_verses}"
    label = f"{english_label} → {synodal_label}"

    return label


def classify_blocks(pdf_pages, chapters):
    """Give every paragraph a block type and tags; the current Bible passage carries over page breaks."""
    current_passage = None
    for pdf_page in pdf_pages:
        pdf_page_number = pdf_page["pdf_page"]
        pdf_page["chapter"] = chapter_title_for_page(chapters, pdf_page_number)
        blocks = []
        for paragraph_lines in pdf_page["paragraphs"]:
            plain_text = " ".join(line["plain"] for line in paragraph_lines)
            markdown_text = join_markdown(" ".join(line["markdown"] for line in paragraph_lines))
            block = {
                "id": len(blocks) + 1,
                "type": "prose",
                "tags": [],
                "plain": plain_text,
                "markdown": markdown_text,
                "words": len(plain_text.split()),
                "lines": paragraph_lines,
            }
            blocks.append(block)
            reference_match = REFERENCE_RE.match(plain_text)
            strongs_match = STRONGS_RE.match(plain_text)
            verse_match = VERSE_START_RE.match(plain_text)
            identified_quote = IDENTIFIED_KJV_QUOTES.get((pdf_page_number, block["id"]))
            if pdf_page_number in KEEP_ENGLISH_PDF_PAGES:
                block["type"] = "keep-english"
            elif pdf_page_number == TOC_PDF_PAGE:
                block["type"] = "toc"
            elif identified_quote:
                book_alias, chapter, verse, is_partial = identified_quote
                english_book_name, synodal_abbreviation = BOOK_BY_ALIAS[normalize_book_name(book_alias)]
                quote_passage = {
                    "book_alias": book_alias,
                    "english_book_name": english_book_name,
                    "synodal_abbreviation": synodal_abbreviation,
                    "chapter": chapter,
                }
                block["type"] = "kjv-verse"
                block["passage"] = passage_label(quote_passage, str(verse))
                block["tags"] += [block["passage"], "identified-quote", "no-verse-number"] + (["partial"] if is_partial else [])
                block["numbering_note"] = numbering_note(english_book_name, chapter, verse)
                current_passage = None
            elif max(line["size"] for line in paragraph_lines) >= HEADING_MIN_SIZE:
                block["type"] = "heading"
                current_passage = None
            elif reference_match and is_reference_line(plain_text):
                english_book_name, synodal_abbreviation = BOOK_BY_ALIAS[normalize_book_name(reference_match["book"])]
                verse_numbers = [int(number) for number in re.findall(r"\d+", reference_match["verses"])]
                current_passage = {
                    "book_alias": reference_match["book"],
                    "english_book_name": english_book_name,
                    "synodal_abbreviation": synodal_abbreviation,
                    "chapter": int(reference_match["chapter"]),
                    "first_verse": min(verse_numbers),
                    "last_verse": max(verse_numbers),
                }
                block["type"] = "reference"
                block["passage"] = passage_label(current_passage, reference_match["verses"])
                block["tags"].append(block["passage"])
                block["numbering_note"] = numbering_note(english_book_name, current_passage["chapter"], current_passage["first_verse"])
            elif strongs_match:
                block["type"] = "strongs"
                testament_prefix = "ВЗ" if strongs_match["testament"] == "OT" else "НЗ"
                block["strongs"] = f"{strongs_match['testament']}:{strongs_match['number']} {strongs_match['word']}"
                block["strongs_entries"] = [f"{strongs_match['testament']}:{strongs_match['number']}"]
                block["tags"].append(f"{strongs_match['testament']}:{strongs_match['number']} → Стронг {testament_prefix}:{strongs_match['number']} · {strongs_match['word']}")
                if strongs_match["headword"]:
                    block["tags"].append(f"headword {strongs_match['headword']}")
                current_passage = None
            elif is_inline_reference_line(plain_text):
                inline_reference_match = INLINE_REFERENCE_RE.match(plain_text)
                english_book_name, synodal_abbreviation = BOOK_BY_ALIAS[normalize_book_name(inline_reference_match["book"])]
                verse_number = int(inline_reference_match["verse"])
                # an inline reference names one verse; the numbered verses that may follow have no known end
                current_passage = {
                    "book_alias": inline_reference_match["book"],
                    "english_book_name": english_book_name,
                    "synodal_abbreviation": synodal_abbreviation,
                    "chapter": int(inline_reference_match["chapter"]),
                    "first_verse": verse_number,
                    "last_verse": None,
                }
                block["type"] = "kjv-verse"
                block["passage"] = passage_label(current_passage, str(verse_number))
                block["tags"] += [block["passage"], "inline-reference"]
                block["numbering_note"] = numbering_note(english_book_name, current_passage["chapter"], verse_number)
                if "**" in markdown_text:
                    block["tags"].append("emphasis")
                if "(" in plain_text or "[" in plain_text:
                    block["tags"].append("insertion")
            elif current_passage and verse_match:
                verse_number = int(verse_match["verse"])
                block["type"] = "kjv-verse"
                block["passage"] = passage_label(current_passage, str(verse_number))
                block["tags"].append(block["passage"])
                block["numbering_note"] = numbering_note(current_passage["english_book_name"], current_passage["chapter"], verse_number)
                has_passage_end = current_passage["last_verse"] is not None
                if has_passage_end and not current_passage["first_verse"] <= verse_number <= current_passage["last_verse"]:
                    block["tags"].append("outside-passage-range")
                if "**" in markdown_text:
                    block["tags"].append("emphasis")
                if "(" in plain_text or "[" in plain_text:
                    block["tags"].append("insertion")
            elif KJV_ENDING_RE.search(plain_text):
                block["type"] = "kjv-quote"
                block["tags"].append("reference-unknown")
                current_passage = None
            elif all(line["is_bold"] for line in paragraph_lines) and block["words"] <= 15:
                block["type"] = "subheading"
                current_passage = None
            else:
                current_passage = None
            if block["type"] != "strongs":
                inline_strongs_matches = list(INLINE_STRONGS_RE.finditer(plain_text))
                block["strongs_entries"] = [
                    f"{inline_match['testament']}:{inline_match['number']}" for inline_match in inline_strongs_matches
                ]
                for inline_match in inline_strongs_matches:
                    testament_prefix = "ВЗ" if inline_match["testament"] == "OT" else "НЗ"
                    block["tags"].append(f"inline Стронг {testament_prefix}:{inline_match['number']} · {inline_match['word']}")
            if block.get("numbering_note"):
                block["tags"].append("numbering")
        pdf_page["blocks"] = blocks


def load_glossary_terms():
    """Rows of the §1 Terms table of glossary.md, each with a search pattern for the English term."""
    glossary_lines = GLOSSARY_PATH.read_text(encoding="utf-8").splitlines()
    glossary_terms = []
    is_in_terms_section = False
    for glossary_line in glossary_lines:
        if glossary_line.startswith("## "):
            is_in_terms_section = glossary_line.startswith("## 1.")
            continue
        is_term_row = glossary_line.startswith("| ") and not glossary_line.startswith(("| English", "|---"))
        if not is_in_terms_section or not is_term_row:
            continue
        cells = [cell.strip() for cell in glossary_line.strip().strip("|").split("|")]
        english_term, russian_term, english_in_brackets, _strongs, _source, status = cells
        search_words = re.sub(r"\(.*?\)", "", english_term)
        search_words = re.sub(r"^(a|to)\s+", "", search_words.strip()).split()
        search_pattern = re.compile(r"\b" + r"\s+".join(re.escape(word) for word in search_words) + r"(?:s|es)?\b", re.IGNORECASE)
        glossary_terms.append({
            "english": english_term,
            "russian": russian_term,
            "shows_english": english_in_brackets == "yes",
            "status": status,
            "pattern": search_pattern,
        })

    return glossary_terms


def has_translation(markdown_path):
    """True when a page file holds any line besides front matter, block markers and quoted English."""
    if not markdown_path.exists():
        return False
    file_lines = markdown_path.read_text(encoding="utf-8").splitlines()
    front_matter_end = file_lines.index("---", 1) if file_lines[:1] == ["---"] else -1
    body_lines = file_lines[front_matter_end + 1:]
    translated_lines = [
        body_line for body_line in body_lines
        if body_line.strip() and not body_line.startswith(("<!--", ">"))
    ]
    has_translated_lines = bool(translated_lines)

    return has_translated_lines


def render_page_markdown(pdf_page):
    printed_page = pdf_page["printed_page"] if pdf_page["printed_page"] is not None else "none"
    chapter_title = pdf_page["chapter"].replace('"', '\\"')
    markdown_lines = [
        "---",
        f"pdf_page: {pdf_page['pdf_page']}",
        f"printed_page: {printed_page}",
        f'chapter: "{chapter_title}"',
        "---",
        "",
    ]
    page_blocks = pdf_page["blocks"]
    if not page_blocks:
        markdown_lines += ["<!-- no text to translate on this page besides the footer -->", ""]
    for block in page_blocks:
        marker_parts = [f"block {block['id']}", block["type"]] + block["tags"]
        markdown_lines += [f"<!-- {' · '.join(marker_parts)} -->", f"> {block['markdown']}", "", ""]
    page_markdown = "\n".join(markdown_lines)

    return page_markdown


def render_blocks_json(pdf_page):
    page_geometry = {
        "pdf_page": pdf_page["pdf_page"],
        "printed_page": pdf_page["printed_page"],
        "blocks": [
            {
                "id": block["id"],
                "type": block["type"],
                "bbox": [
                    min(line["bbox"][0] for line in block["lines"]),
                    min(line["bbox"][1] for line in block["lines"]),
                    max(line["bbox"][2] for line in block["lines"]),
                    max(line["bbox"][3] for line in block["lines"]),
                ],
                "lines": [
                    {key: line[key] for key in ("bbox", "origin", "size", "font", "color", "is_bold")}
                    for line in block["lines"]
                ],
            }
            for block in pdf_page["blocks"]
        ],
    }
    blocks_json = json.dumps(page_geometry, ensure_ascii=False, indent=1)

    return blocks_json


def page_link(pdf_page_number):
    link = f"[{pdf_page_number:03d}](pages/{pdf_page_number:03d}.md)"

    return link


def find_term_occurrences(pdf_pages, glossary_terms):
    """For every glossary term: the blocks where it occurs, split into the author's text and Bible verses."""
    author_text_types = {"prose", "heading", "subheading", "strongs"}
    bible_text_types = {"kjv-verse", "kjv-quote"}
    term_occurrences = {term["english"]: {"author": [], "bible": []} for term in glossary_terms}
    for pdf_page in pdf_pages:
        for block in pdf_page["blocks"]:
            for term in glossary_terms:
                if not term["pattern"].search(block["plain"]):
                    continue
                occurrence = (pdf_page["pdf_page"], block["id"], pdf_page["chapter"])
                if block["type"] in author_text_types:
                    term_occurrences[term["english"]]["author"].append(occurrence)
                elif block["type"] in bible_text_types:
                    term_occurrences[term["english"]]["bible"].append(occurrence)

    return term_occurrences


def summarize_page_blocks(page_blocks):
    """Compress the block list of a page into runs, e.g. "b3–b5 kjv-verse Gen 1:26–28"."""
    block_runs = []
    for block in page_blocks:
        run_key = (block["type"], block.get("passage", "").split(":")[0] if block["type"] == "kjv-verse" else block["id"])
        if block["type"] == "prose":
            run_key = ("prose",)
        if block_runs and block_runs[-1]["key"] == run_key:
            block_runs[-1]["blocks"].append(block)
        else:
            block_runs.append({"key": run_key, "blocks": [block]})
    run_labels = []
    for block_run in block_runs:
        run_blocks = block_run["blocks"]
        first_block, last_block = run_blocks[0], run_blocks[-1]
        block_range = f"b{first_block['id']}" if first_block is last_block else f"b{first_block['id']}–b{last_block['id']}"
        run_detail = ""
        if first_block["type"] == "kjv-verse":
            first_label = first_block["passage"].split(" → ")[0]
            last_verse = last_block["passage"].split(" → ")[0].split(":")[-1]
            run_detail = first_label if first_block is last_block else f"{first_label}–{last_verse}"
        elif first_block["type"] == "reference":
            run_detail = first_block["passage"].split(" → ")[0]
        elif first_block["type"] == "strongs":
            run_detail = first_block["strongs"]
        run_label = " ".join(part for part in (block_range, first_block["type"], run_detail) if part)
        run_labels.append(run_label)
    page_summary = " · ".join(run_labels) if run_labels else "footer only"

    return page_summary


def render_plan(pdf_pages, chapters, glossary_terms, page_file_results):
    all_blocks = [(pdf_page, block) for pdf_page in pdf_pages for block in pdf_page["blocks"]]
    blocks_by_type = {}
    for _pdf_page, block in all_blocks:
        blocks_by_type.setdefault(block["type"], []).append(block)
    term_occurrences = find_term_occurrences(pdf_pages, glossary_terms)
    translatable_types = {"prose", "heading", "subheading", "toc"}
    plan_lines = [
        "# Dominion Life — translation plan",
        "",
        f"Generated on {datetime.date.today().isoformat()} by `God/tools/extract_pages.py` from `God/Dominion_Life_Manual_Updates_2024.pdf` and `God/glossary.md`. Regenerate after changing the glossary: `~/.local/share/pipx/venvs/pymupdf/bin/python God/tools/extract_pages.py` (page files that already hold a translation are kept).",
        "",
        "Part 1 lists only what needs a decision before translating. Part 2 is the inventory of every page. Each page file `pages/NNN.md` holds the English text of PDF page NNN as tagged blocks.",
        "",
        "## How to translate a page file",
        "",
        "Each block of `pages/NNN.md` is a marker line, the English text quoted with `> `, and an empty line below it. Write the Russian text of the block on the empty line under its English text, as one line per paragraph, and keep the marker and the `> ` line unchanged: the marker's block number ties the Russian text to the rectangle of the English text in `pages/NNN.blocks.json`. `**bold**` and `*italic*` mark the author's emphasis; mark the corresponding Russian words the same way.",
        "",
        "| Block type | What to write under it |",
        "|---|---|",
        "| `heading`, `subheading`, `prose` | the translation of the author's text, using the terms of `glossary.md` §1 |",
        "| `reference` | the Синодальный перевод reference shown in the marker, for example `Быт. 1:26-28` |",
        "| `kjv-verse` | the verse from the Синодальный перевод (reference in the marker), not a translation of the English verse; keep the verse number in front |",
        "| `kjv-quote` | the verse from the Синодальный перевод, once its reference is identified (Part 1.4) |",
        "| `strongs` | the entry rebuilt to the pattern of `glossary.md` §3 |",
        "| `toc` | the translated chapter title and its page number |",
        "| `keep-english` | nothing — the block stays in English |",
        "",
        "## Part 1. Decisions before translating",
        "",
        "### 1.1 Open glossary terms (status `decide` in `glossary.md` §1)",
        "",
        "A page that contains an open term in the author's text waits until the term is decided. Inside Bible verses the Синодальный перевод wording is used anyway, so verse occurrences do not block a page.",
        "",
        "| Term | Proposed Russian | Pages, author's text | Pages, Bible verses only |",
        "|---|---|---|---|",
    ]
    open_terms = [term for term in glossary_terms if term["status"].startswith("decide")]
    for term in open_terms:
        occurrences = term_occurrences[term["english"]]
        author_pages = sorted({occurrence[0] for occurrence in occurrences["author"]})
        bible_pages = sorted({occurrence[0] for occurrence in occurrences["bible"]} - set(author_pages))
        author_pages_text = ", ".join(page_link(page_number) for page_number in author_pages) or "—"
        bible_pages_text = ", ".join(page_link(page_number) for page_number in bible_pages) or "—"
        plan_lines.append(f"| {term['english']} | {term['russian']} | {author_pages_text} | {bible_pages_text} |")

    plan_lines += [
        "",
        "### 1.2 Footer text (translated once, used on every page)",
        "",
        "English: `Dominion Life Manual Reproduction Prohibited © jglm.org`. Proposed Russian: `Пособие „Жизнь во владычестве“. Воспроизведение запрещено © jglm.org`. Status: approved (`glossary.md` §5).",
        "",
        "### 1.3 Strong's entries (`glossary.md` §3)",
        "",
        "An entry is either a block of its own (`strongs`) or embedded in another block, such as the author's insertion inside a verse (`inline`).",
        "",
        "| Page | Block | Block type | Entry | Also quoted on |",
        "|---|---|---|---|---|",
    ]
    strongs_blocks = [(pdf_page, block) for pdf_page, block in all_blocks if block.get("strongs_entries")]
    pages_by_strongs_number = {}
    for pdf_page, block in strongs_blocks:
        for strongs_number in block["strongs_entries"]:
            pages_by_strongs_number.setdefault(strongs_number, set()).add(pdf_page["pdf_page"])
    for pdf_page, block in strongs_blocks:
        block_strongs_numbers = block["strongs_entries"]
        other_pages = sorted(set().union(*(pages_by_strongs_number[number] for number in block_strongs_numbers)) - {pdf_page["pdf_page"]})
        other_pages_text = ", ".join(page_link(page_number) for page_number in other_pages) or "—"
        strongs_tags = [tag for tag in block["tags"] if "Стронг" in tag or tag.startswith("headword")]
        plan_lines.append(f"| {page_link(pdf_page['pdf_page'])} | {block['id']} | {block['type']} | {' · '.join(strongs_tags)} | {other_pages_text} |")

    plan_lines += [
        "",
        "### 1.4 Bible passages and their Синодальный перевод references",
        "",
        "Every `reference` block with the verses that follow it. The column \"Numbering\" is filled only for the known places where the Синодальный перевод numbers the verse differently; every verse is still checked when its Russian text is inserted.",
        "",
        "| Page | Block | KJV → Синодальный перевод | Verses on the page | Numbering |",
        "|---|---|---|---|---|",
    ]
    for pdf_page in pdf_pages:
        page_blocks = pdf_page["blocks"]
        for block_index, block in enumerate(page_blocks):
            if block["type"] != "reference":
                continue
            following_verses = []
            for following_block in page_blocks[block_index + 1:]:
                if following_block["type"] != "kjv-verse":
                    break
                following_verses.append(following_block["passage"].split(" → ")[0].split(":")[-1])
            verses_text = ", ".join(following_verses) or "— (continues on the next page)"
            plan_lines.append(f"| {page_link(pdf_page['pdf_page'])} | {block['id']} | {block['passage']} | {verses_text} | {block.get('numbering_note') or ''} |")
    continued_verse_pages = [
        pdf_page for pdf_page in pdf_pages
        if pdf_page["blocks"] and pdf_page["blocks"][0]["type"] == "kjv-verse"
    ]
    for pdf_page in continued_verse_pages:
        first_block = pdf_page["blocks"][0]
        plan_lines.append(f"| {page_link(pdf_page['pdf_page'])} | {first_block['id']} | {first_block['passage']} (continued from the previous page) | | {first_block.get('numbering_note') or ''} |")

    plan_lines += [
        "",
        "### 1.5 Quotations ending with \"KJV\" whose reference was not found",
        "",
        "The reference of each quotation below must be identified before the Синодальный перевод text can replace it.",
        "",
        "| Page | Block | Words |",
        "|---|---|---|",
    ]
    for pdf_page, block in all_blocks:
        if block["type"] == "kjv-quote":
            plan_lines.append(f"| {page_link(pdf_page['pdf_page'])} | {block['id']} | {block['words']} |")

    plan_lines += [
        "",
        "### 1.6 Verses with the author's emphasis or insertions",
        "",
        "`emphasis`: the author bolds words inside the verse, so the corresponding words of the Синодальный перевод verse must be bolded too. `insertion`: the verse contains the author's words in parentheses or brackets, which are translated and placed at the same point of the Russian verse (`glossary.md` §2, rule 6).",
        "",
        "| Page | Block | Verse | Flags |",
        "|---|---|---|---|",
    ]
    for pdf_page, block in all_blocks:
        verse_flags = [tag for tag in block["tags"] if tag in ("emphasis", "insertion", "outside-passage-range")]
        if block["type"] == "kjv-verse" and verse_flags:
            plan_lines.append(f"| {page_link(pdf_page['pdf_page'])} | {block['id']} | {block['passage']} | {', '.join(verse_flags)} |")

    plan_lines += [
        "",
        "### 1.7 English in brackets: first occurrence per chapter",
        "",
        "For terms marked `EN = yes` in `glossary.md` §1, the English original is added in round brackets at the first occurrence in the author's text of each chapter, listed here.",
        "",
        "| Term | Russian | First occurrence per chapter (page · block) |",
        "|---|---|---|",
    ]
    bracket_terms = [term for term in glossary_terms if term["shows_english"]]
    for term in bracket_terms:
        first_occurrences = {}
        for pdf_page_number, block_id, chapter_title in term_occurrences[term["english"]]["author"]:
            first_occurrences.setdefault(chapter_title, (pdf_page_number, block_id))
        first_occurrences_text = "; ".join(
            f"{page_link(pdf_page_number)} · b{block_id}" for pdf_page_number, block_id in first_occurrences.values()
        ) or "—"
        plan_lines.append(f"| {term['english']} | {term['russian']} | {first_occurrences_text} |")

    image_pages = [pdf_page for pdf_page in pdf_pages if pdf_page["image_count"]]
    full_pages = [
        pdf_page for pdf_page in pdf_pages
        if pdf_page["blocks"]
        and max(line["bbox"][3] for block in pdf_page["blocks"] for line in block["lines"]) > FULL_PAGE_BOTTOM_Y
        and sum(block["words"] for block in pdf_page["blocks"]) >= FULL_PAGE_MIN_WORDS
    ]
    footer_only_pages = [pdf_page for pdf_page in pdf_pages if not pdf_page["blocks"]]
    plan_lines += [
        "",
        "### 1.8 Pages with images",
        "",
        "Text inside an image cannot be replaced; check each page visually for such text.",
        "",
        ", ".join(f"{page_link(pdf_page['pdf_page'])} ({pdf_page['image_count']})" for pdf_page in image_pages) or "none",
        "",
        "### 1.9 Full pages",
        "",
        f"Text reaches below y = {FULL_PAGE_BOTTOM_Y} pt with at least {FULL_PAGE_MIN_WORDS} words. Russian text runs 10–20% longer, so these pages will need a smaller font size or tighter line spacing when the PDF is rebuilt.",
        "",
        ", ".join(page_link(pdf_page["pdf_page"]) for pdf_page in full_pages) or "none",
        "",
        "### 1.10 Pages with nothing to translate",
        "",
        "Footer only: " + (", ".join(page_link(pdf_page["pdf_page"]) for pdf_page in footer_only_pages) or "none") + ". Kept in English (`glossary.md` §6): " + ", ".join(page_link(page_number) for page_number in sorted(KEEP_ENGLISH_PDF_PAGES)) + ".",
        "",
        "## Part 2. Inventory of every page",
        "",
        "Blocks by type across the book: " + ", ".join(f"`{block_type}` {len(type_blocks)}" for block_type, type_blocks in sorted(blocks_by_type.items())) + ". \"Words to translate\" counts the author's text only; Bible verses are replaced from the Синодальный перевод and are not counted.",
        "",
    ]
    chapter_titles = [FRONT_MATTER_CHAPTER] + [chapter["title"] for chapter in chapters]
    for chapter_title in chapter_titles:
        chapter_pages = [pdf_page for pdf_page in pdf_pages if pdf_page["chapter"] == chapter_title]
        if not chapter_pages:
            continue
        plan_lines += [
            f"### {chapter_title}",
            "",
            "| PDF page | Printed | Words to translate | Blocks | Page file |",
            "|---|---|---|---|---|",
        ]
        for pdf_page in chapter_pages:
            words_to_translate = sum(block["words"] for block in pdf_page["blocks"] if block["type"] in translatable_types)
            printed_page = pdf_page["printed_page"] or "—"
            plan_lines.append(
                f"| {page_link(pdf_page['pdf_page'])} | {printed_page} | {words_to_translate} | {summarize_page_blocks(pdf_page['blocks'])} | {page_file_results[pdf_page['pdf_page']]} |"
            )
        plan_lines.append("")
    plan_markdown = "\n".join(plan_lines)

    return plan_markdown


def main():
    document = pymupdf.open(SOURCE_PDF_PATH)
    pdf_pages = read_pdf_pages(document)
    chapters = read_chapters(pdf_pages)
    classify_blocks(pdf_pages, chapters)
    glossary_terms = load_glossary_terms()
    PAGES_DIR.mkdir(exist_ok=True)
    page_file_results = {}
    for pdf_page in pdf_pages:
        page_file_stem = f"{pdf_page['pdf_page']:03d}"
        markdown_path = PAGES_DIR / f"{page_file_stem}.md"
        (PAGES_DIR / f"{page_file_stem}.blocks.json").write_text(render_blocks_json(pdf_page), encoding="utf-8")
        if has_translation(markdown_path):
            page_file_results[pdf_page["pdf_page"]] = "kept (has translation)"
            continue
        markdown_path.write_text(render_page_markdown(pdf_page), encoding="utf-8")
        page_file_results[pdf_page["pdf_page"]] = "written"
    PLAN_PATH.write_text(render_plan(pdf_pages, chapters, glossary_terms, page_file_results), encoding="utf-8")
    kept_pages = [page_number for page_number, result in page_file_results.items() if result != "written"]
    print(f"{len(pdf_pages)} pages, {len(chapters)} chapters; kept with translation: {kept_pages or 'none'}")
    print(f"wrote {PAGES_DIR} and {PLAN_PATH}")


if __name__ == "__main__":
    main()
