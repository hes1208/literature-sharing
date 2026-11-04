"""Synthetic fixtures only; no real papers or user examples."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from docx import Document
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


assets = load('pdf_assets')
checker = load('check_share')


def synthetic_pdf(path):
    # A single 200 x 200 point page containing a red rectangle.
    stream = b'1 0 0 rg 20 100 80 60 re f\n'
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Resources << >> /Contents 4 0 R >>',
               b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'endstream']
    out = bytearray(b'%PDF-1.4\n'); offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(out)); out += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'
    start = len(out); out += b'xref\n0 5\n0000000000 65535 f \n'
    for offset in offsets[1:]: out += f'{offset:010d} 00000 n \n'.encode()
    out += f'trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
    path.write_bytes(out)


class HelperTests(unittest.TestCase):
    def test_crop_coordinates_pixels_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); source = tmp / 'test.pdf'; synthetic_pdf(source)
            plan = tmp / 'plan.json'
            plan.write_text(json.dumps({'coordinate_system': 'top-left-points',
                'regions': [{'id': 'fig1', 'page': 1, 'bbox': [20, 40, 100, 100]}]}))
            manifest = assets.export_assets(source, tmp / 'out', plan, [1], 144)
            with Image.open(tmp / 'out/fig1.png') as image:
                self.assertEqual(image.size, (160, 120))
                red, green, blue = image.getpixel((80, 60))
                self.assertGreater(red, 240); self.assertLess(green, 15); self.assertLess(blue, 15)
            self.assertEqual(manifest['source_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(len(manifest['assets']), 2)

    def test_reject_invalid_crop_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); source = tmp / 'test.pdf'; synthetic_pdf(source)
            for item in [{'id': '../escape', 'page': 1, 'bbox': [0, 0, 20, 20]},
                         {'id': 'fig1', 'page': 0, 'bbox': [0, 0, 20, 20]},
                         {'id': 'fig1', 'page': 1, 'bbox': [0, 0, 201, 20]},
                         {'id': 'fig1', 'page': 1, 'bbox': [30, 0, 20, 20]}]:
                plan = tmp / 'plan.json'
                plan.write_text(json.dumps({'coordinate_system': 'top-left-points', 'regions': [item]}))
                with self.assertRaises(ValueError): assets.export_assets(source, tmp / 'out', plan)
                self.assertFalse((tmp / 'out').exists())

    def make_document(self, tmp, narrative=True):
        image = tmp / 'fig1.png'; Image.new('RGB', (100, 50), 'white').save(image)
        d = Document()
        for label in ['原文标题', '原文作者', '作者机构', '原文期刊', '发表日期', '原文链接']:
            d.add_paragraph(label + '：Example')
        for heading in ['中文摘要', '背景与目的', '方法', '结果', '讨论', '政策启示']:
            d.add_paragraph(heading)
        if narrative: d.add_paragraph('示例结果（图1）。')
        d.add_picture(str(image)); d.add_paragraph('图1 示例图名')
        d.add_paragraph('英文摘要'); d.add_paragraph('Synthetic abstract. No real paper.')
        docx = tmp / 'share.docx'; d.save(docx)
        ledger = tmp / 'ledger.json'; ledger.write_text(json.dumps({'objects': [
            {'kind': 'figure', 'number': '1', 'source_page': 1, 'screenshot': 'fig1.png',
             'caption': '图1 示例图名', 'citation': '图1'}]}, ensure_ascii=False), encoding='utf-8')
        return docx, ledger

    def test_document_coverage_and_abstract(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); docx, ledger = self.make_document(tmp)
            abstract = tmp / 'abstract.txt'; abstract.write_text('Synthetic abstract.\nNo real paper.')
            self.assertTrue(checker.check_document(docx, ledger, abstract)['ok'])
            abstract.write_text('A different abstract.')
            self.assertFalse(checker.check_document(docx, ledger, abstract)['ok'])

    def test_caption_is_not_narrative_citation(self):
        with tempfile.TemporaryDirectory() as tmp:
            docx, ledger = self.make_document(Path(tmp), narrative=False)
            self.assertFalse(checker.check_document(docx, ledger)['ok'])
        self.assertFalse(checker.contains('图10', '图1'))

    def test_reports_native_tables_and_body_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); docx, ledger = self.make_document(tmp)
            report = checker.check_document(docx, ledger, max_body_chars=1)
            self.assertEqual(report['native_tables'], 0)
            self.assertGreater(report['body_cjk_chars'], 0)
            self.assertTrue(any('character budget' in w for w in report['warnings']))

            doc = Document(docx)
            doc.add_table(rows=2, cols=2)
            doc.save(docx)
            report = checker.check_document(docx, ledger)
            self.assertEqual(report['native_tables'], 1)
            self.assertTrue(any('native table' in w for w in report['warnings']))


if __name__ == '__main__':
    unittest.main()
