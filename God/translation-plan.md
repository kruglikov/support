# Dominion Life — translation plan

Generated on 2026-09-29 by `God/tools/extract_pages.py` from `God/Dominion_Life_Manual_Updates_2024.pdf` and `God/glossary.md`. Regenerate after changing the glossary: `~/.local/share/pipx/venvs/pymupdf/bin/python God/tools/extract_pages.py` (page files that already hold a translation are kept).

Part 1 lists only what needs a decision before translating. Part 2 is the inventory of every page. Each page file `pages/NNN.md` holds the English text of PDF page NNN as tagged blocks.

## How to translate a page file

Each block of `pages/NNN.md` is a marker line, the English text quoted with `> `, and an empty line below it. Write the Russian text of the block on the empty line under its English text, as one line per paragraph, and keep the marker and the `> ` line unchanged: the marker's block number ties the Russian text to the rectangle of the English text in `pages/NNN.blocks.json`. `**bold**` and `*italic*` mark the author's emphasis; mark the corresponding Russian words the same way.

| Block type | What to write under it |
|---|---|
| `heading`, `subheading`, `prose` | the translation of the author's text, using the terms of `glossary.md` §1 |
| `reference` | the Синодальный перевод reference shown in the marker, for example `Быт. 1:26-28` |
| `kjv-verse` | the verse from the Синодальный перевод (reference in the marker), not a translation of the English verse; keep the verse number in front |
| `kjv-quote` | the verse from the Синодальный перевод, once its reference is identified (Part 1.4) |
| `strongs` | the entry rebuilt to the pattern of `glossary.md` §3 |
| `toc` | the translated chapter title and its page number |
| `keep-english` | nothing — the block stays in English |

## Part 1. Decisions before translating

### 1.1 Open glossary terms (status `decide` in `glossary.md` §1)

A page that contains an open term in the author's text waits until the term is decided. Inside Bible verses the Синодальный перевод wording is used anyway, so verse occurrences do not block a page.

| Term | Proposed Russian | Pages, author's text | Pages, Bible verses only |
|---|---|---|---|

### 1.2 Footer text (translated once, used on every page)

English: `Dominion Life Manual Reproduction Prohibited © jglm.org`. Proposed Russian: `Пособие „Жизнь во владычестве“. Воспроизведение запрещено © jglm.org`. Status: approved (`glossary.md` §5).

### 1.3 Strong's entries (`glossary.md` §3)

An entry is either a block of its own (`strongs`) or embedded in another block, such as the author's insertion inside a verse (`inline`).

| Page | Block | Block type | Entry | Also quoted on |
|---|---|---|---|---|
| [006](pages/006.md) | 6 | strongs | OT:7287 → Стронг ВЗ:7287 · radah | — |
| [008](pages/008.md) | 7 | strongs | NT:1849 → Стронг НЗ:1849 · exousia | [010](pages/010.md), [076](pages/076.md) |
| [010](pages/010.md) | 7 | strongs | NT:1849 → Стронг НЗ:1849 · exousia | [008](pages/008.md), [076](pages/076.md) |
| [018](pages/018.md) | 3 | strongs | NT:2634 → Стронг НЗ:2634 · katakurieuo · headword Dominion | — |
| [018](pages/018.md) | 4 | strongs | NT:2715 → Стронг НЗ:2715 · katexousiazo · headword Authority | — |
| [040](pages/040.md) | 1 | strongs | NT:2983 → Стронг НЗ:2983 · lambano · headword Shall Receive | — |
| [040](pages/040.md) | 2 | strongs | NT:1411 → Стронг НЗ:1411 · dunamis · headword Power | — |
| [076](pages/076.md) | 1 | kjv-verse | inline Стронг НЗ:1849 · exousia | [008](pages/008.md), [010](pages/010.md) |

### 1.4 Bible passages and their Синодальный перевод references

Every `reference` block with the verses that follow it. The column "Numbering" is filled only for the known places where the Синодальный перевод numbers the verse differently; every verse is still checked when its Russian text is inserted.

| Page | Block | KJV → Синодальный перевод | Verses on the page | Numbering |
|---|---|---|---|---|
| [006](pages/006.md) | 2 | Gen 1:26-28 → Быт. 1:26-28 | 26, 27, 28 |  |
| [006](pages/006.md) | 7 | Deut 28:1-14 → Втор. 28:1-14 | 1, 2, 3 |  |
| [008](pages/008.md) | 3 | Matt 28:18-20 → Мф. 28:18-20 | 18, 19, 20 |  |
| [010](pages/010.md) | 3 | Matt 28:18-20 → Мф. 28:18-20 | 18, 19, 20 |  |
| [010](pages/010.md) | 9 | 1 John 4:15-18 → 1 Ин. 4:15-18 | 15, 16, 17 |  |
| [011](pages/011.md) | 2 | Mark 16:14-20 → Мк. 16:14-20 | 14, 15, 16, 17, 18, 19, 20 |  |
| [012](pages/012.md) | 2 | Mark 13:31-37 → Мк. 13:31-37 | 31, 32, 33, 34, 35, 36, 37 |  |
| [012](pages/012.md) | 10 | John 14:6-20 → Ин. 14:6-20 | 6, 7, 8 |  |
| [014](pages/014.md) | 3 | Matt 16:13-20 → Мф. 16:13-20 | 13, 14, 15, 16, 17, 18, 19, 20 |  |
| [015](pages/015.md) | 1 | Matt 7:12-29 → Мф. 7:12-29 | 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 |  |
| [016](pages/016.md) | 9 | Matt 8:5-13 → Мф. 8:5-13 | 5, 6 |  |
| [018](pages/018.md) | 1 | Matt 20:25-34 → Мф. 20:25-34 | 25 |  |
| [019](pages/019.md) | 3 | Matt 21:23-27 → Мф. 21:23-27 | 23, 24, 25, 26, 27 |  |
| [019](pages/019.md) | 9 | Ps 138:2 → Пс. 137:2 | 2 | KJV Psalm 138:2 is Пс. 137:2; a psalm title can shift the verse, confirm it |
| [024](pages/024.md) | 2 | Gen 1:26-28 → Быт. 1:26-28 | 26, 27, 28 |  |
| [024](pages/024.md) | 6 | Ps 115:13-16 → Пс. 113:21-24 | 13, 14, 15, 16 | KJV Psalm 115:13 is Пс. 113:21; a psalm title can shift the verse, confirm it |
| [024](pages/024.md) | 11 | 2 Cor 4:3-4 → 2 Кор. 4:3-4 | 3, 4 |  |
| [025](pages/025.md) | 1 | Luke 4:1-7 → Лк. 4:1-7 | 1, 2, 3, 4, 5, 6, 7 |  |
| [025](pages/025.md) | 9 | Matt 21:12-16 → Мф. 21:12-16 | 12, 13, 14 |  |
| [027](pages/027.md) | 2 | Heb 2:1-18 → Евр. 2:1-18 | 1, 2, 3, 4, 5, 6, 7, 8, 9 |  |
| [029](pages/029.md) | 1 | 1 Cor 15:45-49 → 1 Кор. 15:45-49 | 45, 46, 47, 48, 49 |  |
| [029](pages/029.md) | 7 | 2 Cor 5:17-21 → 2 Кор. 5:17-21 | 17, 18, 19, 20 |  |
| [030](pages/030.md) | 3 | 1 John 4:17-18 → 1 Ин. 4:17-18 | 17, 18 |  |
| [030](pages/030.md) | 6 | Eph 2:10 → Еф. 2:10 | — (continues on the next page) |  |
| [030](pages/030.md) | 8 | Eph 4:24 → Еф. 4:24 | — (continues on the next page) |  |
| [030](pages/030.md) | 10 | Eph 1:18-23 → Еф. 1:18-23 | 18, 19, 20 |  |
| [031](pages/031.md) | 4 | Matt 28:18-20 → Мф. 28:18-20 | 18, 19, 20 |  |
| [031](pages/031.md) | 8 | Luke 10:19-20 → Лк. 10:19-20 | 19, 20 |  |
| [031](pages/031.md) | 11 | Acts 1:8 → Деян. 1:8 | — (continues on the next page) |  |
| [032](pages/032.md) | 2 | Mark 13:31-37 → Мк. 13:31-37 | 31, 32, 33, 34, 35, 36, 37 |  |
| [034](pages/034.md) | 2 | Isa 53:11-12 → Ис. 53:11-12 | 11, 12 |  |
| [034](pages/034.md) | 5 | Col 2:15 → Кол. 2:15 | 15 |  |
| [034](pages/034.md) | 7 | Eph 4:8-15 → Еф. 4:8-15 | 8, 9, 10, 11, 12 |  |
| [035](pages/035.md) | 5 | Luke 4:16-19 → Лк. 4:16-19 | 16, 17, 18, 19 |  |
| [038](pages/038.md) | 1 | Luke 10:12-20 → Лк. 10:12-20 | 12, 13, 14, 15, 16, 17, 18, 19, 20 |  |
| [039](pages/039.md) | 1 | Acts 1:1-8 → Деян. 1:1-8 | 1, 2, 3, 4, 5, 6, 7, 8 |  |
| [040](pages/040.md) | 4 | Matt 6:7-13 → Мф. 6:7-13 | 7, 8, 9, 10, 11, 12, 13 |  |
| [042](pages/042.md) | 2 | Matt 8:16-17 → Мф. 8:16-17 | 16, 17 |  |
| [042](pages/042.md) | 5 | Matt 9:31-35 → Мф. 9:31-35 | 31, 32, 33, 34, 35 |  |
| [043](pages/043.md) | 1 | Matt 10:7-8 → Мф. 10:7-8 | 7, 8 |  |
| [043](pages/043.md) | 4 | Mark 16:17-20 → Мк. 16:17-20 | 17, 18, 19, 20 |  |
| [044](pages/044.md) | 2 | Rom 5:17 → Рим. 5:17 | 17 |  |
| [044](pages/044.md) | 4 | Eccl 8:4 → Еккл. 8:4 | 4 |  |
| [046](pages/046.md) | 2 | Rev 1:4-7 → Откр. 1:4-7 | 4, 5, 6, 7 |  |
| [047](pages/047.md) | 1 | Rev 5:9-10 → Откр. 5:9-10 | 9, 10 |  |
| [048](pages/048.md) | 2 | Matt 25:14-46 → Мф. 25:14-46 | 14, 15, 16, 17, 18, 19, 20, 21, 22 |  |
| [052](pages/052.md) | 2 | Luke 19:11-27 → Лк. 19:11-27 | 11, 12, 13, 14, 15, 16, 17, 18, 19 |  |
| [054](pages/054.md) | 2 | Rom 12:1-3 → Рим. 12:1-3 | 1, 2, 3 |  |
| [056](pages/056.md) | 2 | 1 Sam 15:22-23 → 1 Цар. 15:22-23 | 22, 23 |  |
| [058](pages/058.md) | 10 | Gal 6:7-9 → Гал. 6:7-9 | 7, 8, 9 |  |
| [058](pages/058.md) | 14 | Luke 6:36-38 → Лк. 6:36-38 | 36, 37 |  |
| [059](pages/059.md) | 2 | 2 Cor 9:6-10 → 2 Кор. 9:6-10 | 6, 7, 8, 9, 10 |  |
| [060](pages/060.md) | 2 | Rom 3:27-31 → Рим. 3:27-31 | 27, 28, 29, 30, 31 |  |
| [060](pages/060.md) | 8 | Matt 17:19-20 → Мф. 17:19-20 | 19, 20 |  |
| [061](pages/061.md) | 2 | James 2:8-9 → Иак. 2:8-9 | 8, 9 |  |
| [061](pages/061.md) | 7 | Mark 11:23 → Мк. 11:23 | 23 |  |
| [061](pages/061.md) | 9 | Matt 12:36-37 → Мф. 12:36-37 | 36, 37 |  |
| [062](pages/062.md) | 1 | James 3:5-13 → Иак. 3:5-13 | 5, 6, 7, 8, 9, 10, 11, 12, 13 |  |
| [065](pages/065.md) | 5 | James 1:5-8 → Иак. 1:5-8 | 5, 6, 7, 8 |  |
| [066](pages/066.md) | 2 | James 1:21-27 → Иак. 1:21-27 | 21, 22, 23, 24, 25, 26, 27 |  |
| [067](pages/067.md) | 1 | Matt 7:6-29 → Мф. 7:6-29 | 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 |  |
| [070](pages/070.md) | 2 | 1 Corinthians 3:1-9 → 1 Кор. 3:1-9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 |  |
| [071](pages/071.md) | 1 | Eph 4:8-15 → Еф. 4:8-15 | 8, 9, 10, 11, 12, 13, 14, 15 |  |
| [072](pages/072.md) | 1 | James 3:2-13 → Иак. 3:2-13 | 2, 3, 4, 5, 6, 7, 8, 9, 10 |  |
| [074](pages/074.md) | 2 | Gal 2:20 → Гал. 2:20 | 20 |  |
| [074](pages/074.md) | 4 | James 2:1-9 → Иак. 2:1-9 | 1, 2, 3, 4, 5, 6, 7 |  |
| [076](pages/076.md) | 2 | Luke 9:1-6 → Лк. 9:1-6 | 1, 2, 3, 4, 5, 6 |  |
| [077](pages/077.md) | 1 | Luke 6:17-19 → Лк. 6:17-19 | 17, 18, 19 |  |
| [077](pages/077.md) | 5 | Matt 4:23-24 → Мф. 4:23-24 | 23 |  |
| [077](pages/077.md) | 9 | Matt 8:16-17 → Мф. 8:16-17 | 16 |  |
| [078](pages/078.md) | 1 | Matt 15:21-30 → Мф. 15:21-30 | 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 |  |
| [079](pages/079.md) | 1 | Mark 16:14-20 → Мк. 16:14-20 | 14, 15, 16, 17, 18, 19, 20 |  |
| [079](pages/079.md) | 9 | Mark 3:1-15 → Мк. 3:1-15 | 1, 2 |  |
| [081](pages/081.md) | 4 | Matt 12:14-30 → Мф. 12:14-30 | — (continues on the next page) |  |
| [083](pages/083.md) | 1 | Matt 14:34-36 → Мф. 14:34-36 | — (continues on the next page) |  |
| [083](pages/083.md) | 7 | Mark 1:14-45 → Мк. 1:14-45 | 14, 15, 16, 17, 18 |  |
| [086](pages/086.md) | 7 | Mark 16:15-20 → Мк. 16:15-20 | 15, 16, 17, 18 |  |
| [087](pages/087.md) | 3 | Matt 28:18-20 → Мф. 28:18-20 | 18, 19, 20 |  |
| [087](pages/087.md) | 8 | Matt 28:18-20 → Мф. 28:18-20 | 18, 19, 20 |  |
| [088](pages/088.md) | 4 | Phil 2:8-10 → Флп. 2:8-10 | 8, 9, 10 |  |
| [088](pages/088.md) | 8 | John 1:11-13 → Ин. 1:11-13 | 11, 12, 13 |  |
| [089](pages/089.md) | 1 | 1 John 3:1-4 → 1 Ин. 3:1-4 | 1, 2, 3, 4 |  |
| [089](pages/089.md) | 7 | John 14:12-17 → Ин. 14:12-17 | 12, 13, 14, 15 |  |
| [090](pages/090.md) | 3 | John 16:7-13 → Ин. 16:7-13 | 7, 8, 9, 10, 11, 12, 13 |  |
| [091](pages/091.md) | 1 | Matt 8:5-13 → Мф. 8:5-13 | 5, 6, 7, 8, 9, 10, 11, 12, 13 |  |
| [092](pages/092.md) | 1 | Matt 9:1-8 → Мф. 9:1-8 | 1, 2, 3, 4, 5, 6, 7, 8 |  |
| [092](pages/092.md) | 10 | Matt 10:1 → Мф. 10:1 | 1 |  |
| [093](pages/093.md) | 1 | Matt 10:5-8 → Мф. 10:5-8 | 5, 6, 7, 8 |  |
| [093](pages/093.md) | 7 | Mark 3:13-15 → Мк. 3:13-15 | 13, 14 |  |
| [094](pages/094.md) | 1 | Mark 6:7-13 → Мк. 6:7-13 | 7, 8, 9, 10, 11, 12, 13 |  |
| [095](pages/095.md) | 1 | Acts 1:7-8 → Деян. 1:7-8 | 7, 8 |  |
| [096](pages/096.md) | 1 | Acts 3:12 → Деян. 3:12 | 12 |  |
| [096](pages/096.md) | 3 | Acts 3:16 → Деян. 3:16 | 16 |  |
| [096](pages/096.md) | 5 | Acts 3:6 → Деян. 3:6 | 6 |  |
| [096](pages/096.md) | 7 | Matt 17:14-20 → Мф. 17:14-20 | 14, 15, 16, 17, 18, 19 |  |
| [097](pages/097.md) | 4 | Eph 3:14-15 → Еф. 3:14-15 | 14, 15 |  |
| [097](pages/097.md) | 7 | Eph 1:19-23 → Еф. 1:19-23 | 19, 20, 21, 22, 23 |  |
| [007](pages/007.md) | 1 | Deut 28:4 → Втор. 28:4 (continued from the previous page) | |  |
| [008](pages/008.md) | 1 | Deut 28:13 → Втор. 28:13 (continued from the previous page) | |  |
| [011](pages/011.md) | 1 | 1 John 4:18 → 1 Ин. 4:18 (continued from the previous page) | |  |
| [013](pages/013.md) | 1 | John 14:9 → Ин. 14:9 (continued from the previous page) | |  |
| [014](pages/014.md) | 1 | John 14:19 → Ин. 14:19 (continued from the previous page) | |  |
| [016](pages/016.md) | 1 | Matt 7:22 → Мф. 7:22 (continued from the previous page) | |  |
| [017](pages/017.md) | 1 | Matt 8:7 → Мф. 8:7 (continued from the previous page) | |  |
| [026](pages/026.md) | 1 | Matt 21:15 → Мф. 21:15 (continued from the previous page) | |  |
| [028](pages/028.md) | 1 | Heb 2:10 → Евр. 2:10 (continued from the previous page) | |  |
| [030](pages/030.md) | 1 | 2 Cor 5:21 → 2 Кор. 5:21 (continued from the previous page) | |  |
| [031](pages/031.md) | 1 | Eph 1:21 → Еф. 1:21 (continued from the previous page) | |  |
| [035](pages/035.md) | 1 | Eph 4:13 → Еф. 4:13 (continued from the previous page) | |  |
| [037](pages/037.md) | 1 | Luke 10:3 → Лк. 10:3 (continued from the previous page) | |  |
| [049](pages/049.md) | 1 | Matt 25:23 → Мф. 25:23 (continued from the previous page) | |  |
| [050](pages/050.md) | 1 | Matt 25:32 → Мф. 25:32 (continued from the previous page) | |  |
| [051](pages/051.md) | 1 | Matt 25:42 → Мф. 25:42 (continued from the previous page) | |  |
| [053](pages/053.md) | 1 | Luke 19:20 → Лк. 19:20 (continued from the previous page) | |  |
| [059](pages/059.md) | 1 | Luke 6:38 → Лк. 6:38 (continued from the previous page) | |  |
| [068](pages/068.md) | 1 | Matt 7:16 → Мф. 7:16 (continued from the previous page) | |  |
| [069](pages/069.md) | 1 | Matt 7:26 → Мф. 7:26 (continued from the previous page) | |  |
| [073](pages/073.md) | 1 | James 3:11 → Иак. 3:11 (continued from the previous page) | |  |
| [075](pages/075.md) | 1 | James 2:8 → Иак. 2:8 (continued from the previous page) | |  |
| [076](pages/076.md) | 1 | Matt 10:1 → Мф. 10:1 (continued from the previous page) | |  |
| [080](pages/080.md) | 1 | Mark 3:3 → Мк. 3:3 (continued from the previous page) | |  |
| [081](pages/081.md) | 1 | Mark 3:13 → Мк. 3:13 (continued from the previous page) | |  |
| [084](pages/084.md) | 1 | Mark 1:19 → Мк. 1:19 (continued from the previous page) | |  |
| [085](pages/085.md) | 1 | Mark 1:29 → Мк. 1:29 (continued from the previous page) | |  |
| [086](pages/086.md) | 1 | Mark 1:40 → Мк. 1:40 (continued from the previous page) | |  |
| [087](pages/087.md) | 1 | Mark 16:19 → Мк. 16:19 (continued from the previous page) | |  |
| [090](pages/090.md) | 1 | John 14:16 → Ин. 14:16 (continued from the previous page) | |  |
| [097](pages/097.md) | 1 | Matt 17:20 → Мф. 17:20 (continued from the previous page) | |  |

### 1.5 Quotations ending with "KJV" whose reference was not found

The reference of each quotation below must be identified before the Синодальный перевод text can replace it.

| Page | Block | Words |
|---|---|---|

### 1.6 Verses with the author's emphasis or insertions

`emphasis`: the author bolds words inside the verse, so the corresponding words of the Синодальный перевод verse must be bolded too. `insertion`: the verse contains the author's words in parentheses or brackets, which are translated and placed at the same point of the Russian verse (`glossary.md` §2, rule 6).

| Page | Block | Verse | Flags |
|---|---|---|---|
| [006](pages/006.md) | 3 | Gen 1:26 → Быт. 1:26 | emphasis |
| [006](pages/006.md) | 5 | Gen 1:28 → Быт. 1:28 | emphasis |
| [008](pages/008.md) | 1 | Deut 28:13 → Втор. 28:13 | emphasis |
| [008](pages/008.md) | 2 | Deut 28:14 → Втор. 28:14 | emphasis |
| [008](pages/008.md) | 4 | Matt 28:18 → Мф. 28:18 | emphasis, insertion |
| [010](pages/010.md) | 12 | 1 John 4:17 → 1 Ин. 4:17 | emphasis |
| [016](pages/016.md) | 3 | Matt 7:24 → Мф. 7:24 | emphasis |
| [016](pages/016.md) | 5 | Matt 7:26 → Мф. 7:26 | emphasis |
| [016](pages/016.md) | 7 | Matt 7:28 → Мф. 7:28 | emphasis |
| [016](pages/016.md) | 8 | Matt 7:29 → Мф. 7:29 | emphasis |
| [017](pages/017.md) | 1 | Matt 8:7 → Мф. 8:7 | emphasis |
| [017](pages/017.md) | 2 | Matt 8:8 → Мф. 8:8 | emphasis |
| [017](pages/017.md) | 3 | Matt 8:9 → Мф. 8:9 | emphasis |
| [018](pages/018.md) | 2 | Matt 20:25 → Мф. 20:25 | emphasis |
| [031](pages/031.md) | 2 | Eph 1:22 → Еф. 1:22 | emphasis |
| [031](pages/031.md) | 3 | Eph 1:23 → Еф. 1:23 | emphasis |
| [034](pages/034.md) | 4 | Isa 53:12 → Ис. 53:12 | emphasis |
| [034](pages/034.md) | 9 | Eph 4:9 → Еф. 4:9 | insertion |
| [038](pages/038.md) | 9 | Luke 10:19 → Лк. 10:19 | emphasis |
| [039](pages/039.md) | 6 | Acts 1:5 → Деян. 1:5 | emphasis |
| [039](pages/039.md) | 9 | Acts 1:8 → Деян. 1:8 | emphasis |
| [040](pages/040.md) | 8 | Matt 6:10 → Мф. 6:10 | emphasis |
| [052](pages/052.md) | 9 | Luke 19:17 → Лк. 19:17 | emphasis |
| [052](pages/052.md) | 11 | Luke 19:19 → Лк. 19:19 | emphasis |
| [053](pages/053.md) | 3 | Luke 19:22 → Лк. 19:22 | emphasis |
| [053](pages/053.md) | 6 | Luke 19:25 → Лк. 19:25 | insertion |
| [056](pages/056.md) | 3 | 1 Sam 15:22 → 1 Цар. 15:22 | emphasis |
| [059](pages/059.md) | 6 | 2 Cor 9:9 → 2 Кор. 9:9 | insertion |
| [071](pages/071.md) | 3 | Eph 4:9 → Еф. 4:9 | insertion |
| [071](pages/071.md) | 6 | Eph 4:12 → Еф. 4:12 | emphasis |
| [071](pages/071.md) | 7 | Eph 4:13 → Еф. 4:13 | emphasis |
| [076](pages/076.md) | 1 | Matt 10:1 → Мф. 10:1 | emphasis, insertion |
| [076](pages/076.md) | 3 | Luke 9:1 → Лк. 9:1 | emphasis |
| [076](pages/076.md) | 4 | Luke 9:2 → Лк. 9:2 | emphasis |
| [076](pages/076.md) | 8 | Luke 9:6 → Лк. 9:6 | emphasis |
| [077](pages/077.md) | 2 | Luke 6:17 → Лк. 6:17 | emphasis |
| [077](pages/077.md) | 3 | Luke 6:18 → Лк. 6:18 | emphasis |
| [077](pages/077.md) | 4 | Luke 6:19 → Лк. 6:19 | emphasis |
| [077](pages/077.md) | 6 | Matt 4:23 → Мф. 4:23 | emphasis |
| [077](pages/077.md) | 10 | Matt 8:16 → Мф. 8:16 | emphasis |
| [078](pages/078.md) | 5 | Matt 15:24 → Мф. 15:24 | emphasis |
| [078](pages/078.md) | 7 | Matt 15:26 → Мф. 15:26 | emphasis |
| [078](pages/078.md) | 11 | Matt 15:30 → Мф. 15:30 | emphasis |
| [079](pages/079.md) | 3 | Mark 16:15 → Мк. 16:15 | emphasis |
| [079](pages/079.md) | 11 | Mark 3:2 → Мк. 3:2 | emphasis |
| [080](pages/080.md) | 1 | Mark 3:3 → Мк. 3:3 | emphasis |
| [080](pages/080.md) | 3 | Mark 3:5 → Мк. 3:5 | emphasis |
| [080](pages/080.md) | 8 | Mark 3:10 → Мк. 3:10 | emphasis |
| [080](pages/080.md) | 9 | Mark 3:11 → Мк. 3:11 | emphasis |
| [081](pages/081.md) | 2 | Mark 3:14 → Мк. 3:14 | emphasis |
| [081](pages/081.md) | 3 | Mark 3:15 → Мк. 3:15 | emphasis |
| [084](pages/084.md) | 4 | Mark 1:22 → Мк. 1:22 | emphasis |
| [084](pages/084.md) | 9 | Mark 1:27 → Мк. 1:27 | emphasis |
| [085](pages/085.md) | 2 | Mark 1:30 → Мк. 1:30 | emphasis |
| [085](pages/085.md) | 4 | Mark 1:32 → Мк. 1:32 | emphasis |
| [085](pages/085.md) | 6 | Mark 1:34 → Мк. 1:34 | emphasis |
| [085](pages/085.md) | 11 | Mark 1:39 → Мк. 1:39 | emphasis |
| [086](pages/086.md) | 2 | Mark 1:41 → Мк. 1:41 | emphasis |
| [086](pages/086.md) | 3 | Mark 1:42 → Мк. 1:42 | emphasis |
| [087](pages/087.md) | 5 | Matt 28:19 → Мф. 28:19 | emphasis |
| [087](pages/087.md) | 6 | Matt 28:20 → Мф. 28:20 | emphasis |
| [087](pages/087.md) | 9 | Matt 28:18 → Мф. 28:18 | emphasis, insertion |
| [087](pages/087.md) | 11 | Matt 28:20 → Мф. 28:20 | emphasis |
| [088](pages/088.md) | 10 | John 1:12 → Ин. 1:12 | emphasis, insertion |
| [089](pages/089.md) | 2 | 1 John 3:1 → 1 Ин. 3:1 | emphasis |
| [089](pages/089.md) | 3 | 1 John 3:2 → 1 Ин. 3:2 | emphasis |
| [089](pages/089.md) | 8 | John 14:12 → Ин. 14:12 | emphasis |
| [089](pages/089.md) | 9 | John 14:13 → Ин. 14:13 | emphasis |
| [089](pages/089.md) | 10 | John 14:14 → Ин. 14:14 | emphasis |
| [090](pages/090.md) | 1 | John 14:16 → Ин. 14:16 | emphasis, insertion |
| [090](pages/090.md) | 4 | John 16:7 → Ин. 16:7 | emphasis |
| [090](pages/090.md) | 9 | John 16:12 → Ин. 16:12 | emphasis |
| [090](pages/090.md) | 10 | John 16:13 → Ин. 16:13 | emphasis |
| [091](pages/091.md) | 5 | Matt 8:8 → Мф. 8:8 | emphasis |
| [091](pages/091.md) | 6 | Matt 8:9 → Мф. 8:9 | emphasis |
| [091](pages/091.md) | 7 | Matt 8:10 → Мф. 8:10 | emphasis |
| [091](pages/091.md) | 10 | Matt 8:13 → Мф. 8:13 | emphasis |
| [092](pages/092.md) | 7 | Matt 9:6 → Мф. 9:6 | emphasis, insertion |
| [092](pages/092.md) | 9 | Matt 9:8 → Мф. 9:8 | emphasis, insertion |
| [092](pages/092.md) | 11 | Matt 10:1 → Мф. 10:1 | emphasis, insertion |
| [093](pages/093.md) | 4 | Matt 10:7 → Мф. 10:7 | emphasis |
| [093](pages/093.md) | 5 | Matt 10:8 → Мф. 10:8 | emphasis |
| [093](pages/093.md) | 9 | Mark 3:14 → Мк. 3:14 | emphasis, insertion |
| [094](pages/094.md) | 2 | Mark 6:7 → Мк. 6:7 | emphasis, insertion |
| [094](pages/094.md) | 7 | Mark 6:12 → Мк. 6:12 | emphasis |
| [094](pages/094.md) | 8 | Mark 6:13 → Мк. 6:13 | emphasis |
| [095](pages/095.md) | 2 | Acts 1:7 → Деян. 1:7 | emphasis, insertion |
| [095](pages/095.md) | 3 | Acts 1:8 → Деян. 1:8 | emphasis, insertion |
| [096](pages/096.md) | 2 | Acts 3:12 → Деян. 3:12 | emphasis, insertion |
| [096](pages/096.md) | 11 | Matt 17:17 → Мф. 17:17 | emphasis |
| [096](pages/096.md) | 12 | Matt 17:18 → Мф. 17:18 | emphasis |
| [096](pages/096.md) | 13 | Matt 17:19 → Мф. 17:19 | emphasis |
| [097](pages/097.md) | 1 | Matt 17:20 → Мф. 17:20 | emphasis |
| [097](pages/097.md) | 5 | Eph 3:14 → Еф. 3:14 | emphasis |
| [097](pages/097.md) | 6 | Eph 3:15 → Еф. 3:15 | emphasis |
| [097](pages/097.md) | 11 | Eph 1:22 → Еф. 1:22 | emphasis |
| [097](pages/097.md) | 12 | Eph 1:23 → Еф. 1:23 | emphasis |

### 1.7 English in brackets: first occurrence per chapter

For terms marked `EN = yes` in `glossary.md` §1, the English original is added in round brackets at the first occurrence in the author's text of each chapter, listed here.

| Term | Russian | First occurrence per chapter (page · block) |
|---|---|---|
| dominion | владычество | [001](pages/001.md) · b2; [006](pages/006.md) · b1; [018](pages/018.md) · b3; [026](pages/026.md) · b8; [042](pages/042.md) · b1; [048](pages/048.md) · b1 |
| authority | власть | [008](pages/008.md) · b7; [010](pages/010.md) · b1; [032](pages/032.md) · b1; [034](pages/034.md) · b1; [036](pages/036.md) · b1; [052](pages/052.md) · b1; [075](pages/075.md) · b3 |
| power | сила | [008](pages/008.md) · b7; [010](pages/010.md) · b7; [031](pages/031.md) · b12; [040](pages/040.md) · b2; [093](pages/093.md) · b11 |
| delegated authority | делегированная власть | [036](pages/036.md) · b1 |
| inherited authority | унаследованная власть | [036](pages/036.md) · b1 |
| pre-permission | предварительное разрешение | [010](pages/010.md) · b2; [034](pages/034.md) · b1; [087](pages/087.md) · b7 |
| servants | in verses: as the Синодальный перевод («рабы»); in the author's text: «рабы» or «слуги» by context | [012](pages/012.md) · b1; [032](pages/032.md) · b1 |
| confusion | in verses: as the Синодальный перевод («неустройство»); in the author's text: «неустройство» or «смятение» by context | [058](pages/058.md) · b1 |
| demons | in verses: as the Синодальный перевод («бесы»); in the author's text: «бесы» or «демоны» by context | [042](pages/042.md) · b1 |
| God-ordained position | «Богом установленное положение» or «Богом данная позиция» by context | [024](pages/024.md) · b1 |
| systems (laws) | системы (законы) | [058](pages/058.md) · b1; [066](pages/066.md) · b1 |
| principles | принципы | [058](pages/058.md) · b1; [066](pages/066.md) · b1 |

### 1.8 Pages with images

Text inside an image cannot be replaced; check each page visually for such text.

[001](pages/001.md) (3), [002](pages/002.md) (1), [098](pages/098.md) (4), [099](pages/099.md) (1)

### 1.9 Full pages

Text reaches below y = 700 pt with at least 200 words. Russian text runs 10–20% longer, so these pages will need a smaller font size or tighter line spacing when the PDF is rebuilt.

[010](pages/010.md), [021](pages/021.md), [022](pages/022.md), [024](pages/024.md), [025](pages/025.md), [026](pages/026.md), [027](pages/027.md), [040](pages/040.md), [074](pages/074.md), [078](pages/078.md), [086](pages/086.md)

### 1.10 Pages with nothing to translate

Footer only: [005](pages/005.md), [009](pages/009.md), [033](pages/033.md), [041](pages/041.md), [045](pages/045.md), [055](pages/055.md), [057](pages/057.md), [098](pages/098.md). Kept in English (`glossary.md` §6): [003](pages/003.md).

## Part 2. Inventory of every page

Blocks by type across the book: `heading` 42, `keep-english` 5, `kjv-verse` 562, `prose` 102, `reference` 97, `strongs` 7, `subheading` 14, `toc` 17. "Words to translate" counts the author's text only; Bible verses are replaced from the Синодальный перевод and are not counted.

### Front matter

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [001](pages/001.md) | — | 6 | b1 heading · b2 heading · b3 heading · b4 prose | written |
| [002](pages/002.md) | — | 5 | b1 heading · b2 heading | written |
| [003](pages/003.md) | 2 | 0 | b1 keep-english · b2 keep-english · b3 keep-english · b4 keep-english · b5 keep-english | written |
| [004](pages/004.md) | 3 | 126 | b1 toc · b2 toc · b3 toc · b4 toc · b5 toc · b6 toc · b7 toc · b8 toc · b9 toc · b10 toc · b11 toc · b12 toc · b13 toc · b14 toc · b15 toc · b16 toc · b17 toc | written |
| [005](pages/005.md) | 4 | 0 | footer only | written |

### What Is “Dominion”

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [006](pages/006.md) | 5 | 3 | b1 heading · b2 reference Gen 1:26-28 · b3–b5 kjv-verse Gen 1:26–28 · b6 strongs OT:7287 radah · b7 reference Deut 28:1-14 · b8–b10 kjv-verse Deut 28:1–3 | kept (has translation) |
| [007](pages/007.md) | 6 | 0 | b1–b9 kjv-verse Deut 28:4–12 | kept (has translation) |
| [008](pages/008.md) | 7 | 0 | b1–b2 kjv-verse Deut 28:13–14 · b3 reference Matt 28:18-20 · b4–b6 kjv-verse Matt 28:18–20 · b7 strongs NT:1849 exousia | kept (has translation) |
| [009](pages/009.md) | 8 | 0 | footer only | written |

### What Is “Authority”

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [010](pages/010.md) | 9 | 10 | b1 heading · b2 heading · b3 reference Matt 28:18-20 · b4–b6 kjv-verse Matt 28:18–20 · b7 strongs NT:1849 exousia · b8 subheading · b9 reference 1 John 4:15-18 · b10–b12 kjv-verse 1 John 4:15–17 | kept (has translation) |
| [011](pages/011.md) | 10 | 0 | b1 kjv-verse 1 John 4:18 · b2 reference Mark 16:14-20 · b3–b9 kjv-verse Mark 16:14–20 | kept (has translation) |
| [012](pages/012.md) | 11 | 10 | b1 heading · b2 reference Mark 13:31-37 · b3–b9 kjv-verse Mark 13:31–37 · b10 reference John 14:6-20 · b11–b13 kjv-verse John 14:6–8 | kept (has translation) |
| [013](pages/013.md) | 12 | 0 | b1–b10 kjv-verse John 14:9–18 | kept (has translation) |
| [014](pages/014.md) | 13 | 0 | b1–b2 kjv-verse John 14:19–20 · b3 reference Matt 16:13-20 · b4–b11 kjv-verse Matt 16:13–20 | kept (has translation) |
| [015](pages/015.md) | 14 | 0 | b1 reference Matt 7:12-29 · b2–b11 kjv-verse Matt 7:12–21 | kept (has translation) |
| [016](pages/016.md) | 15 | 0 | b1–b8 kjv-verse Matt 7:22–29 · b9 reference Matt 8:5-13 · b10–b11 kjv-verse Matt 8:5–6 | kept (has translation) |
| [017](pages/017.md) | 16 | 0 | b1–b7 kjv-verse Matt 8:7–13 | kept (has translation) |
| [018](pages/018.md) | 17 | 149 | b1 reference Matt 20:25-34 · b2 kjv-verse Matt 20:25 · b3 strongs NT:2634 katakurieuo · b4 strongs NT:2715 katexousiazo · b5–b11 prose | kept (has translation) |
| [019](pages/019.md) | 18 | 33 | b1–b2 prose · b3 reference Matt 21:23-27 · b4–b8 kjv-verse Matt 21:23–27 · b9 reference Ps 138:2 · b10 kjv-verse Ps 138:2 | kept (has translation) |
| [020](pages/020.md) | 19 | 308 | b1 heading · b2–b9 prose · b10 heading | written |
| [021](pages/021.md) | 20 | 351 | b1 heading · b2–b5 prose · b6 subheading · b7–b9 prose | written |
| [022](pages/022.md) | 21 | 377 | b1–b6 prose | written |
| [023](pages/023.md) | 22 | 35 | b1 prose · b2 heading · b3 prose | written |

### “Take Your God-Ordained Position”

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [024](pages/024.md) | 23 | 4 | b1 heading · b2 reference Gen 1:26-28 · b3–b5 kjv-verse Gen 1:26–28 · b6 reference Ps 115:13-16 · b7–b10 kjv-verse Ps 115:13–16 · b11 reference 2 Cor 4:3-4 · b12–b13 kjv-verse 2 Cor 4:3–4 | kept (has translation) |
| [025](pages/025.md) | 24 | 0 | b1 reference Luke 4:1-7 · b2–b8 kjv-verse Luke 4:1–7 · b9 reference Matt 21:12-16 · b10–b12 kjv-verse Matt 21:12–14 | kept (has translation) |
| [026](pages/026.md) | 25 | 163 | b1–b2 kjv-verse Matt 21:15–16 · b3–b10 prose | kept (has translation) |
| [027](pages/027.md) | 26 | 14 | b1 prose · b2 reference Heb 2:1-18 · b3–b11 kjv-verse Heb 2:1–9 | kept (has translation) |
| [028](pages/028.md) | 27 | 0 | b1–b9 kjv-verse Heb 2:10–18 | kept (has translation) |
| [029](pages/029.md) | 28 | 0 | b1 reference 1 Cor 15:45-49 · b2–b6 kjv-verse 1 Cor 15:45–49 · b7 reference 2 Cor 5:17-21 · b8–b11 kjv-verse 2 Cor 5:17–20 | kept (has translation) |
| [030](pages/030.md) | 29 | 48 | b1 kjv-verse 2 Cor 5:21 · b2 subheading · b3 reference 1 John 4:17-18 · b4–b5 kjv-verse 1 John 4:17–18 · b6 reference Eph 2:10 · b7 prose · b8 reference Eph 4:24 · b9 prose · b10 reference Eph 1:18-23 · b11–b13 kjv-verse Eph 1:18–20 | kept (has translation) |
| [031](pages/031.md) | 30 | 39 | b1–b3 kjv-verse Eph 1:21–23 · b4 reference Matt 28:18-20 · b5–b7 kjv-verse Matt 28:18–20 · b8 reference Luke 10:19-20 · b9–b10 kjv-verse Luke 10:19–20 · b11 reference Acts 1:8 · b12 prose | kept (has translation) |

### The Son Gave Authority To His Servants UNTIL He Returns

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [032](pages/032.md) | 31 | 10 | b1 heading · b2 reference Mark 13:31-37 · b3–b9 kjv-verse Mark 13:31–37 | kept (has translation) |
| [033](pages/033.md) | 32 | 0 | footer only | written |

### AUTHORITY IS PRE-PERMISSION

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [034](pages/034.md) | 33 | 3 | b1 heading · b2 reference Isa 53:11-12 · b3–b4 kjv-verse Isa 53:11–12 · b5 reference Col 2:15 · b6 kjv-verse Col 2:15 · b7 reference Eph 4:8-15 · b8–b12 kjv-verse Eph 4:8–12 | kept (has translation) |
| [035](pages/035.md) | 34 | 22 | b1–b3 kjv-verse Eph 4:13–15 · b4 prose · b5 reference Luke 4:16-19 · b6–b9 kjv-verse Luke 4:16–19 | kept (has translation) |

### Delegated Authority vs. Inherited Authority

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [036](pages/036.md) | 35 | 159 | b1 heading · b2 heading · b3 subheading · b4–b9 prose · b10–b11 kjv-verse Luke 10:1–2 | kept (has translation) |
| [037](pages/037.md) | 36 | 0 | b1–b9 kjv-verse Luke 10:3–11 | kept (has translation) |
| [038](pages/038.md) | 37 | 0 | b1 reference Luke 10:12-20 · b2–b10 kjv-verse Luke 10:12–20 | kept (has translation) |
| [039](pages/039.md) | 38 | 0 | b1 reference Acts 1:1-8 · b2–b9 kjv-verse Acts 1:1–8 | kept (has translation) |
| [040](pages/040.md) | 39 | 7 | b1 strongs NT:2983 lambano · b2 strongs NT:1411 dunamis · b3 subheading · b4 reference Matt 6:7-13 · b5–b11 kjv-verse Matt 6:7–13 | kept (has translation) |
| [041](pages/041.md) | 40 | 0 | footer only | written |

### Dominion Over Demons

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [042](pages/042.md) | 41 | 3 | b1 heading · b2 reference Matt 8:16-17 · b3–b4 kjv-verse Matt 8:16–17 · b5 reference Matt 9:31-35 · b6–b10 kjv-verse Matt 9:31–35 | kept (has translation) |
| [043](pages/043.md) | 42 | 0 | b1 reference Matt 10:7-8 · b2–b3 kjv-verse Matt 10:7–8 · b4 reference Mark 16:17-20 · b5–b8 kjv-verse Mark 16:17–20 | kept (has translation) |

### King’s Reign – That’s What They Do

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [044](pages/044.md) | 43 | 7 | b1 heading · b2 reference Rom 5:17 · b3 kjv-verse Rom 5:17 · b4 reference Eccl 8:4 · b5 kjv-verse Eccl 8:4 | kept (has translation) |
| [045](pages/045.md) | 44 | 0 | footer only | written |

### Priests Establish Righteousness – That’s What They Do

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [046](pages/046.md) | 45 | 8 | b1 heading · b2 reference Rev 1:4-7 · b3–b6 kjv-verse Rev 1:4–7 | kept (has translation) |
| [047](pages/047.md) | 46 | 0 | b1 reference Rev 5:9-10 · b2–b3 kjv-verse Rev 5:9–10 | kept (has translation) |

### Developing Dominion – Practicing Your Position

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [048](pages/048.md) | 47 | 6 | b1 heading · b2 reference Matt 25:14-46 · b3–b11 kjv-verse Matt 25:14–22 | kept (has translation) |
| [049](pages/049.md) | 48 | 0 | b1–b9 kjv-verse Matt 25:23–31 | kept (has translation) |
| [050](pages/050.md) | 49 | 0 | b1–b10 kjv-verse Matt 25:32–41 | kept (has translation) |
| [051](pages/051.md) | 50 | 0 | b1–b5 kjv-verse Matt 25:42–46 | kept (has translation) |
| [052](pages/052.md) | 51 | 10 | b1 heading · b2 reference Luke 19:11-27 · b3–b11 kjv-verse Luke 19:11–19 | kept (has translation) |
| [053](pages/053.md) | 52 | 0 | b1–b8 kjv-verse Luke 19:20–27 | kept (has translation) |

### A Living Sacrifice

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [054](pages/054.md) | 53 | 3 | b1 heading · b2 reference Rom 12:1-3 · b3–b5 kjv-verse Rom 12:1–3 | kept (has translation) |
| [055](pages/055.md) | 54 | 0 | footer only | written |

### Obedience Is Better Than Sacrifice

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [056](pages/056.md) | 55 | 5 | b1 heading · b2 reference 1 Sam 15:22-23 · b3–b4 kjv-verse 1 Sam 15:22–23 | kept (has translation) |
| [057](pages/057.md) | 56 | 0 | footer only | written |

### Systems (Laws), Principles, Peace And Confusion

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [058](pages/058.md) | 57 | 80 | b1 heading · b2 subheading · b3 heading · b4–b7 prose · b8 heading · b9 heading · b10 reference Gal 6:7-9 · b11–b13 kjv-verse Gal 6:7–9 · b14 reference Luke 6:36-38 · b15–b16 kjv-verse Luke 6:36–37 | kept (has translation) |
| [059](pages/059.md) | 58 | 0 | b1 kjv-verse Luke 6:38 · b2 reference 2 Cor 9:6-10 · b3–b7 kjv-verse 2 Cor 9:6–10 | kept (has translation) |
| [060](pages/060.md) | 59 | 4 | b1 heading · b2 reference Rom 3:27-31 · b3–b7 kjv-verse Rom 3:27–31 · b8 reference Matt 17:19-20 · b9–b10 kjv-verse Matt 17:19–20 | kept (has translation) |
| [061](pages/061.md) | 60 | 21 | b1 heading · b2 reference James 2:8-9 · b3–b4 kjv-verse James 2:8–9 · b5 heading · b6 heading · b7 reference Mark 11:23 · b8 kjv-verse Mark 11:23 · b9 reference Matt 12:36-37 · b10–b11 kjv-verse Matt 12:36–37 | kept (has translation) |
| [062](pages/062.md) | 61 | 0 | b1 reference James 3:5-13 · b2–b10 kjv-verse James 3:5–13 | kept (has translation) |
| [063](pages/063.md) | 62 | 113 | b1 prose · b2 heading · b3–b7 prose | written |
| [064](pages/064.md) | 63 | 86 | b1–b3 prose | written |
| [065](pages/065.md) | 64 | 66 | b1 prose · b2 kjv-verse 1 Cor 14:33 · b3–b4 prose · b5 reference James 1:5-8 · b6–b9 kjv-verse James 1:5–8 | kept (has translation) |

### How To Live: Systems and Principles

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [066](pages/066.md) | 65 | 6 | b1 heading · b2 reference James 1:21-27 · b3–b9 kjv-verse James 1:21–27 | kept (has translation) |
| [067](pages/067.md) | 66 | 0 | b1 reference Matt 7:6-29 · b2–b11 kjv-verse Matt 7:6–15 | kept (has translation) |
| [068](pages/068.md) | 67 | 0 | b1–b10 kjv-verse Matt 7:16–25 | kept (has translation) |
| [069](pages/069.md) | 68 | 0 | b1–b4 kjv-verse Matt 7:26–29 | kept (has translation) |

### When Have You Passed From Youth Toward Maturity?

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [070](pages/070.md) | 69 | 8 | b1 heading · b2 reference 1 Corinthians 3:1-9 · b3–b11 kjv-verse 1 Corinthians 3:1–9 | kept (has translation) |
| [071](pages/071.md) | 70 | 0 | b1 reference Eph 4:8-15 · b2–b9 kjv-verse Eph 4:8–15 | kept (has translation) |
| [072](pages/072.md) | 71 | 0 | b1 reference James 3:2-13 · b2–b10 kjv-verse James 3:2–10 | kept (has translation) |
| [073](pages/073.md) | 72 | 0 | b1–b3 kjv-verse James 3:11–13 | kept (has translation) |

### When You Consistently Moved From “I” To “Them” And From “Me” To “Us”

| PDF page | Printed | Words to translate | Blocks | Page file |
|---|---|---|---|---|
| [074](pages/074.md) | 73 | 13 | b1 heading · b2 reference Gal 2:20 · b3 kjv-verse Gal 2:20 · b4 reference James 2:1-9 · b5–b11 kjv-verse James 2:1–7 | kept (has translation) |
| [075](pages/075.md) | 74 | 111 | b1–b2 kjv-verse James 2:8–9 · b3 heading · b4–b8 prose | kept (has translation) |
| [076](pages/076.md) | 75 | 0 | b1 kjv-verse Matt 10:1 · b2 reference Luke 9:1-6 · b3–b8 kjv-verse Luke 9:1–6 | kept (has translation) |
| [077](pages/077.md) | 76 | 50 | b1 reference Luke 6:17-19 · b2–b4 kjv-verse Luke 6:17–19 · b5 reference Matt 4:23-24 · b6 kjv-verse Matt 4:23 · b7 heading · b8 prose · b9 reference Matt 8:16-17 · b10 kjv-verse Matt 8:16 · b11 heading · b12 kjv-verse Matt 8:17 | kept (has translation) |
| [078](pages/078.md) | 77 | 0 | b1 reference Matt 15:21-30 · b2–b11 kjv-verse Matt 15:21–30 | kept (has translation) |
| [079](pages/079.md) | 78 | 0 | b1 reference Mark 16:14-20 · b2–b8 kjv-verse Mark 16:14–20 · b9 reference Mark 3:1-15 · b10–b11 kjv-verse Mark 3:1–2 | kept (has translation) |
| [080](pages/080.md) | 79 | 0 | b1–b10 kjv-verse Mark 3:3–12 | kept (has translation) |
| [081](pages/081.md) | 80 | 142 | b1–b3 kjv-verse Mark 3:13–15 · b4 reference Matt 12:14-30 · b5 subheading · b6–b12 prose | kept (has translation) |
| [082](pages/082.md) | 81 | 218 | b1–b10 prose | written |
| [083](pages/083.md) | 82 | 79 | b1 reference Matt 14:34-36 · b2 subheading · b3–b5 prose · b6 subheading · b7 reference Mark 1:14-45 · b8–b12 kjv-verse Mark 1:14–18 | kept (has translation) |
| [084](pages/084.md) | 83 | 0 | b1–b10 kjv-verse Mark 1:19–28 | kept (has translation) |
| [085](pages/085.md) | 84 | 0 | b1–b11 kjv-verse Mark 1:29–39 | kept (has translation) |
| [086](pages/086.md) | 85 | 0 | b1–b6 kjv-verse Mark 1:40–45 · b7 reference Mark 16:15-20 · b8–b11 kjv-verse Mark 16:15–18 | kept (has translation) |
| [087](pages/087.md) | 86 | 5 | b1–b2 kjv-verse Mark 16:19–20 · b3 reference Matt 28:18-20 · b4–b6 kjv-verse Matt 28:18–20 · b7 heading · b8 reference Matt 28:18-20 · b9–b11 kjv-verse Matt 28:18–20 | kept (has translation) |
| [088](pages/088.md) | 87 | 24 | b1–b3 prose · b4 reference Phil 2:8-10 · b5–b7 kjv-verse Phil 2:8–10 · b8 reference John 1:11-13 · b9–b11 kjv-verse John 1:11–13 | kept (has translation) |
| [089](pages/089.md) | 88 | 4 | b1 reference 1 John 3:1-4 · b2–b5 kjv-verse 1 John 3:1–4 · b6 heading · b7 reference John 14:12-17 · b8–b11 kjv-verse John 14:12–15 | kept (has translation) |
| [090](pages/090.md) | 89 | 0 | b1–b2 kjv-verse John 14:16–17 · b3 reference John 16:7-13 · b4–b10 kjv-verse John 16:7–13 | kept (has translation) |
| [091](pages/091.md) | 90 | 0 | b1 reference Matt 8:5-13 · b2–b10 kjv-verse Matt 8:5–13 | kept (has translation) |
| [092](pages/092.md) | 91 | 6 | b1 reference Matt 9:1-8 · b2–b9 kjv-verse Matt 9:1–8 · b10 reference Matt 10:1 · b11 kjv-verse Matt 10:1 · b12 subheading | kept (has translation) |
| [093](pages/093.md) | 92 | 39 | b1 reference Matt 10:5-8 · b2–b5 kjv-verse Matt 10:5–8 · b6 subheading · b7 reference Mark 3:13-15 · b8–b9 kjv-verse Mark 3:13–14 · b10 subheading · b11 prose · b12 subheading | kept (has translation) |
| [094](pages/094.md) | 93 | 4 | b1 reference Mark 6:7-13 · b2–b8 kjv-verse Mark 6:7–13 · b9 subheading | kept (has translation) |
| [095](pages/095.md) | 94 | 41 | b1 reference Acts 1:7-8 · b2–b3 kjv-verse Acts 1:7–8 · b4 prose | kept (has translation) |
| [096](pages/096.md) | 95 | 0 | b1 reference Acts 3:12 · b2 kjv-verse Acts 3:12 · b3 reference Acts 3:16 · b4 kjv-verse Acts 3:16 · b5 reference Acts 3:6 · b6 kjv-verse Acts 3:6 · b7 reference Matt 17:14-20 · b8–b13 kjv-verse Matt 17:14–19 | kept (has translation) |
| [097](pages/097.md) | 96 | 16 | b1 kjv-verse Matt 17:20 · b2–b3 prose · b4 reference Eph 3:14-15 · b5–b6 kjv-verse Eph 3:14–15 · b7 reference Eph 1:19-23 · b8–b12 kjv-verse Eph 1:19–23 | kept (has translation) |
| [098](pages/098.md) | 97 | 0 | footer only | written |
| [099](pages/099.md) | — | 1 | b1 prose | written |
