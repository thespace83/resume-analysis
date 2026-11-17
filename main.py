import os
import re
import pymorphy2
from pypdf import PdfReader
from natasha import (
    Segmenter, MorphVocab, NewsEmbedding,
    NewsMorphTagger, NewsNERTagger, Doc,
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
ner_tagger = NewsNERTagger(emb)
pymorph = pymorphy2.MorphAnalyzer()

FIO_GRAMMEMES = {"Name", "Surn", "Patr"}

# «ФИО: Иванов Иван Иванович» — самый надёжный якорь в резюме
FIO_LABEL_RE = re.compile(
    r"(?:ФИО|Ф\.\s*И\.\s*О\.)\s*[:\-]\s*"
    r"([А-ЯЁ][а-яё\-]+(?:\s+[А-ЯЁ][а-яё\-]+){0,3})",
    re.IGNORECASE,
)


def extract_text_pypdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    return "\n".join(p.extract_text() or "" for p in reader.pages)


def looks_like_fio_word(word: str) -> bool:
    """Слово похоже на фамилию/имя/отчество?"""
    word = word.strip(".,;:!?()[]«»\"'")
    if len(word) < 2 or not word[0].isupper():
        return False
    parses = pymorph.parse(word)
    if not parses:
        return False
    return bool(parses[0].tag.grammemes & FIO_GRAMMEMES)


def clean_fio_string(text: str) -> str | None:
    """Оставляем только FIO-слова. Нужно 2 или 3 подряд."""
    words = [w for w in text.split() if looks_like_fio_word(w)]
    if 2 <= len(words) <= 3:
        return " ".join(words)
    return None


def extract_by_label(text: str) -> str | None:
    m = FIO_LABEL_RE.search(text)
    return clean_fio_string(m.group(1)) if m else None


def extract_names_natasha(text: str) -> list[str]:
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    results, seen = [], set()
    for span in doc.spans:
        if span.type != "PER":
            continue
        # span.text — исходный вид (не гоняем через normalize,
        # иначе Грибанова → Грибанов и т.п.)
        cleaned = clean_fio_string(span.text)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            results.append(cleaned)
    return results


def extract_first_fio_from_header(text: str, n_lines: int = 15) -> list[str]:
    """ФИО обычно в первых строках резюме."""
    names = []
    for line in text.splitlines()[:n_lines]:
        cleaned = clean_fio_string(line.strip())
        if cleaned:
            names.append(cleaned)
    return names


HEAD_LINES = 25  # сколько строк сверху считаем «шапкой»
HEAD_CHARS = 1500  # доп. страховка по символам (что наступит раньше)


def get_header(text: str,
               max_lines: int = HEAD_LINES,
               max_chars: int = HEAD_CHARS) -> str:
    lines = text.splitlines()[:max_lines]
    return "\n".join(lines)[:max_chars]


def get_full_name(pdf_path: str) -> str | None:
    text = extract_text_pypdf(pdf_path)
    header = get_header(text)  # <-- ВСЁ ниже отрезано

    # 1) явная метка «ФИО:» — самый надёжный сигнал
    if name := extract_by_label(header):
        return name

    # 2) NER + морфофильтр, но только по шапке
    names = extract_names_natasha(header)
    if names:
        return names[0]

    # 3) построчный скан шапки
    for line in header.splitlines():
        if cleaned := clean_fio_string(line.strip()):
            return cleaned

    return None


if __name__ == "__main__":
    path = "docs"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        print(f'{file}: {get_full_name("docs/" + file)}')
