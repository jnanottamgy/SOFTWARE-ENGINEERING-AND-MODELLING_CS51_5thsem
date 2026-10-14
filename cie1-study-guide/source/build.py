#!/usr/bin/env python3
"""Build the SE&M CIE-1 study guide.

  python3 build.py                 -> full book: out/SEM_CIE1_Study_Guide.pdf
  python3 build.py --only ch2      -> preview one fragment: preview/ch2.pdf + preview/ch2/sheet-XX.png
"""
import html as htmlmod
import os
import re
import subprocess
import sys
from pypdf import PdfReader, PdfWriter

ROOT = os.path.dirname(os.path.abspath(__file__))
FRAG = os.path.join(ROOT, 'fragments')
ORDER = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6']
CSS = open(os.path.join(ROOT, 'styles.css'), encoding='utf-8').read()


def read(name):
    p = os.path.join(FRAG, name + '.html')
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def page(body, title='SE&M CIE-1 Study Guide'):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>')


def render(html_text, out_pdf, cover=False):
    tmp = out_pdf[:-4] + '.html'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(html_text)
    cmd = ['node', os.path.join(ROOT, 'render.cjs'), tmp, out_pdf] + (['--cover'] if cover else [])
    subprocess.run(cmd, check=True)


def strip_tags(s):
    s = re.sub(r'<span class="prio[^"]*">.*?</span>', '', s, flags=re.S)
    s = re.sub(r'<span class="pmark">.*?</span>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', htmlmod.unescape(s)).strip()


def headings(frag):
    """Return [(level, id, number, title)] for h1 (chapter) and h2 (sections) carrying an id."""
    out = []
    for m in re.finditer(r'<(h1|h2)\b([^>]*)>(.*?)</\1>', frag, flags=re.S):
        tag, attrs, inner = m.groups()
        idm = re.search(r'\bid="([^"]+)"', attrs)
        if not idm:
            continue
        num = re.search(r'<span class="num">(.*?)</span>', inner, flags=re.S)
        number = strip_tags(num.group(1)) if num else ''
        title = strip_tags(re.sub(r'<span class="num">.*?</span>', '', inner, flags=re.S))
        out.append((tag, idm.group(1), number, title))
    return out


def add_markers(frag):
    return re.sub(r'(<(h1|h2)\b[^>]*\bid="([^"]+)"[^>]*>)',
                  lambda m: m.group(1) + f'<span class="pmark">@@{m.group(3)}@@</span>', frag)


def unit_of(frag):
    m = re.search(r'class="chapter (unit-\d)"', frag)
    return m.group(1) if m else 'unit-1'


def toc_html(frags, pages):
    rows = []
    for name, frag in frags:
        unit = unit_of(frag)
        for tag, hid, num, title in headings(frag):
            pg = pages.get(hid, '00')
            if tag == 'h1':
                label = {'unit-1': 'Unit 1', 'unit-2': 'Unit 2', 'unit-3': 'Unit 3'}[unit]
                chno = re.match(r'ch(\d+)$', name)
                full = (f'Chapter {chno.group(1)} · ' if chno else '') + title
                rows.append(f'<div class="{unit}"><div class="toc-ch"><span class="unit">{label}</span>'
                            f'<span class="t">{htmlmod.escape(full)}</span><span class="dots"></span>'
                            f'<span class="pg">{pg}</span></div></div>')
            else:
                t = (num + '  ' if num else '') + title
                rows.append(f'<div class="{unit}"><div class="toc-row"><span class="t">{htmlmod.escape(t)}</span>'
                            f'<span class="dots"></span><span class="pg">{pg}</span></div></div>')
    return '\n'.join(rows)


def find_pages(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    pages = {}
    for i, ptxt in enumerate(txt.split('\f'), 1):
        for hid in re.findall(r'@@([A-Za-z0-9_.-]+)@@', ptxt):
            pages.setdefault(hid, i)
    return pages


def sheets(pdf, outdir, dpi=62):
    """Rasterise pages and tile them two-up so they can be eyeballed quickly."""
    from PIL import Image
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', pdf, os.path.join(outdir, 'p')], check=True)
    ps = sorted(f for f in os.listdir(outdir) if f.startswith('p-'))
    n = 0
    for i in range(0, len(ps), 2):
        ims = [Image.open(os.path.join(outdir, f)) for f in ps[i:i + 2]]
        w = sum(im.width for im in ims) + 12 * (len(ims) - 1)
        h = max(im.height for im in ims)
        sheet = Image.new('RGB', (w, h), (120, 120, 120))
        x = 0
        for im in ims:
            sheet.paste(im, (x, 0)); x += im.width + 12
        n += 1
        sheet.save(os.path.join(outdir, f'sheet-{n:02d}.png'))
    for f in ps:
        os.remove(os.path.join(outdir, f))
    return n


def preview(name):
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    frag = read(name)
    if not frag:
        sys.exit(f'fragments/{name}.html not found')
    out = os.path.join(ROOT, 'preview', name + '.pdf')
    render(page(frag), out)
    n = len(PdfReader(out).pages)
    s = sheets(out, os.path.join(ROOT, 'preview', name))
    print(f'{out}: {n} pages -> {s} sheets in preview/{name}/ (sheet-01.png = pages 1-2, sheet-02.png = pages 3-4, ...)')


def full():
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    frags = [(n, read(n)) for n in ORDER if read(n)]
    front = read('front')
    back = read('back')

    def assemble(pages, markers):
        body = front.replace('<!--TOC-->', toc_html(frags, pages))
        parts = [body] + [add_markers(f) if markers else f for _, f in frags] + [back]
        return page('\n'.join(parts))

    tmp = os.path.join(ROOT, 'out', 'pass1.pdf')
    render(assemble({}, True), tmp)
    pages = find_pages(tmp)
    body_pdf = os.path.join(ROOT, 'out', 'body.pdf')
    render(assemble(pages, False), body_pdf)

    cover_pdf = os.path.join(ROOT, 'out', 'cover.pdf')
    render(page(read('cover')), cover_pdf, cover=True)

    w = PdfWriter()
    w.append(PdfReader(cover_pdf), import_outline=False)
    w.append(PdfReader(body_pdf), import_outline=True)
    w.add_metadata({'/Title': 'Software Engineering & Modelling (CS51) — CIE-1 Study Guide',
                    '/Subject': 'Units 1, 2 and Unit 3 up to architectural views'})
    w.page_mode = '/UseOutlines'
    final = os.path.join(ROOT, 'out', 'SEM_CIE1_Study_Guide.pdf')
    with open(final, 'wb') as f:
        w.write(f)
    print(final, len(w.pages), 'pages;', len(pages), 'headings located')


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--only':
        preview(sys.argv[2])
    else:
        full()
