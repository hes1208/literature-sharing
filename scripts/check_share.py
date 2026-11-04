#!/usr/bin/env python3
"""Mechanical DOCX coverage checks; NOT a scientific or visual approval."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

from docx import Document


def normalized(text):
    # Keep wording and punctuation; normalize Unicode and extraction whitespace only.
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', text))


def contains(text, needle):
    text, needle = normalized(text), normalized(needle)
    pattern = re.escape(needle) + (r'(?![0-9])' if needle[-1:].isdigit() else '')
    return bool(re.search(pattern, text))


CAPTION_RE = re.compile(r'^\s*(图|表|注\s*[:：]|Figure|Table|Note\s*[:：])')


def body_cjk_count(paragraphs):
    """Approximate Chinese body length, excluding captions, notes and heading lines."""
    total = 0
    for text in paragraphs:
        if not text.strip() or CAPTION_RE.match(text):
            continue
        total += len(re.findall(r'[\u4e00-\u9fff]', text))
    return total


def check_document(docx, ledger_path, abstract_path=None, max_body_chars=None):
    doc = Document(docx)
    ledger_path = Path(ledger_path)
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    paragraphs = [p.text for p in doc.paragraphs]
    all_text = '\n'.join(paragraphs)
    errors, warnings = [], []
    for label in ['原文标题', '原文作者', '作者机构', '原文期刊', '发表日期', '原文链接']:
        if not re.search(re.escape(label) + r'\s*[:：]\s*\S', all_text):
            errors.append(f'Missing or empty metadata field: {label}')
    for label in ['摘要', '背景', '目的', '方法', '结果', '英文摘要']:
        if label not in all_text:
            errors.append(f'Missing section keyword: {label}')
    sections = ledger.get('sections', {})
    for flag, word in [('discussion', '讨论'), ('conclusions', '结论'), ('policy', '政策')]:
        if sections.get(flag) and word not in all_text:
            errors.append(f'Section required by ledger is absent: {word}')
    objects = ledger.get('objects')
    if not isinstance(objects, list) or not objects:
        raise ValueError('ledger.objects must be a non-empty list')
    seen = set()
    for item in objects:
        kind, number = item.get('kind'), item.get('number')
        if kind not in ('figure', 'table', 'equation') or not isinstance(number, str) or not number:
            raise ValueError('Each object needs kind and a non-empty string number')
        identity = (kind, number)
        if identity in seen:
            raise ValueError(f'Duplicate ledger object: {identity}')
        seen.add(identity)
        if type(item.get('source_page')) is not int or item['source_page'] < 1:
            errors.append(f'{identity}: invalid or missing source_page')
        screenshot = item.get('screenshot')
        if not screenshot or not (ledger_path.parent / screenshot).is_file():
            errors.append(f'{identity}: screenshot file is missing')
        caption = item.get('caption', '')
        if not isinstance(caption, str) or not caption:
            errors.append(f'{identity}: caption string is missing')
            continue
        if not any(contains(text, caption) for text in paragraphs):
            errors.append(f'{identity}: expected caption/label absent: {caption}')
        if kind in ('figure', 'table'):
            citation = item.get('citation', '')
            if not isinstance(citation, str) or not citation:
                errors.append(f'{identity}: narrative citation string is missing')
            elif not any(contains(text, citation) and not contains(text, caption)
                         for text in paragraphs):
                errors.append(f'{identity}: no separate narrative citation: {citation}')
        else:
            symbols = item.get('symbols')
            if not isinstance(symbols, list) or not symbols or not all(
                isinstance(symbol, str) and symbol.strip() for symbol in symbols
            ):
                errors.append(f'{identity}: symbol checklist missing')
            else:
                for symbol in symbols:
                    if symbol not in all_text:
                        errors.append(f'{identity}: symbol missing from editable text: {symbol}')
    # Only a lower bound: multiple-part screenshots and native tables need human review.
    if len(doc.inline_shapes) < len(objects):
        warnings.append(f'{len(doc.inline_shapes)} inline image(s) for {len(objects)} objects; '
                        'verify combined, floating or missing screenshots manually.')
    if doc.tables:
        warnings.append(f'{len(doc.tables)} native table object(s) found. Tables are expected to be '
                        'screenshots with the original body untranslated; confirm each one is a layout '
                        'table or a declared supplementary-material rebuild, not a translated table.')
    body_chars = body_cjk_count(paragraphs)
    if max_body_chars and body_chars > max_body_chars:
        warnings.append(f'Approximate Chinese body length {body_chars} exceeds the {max_body_chars} '
                        'character budget; compress background and results before delivery.')
    if abstract_path:
        original = Path(abstract_path).read_text(encoding='utf-8').strip()
        if not original:
            raise ValueError('Reference abstract is empty')
        # Abstract must appear as a complete contiguous sequence of editable paragraphs.
        if normalized(original) not in normalized(all_text):
            errors.append('Original abstract does not match editable document text')
    else:
        warnings.append('No reference abstract supplied; abstract fidelity was not checked.')
    warnings.append('Manual review remains required: source inventory completeness, screenshot '
                    'content, Chinese translation, statistics, symbol meanings, caption position, '
                    'one-to-one correspondence of Results/Discussion subheadings and every final '
                    'rendered page. Text in table cells/text boxes is not checked.')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings,
            'ledger_objects': len(objects), 'inline_images': len(doc.inline_shapes),
            'native_tables': len(doc.tables), 'body_cjk_chars': body_chars}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docx', required=True, type=Path)
    parser.add_argument('--ledger', required=True, type=Path)
    parser.add_argument('--abstract-file', type=Path)
    parser.add_argument('--max-body-chars', type=int, default=None,
                        help='warn when the approximate Chinese body length exceeds this budget')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        report = check_document(args.docx, args.ledger, args.abstract_file, args.max_body_chars)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
