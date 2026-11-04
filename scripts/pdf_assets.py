#!/usr/bin/env python3
"""Render PDF pages or crop verified rectangles. Coordinates: top-left points."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

import pypdfium2 as pdfium


def validate_regions(items, pdf):
    if not isinstance(items, list) or not items:
        raise ValueError('regions must be a non-empty list')
    seen = set()
    for item in items:
        name = item.get('id', '')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', name):
            raise ValueError(f'Unsafe or missing region id: {name!r}')
        if name in seen:
            raise ValueError(f'Duplicate region id: {name}')
        seen.add(name)
        page = item.get('page')
        if type(page) is not int or not 1 <= page <= len(pdf):
            raise ValueError(f'{name}: page must be a 1-based PDF page number')
        box = item.get('bbox')
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError(f'{name}: bbox must contain four coordinates')
        if not all(type(x) in (int, float) and math.isfinite(x) for x in box):
            raise ValueError(f'{name}: bbox coordinates must be finite numbers')
        width, height = pdf[page - 1].get_size()
        left, top, right, bottom = box
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise ValueError(f'{name}: bbox outside displayed page {width} x {height}')
    return items


def export_assets(pdf_path, output_dir, plan=None, pages=None, dpi=300):
    if not 72 <= dpi <= 600:
        raise ValueError('dpi must be between 72 and 600')
    pdf_path, output_dir = Path(pdf_path), Path(output_dir)
    raw = pdf_path.read_bytes()
    pdf = pdfium.PdfDocument(raw)
    try:
        items = []
        if plan is not None:
            payload = json.loads(Path(plan).read_text(encoding='utf-8'))
            if payload.get('coordinate_system') != 'top-left-points':
                raise ValueError('coordinate_system must be top-left-points')
            items = validate_regions(payload.get('regions'), pdf)
        pages = pages or []
        if not items and not pages:
            raise ValueError('Provide a plan or at least one page to render')
        for page in pages:
            if type(page) is not int or not 1 <= page <= len(pdf):
                raise ValueError(f'Invalid page: {page}')
        reserved = {f'page-{page:04d}' for page in pages}
        if any(item['id'] in reserved for item in items):
            raise ValueError('A region id conflicts with a whole-page output name')
        output_dir.mkdir(parents=True, exist_ok=True)
        records = []
        for page_number in sorted(set(pages) | {i['page'] for i in items}):
            page = pdf[page_number - 1]
            bitmap = page.render(scale=dpi / 72)
            try:
                image = bitmap.to_pil().copy()
            finally:
                bitmap.close()
            width, height = page.get_size()
            if page_number in pages:
                filename = f'page-{page_number:04d}.png'
                image.save(output_dir / filename)
                records.append({'id': Path(filename).stem, 'page': page_number,
                                'bbox': [0, 0, width, height], 'file': filename})
            for item in items:
                if item['page'] != page_number:
                    continue
                # Use actual rendered dimensions, avoiding rounding drift at edges.
                sx, sy = image.width / width, image.height / height
                a, b, c, e = item['bbox']
                pixels = [round(a * sx), round(b * sy), round(c * sx), round(e * sy)]
                if pixels[0] == pixels[2] or pixels[1] == pixels[3]:
                    raise ValueError(f"{item['id']}: crop is smaller than one pixel")
                filename = item['id'] + '.png'
                image.crop(pixels).save(output_dir / filename)
                records.append({**item, 'file': filename})
            image.close()
            page.close()
        result = {'source_filename': pdf_path.name,
                  'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'dpi': dpi, 'coordinate_system': 'top-left-points', 'assets': records}
        (output_dir / 'assets-manifest.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return result
    finally:
        pdf.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', required=True, type=Path)
    parser.add_argument('--out-dir', required=True, type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--render-pages', type=int, nargs='+', default=[])
    parser.add_argument('--dpi', type=int, default=300)
    args = parser.parse_args()
    try:
        result = export_assets(args.pdf, args.out_dir, args.plan, args.render_pages, args.dpi)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, pdfium.PdfiumError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')
    print(f"Exported {len(result['assets'])} image(s); inspect them before insertion.")


if __name__ == '__main__':
    main()
