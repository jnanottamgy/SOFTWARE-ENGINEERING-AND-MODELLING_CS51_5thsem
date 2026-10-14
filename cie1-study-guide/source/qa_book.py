#!/usr/bin/env python3
"""Build the CIE-1 'most likely 5-mark questions' booklet: out/SEM_CIE1_Likely_Questions.pdf"""
import html as H
import os
import re

from pypdf import PdfReader, PdfWriter

import build
import make_book as mb

UNITS = [(1, 'unit-1', 'Process & Agile', '#8b93ff'), (2, 'unit-2', 'Requirements & Design', '#2dd4bf'),
         (3, 'unit-3', 'Architecture (CIE-1 part)', '#fbbf24')]


def qa_frag(n):
    return build.read(f'qa{n}')


def questions(n):
    """[(id, number, text)] for each question h2 in unit n."""
    out = []
    for tag, hid, num, title in build.headings(qa_frag(n)):
        if tag == 'h2':
            out.append((hid, num, title))
    return out


def toc(pages):
    rows = []
    for n, cls, short, _ in UNITS:
        if not qa_frag(n):
            continue
        rows.append(f'<a href="#qa{n}-top" class="{cls}"><div class="toc-unit"><span class="un">Unit {n}</span>'
                    f'<span class="t">{H.escape(short)}</span><span class="dots"></span>'
                    f'<span class="pg">{pages.get(f"qa{n}-top", "00")}</span></div></a>')
        for hid, num, title in questions(n):
            t = (num + '  ' if num else '') + title
            rows.append(f'<a href="#{hid}" class="{cls}"><div class="toc-row"><span class="t">{H.escape(t)}</span>'
                        f'<span class="dots"></span><span class="pg">{pages.get(hid, "00")}</span></div></a>')
    rows.append('<a href="#paper-top" class="unit-1" style="--u:#1f2a5c;--u-dark:#1f2a5c;--u-soft:#eceffa">'
                '<div class="toc-ch" style="margin-top:12pt"><span class="chn">PRACTICE</span><span class="t">Predicted CIE-1 papers A and B</span>'
                f'<span class="dots"></span><span class="pg">{pages.get("paper-top", "00")}</span></div></a>')
    return '\n'.join(rows)


def cover():
    style = re.search(r'<style>.*?</style>', build.read('cover'), flags=re.S).group(0)
    nq = sum(1 for n, *_ in UNITS for hid, _, _ in questions(n) if not hid.endswith('-backup'))

    def glance(n):
        m = re.search(r'<ol class="glance"[^>]*>(.*?)</ol>', qa_frag(n), flags=re.S)
        items = re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), flags=re.S) if m else []
        items = [re.sub(r'\s*\((asked|Asked)[^)]*\)', '', build.strip_tags(i)) for i in items]
        return items

    cards = ''.join(
        f'<div class="u" style="--c:{c}"><div class="n">Unit {n} · {len(glance(n))} questions</div><div class="h">{H.escape(s)}</div>'
        f'<ul>{"".join(f"<li>{H.escape(t)}</li>" for t in glance(n)[:5])}</ul></div>'
        for n, _, s, c in UNITS)
    return style + f'''
<div class="cover">
  <svg class="bg" viewBox="0 0 794 1123" width="794" height="1123" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="qc-g1" cx="0.85" cy="0.12" r="0.6"><stop offset="0" stop-color="#db2777" stop-opacity=".45"/><stop offset="1" stop-color="#db2777" stop-opacity="0"/></radialGradient>
      <radialGradient id="qc-g2" cx="0.05" cy="0.75" r="0.5"><stop offset="0" stop-color="#4f46e5" stop-opacity=".4"/><stop offset="1" stop-color="#4f46e5" stop-opacity="0"/></radialGradient>
      <pattern id="qc-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#ffffff" fill-opacity=".07"/></pattern>
    </defs>
    <rect width="794" height="1123" fill="url(#qc-g1)"/><rect width="794" height="1123" fill="url(#qc-g2)"/><rect width="794" height="1123" fill="url(#qc-dots)"/>
    <g transform="translate(676 250)" font-family="Jakarta, sans-serif" font-weight="800" text-anchor="middle">
      <circle r="90" fill="none" stroke="#f472b6" stroke-opacity=".55" stroke-width="3"/>
      <circle r="70" fill="none" stroke="#ffffff" stroke-opacity=".08" stroke-width="1.2" stroke-dasharray="3 6"/>
      <text y="16" font-size="76" fill="#ffffff" fill-opacity=".95">5</text>
      <text y="46" font-size="12.5" letter-spacing="4" fill="#f9a8d4">MARKS</text>
    </g>
  </svg>
  <div class="inner">
    <div class="eyebrow"><span class="pill" style="background:#db2777">CIE-1 Question Bank</span><span>5th Semester · CS51</span></div>
    <div class="title" style="font-size:42pt">Most Likely<br>5-Mark <span class="amp" style="color:#f9a8d4">Questions</span></div>
    <div class="code">SOFTWARE ENGINEERING &amp; MODELLING</div>
    <div class="lede">{nq} questions across all three CIE-1 units, each with a <b>model answer you can write in 10 minutes</b>, chosen using last year's CIE-1 paper and the syllabus.</div>
    <div class="feat"><span>Model answers with diagrams</span><span>Marks split for each answer</span><span>Last year's paper mapped</span><span>2 predicted papers</span></div>
    <div class="units">{cards}</div>
    <div class="foot">
      <div>Companion to the <b>CIE-1 Study Guide</b>. Built from your lecture slides,<br><b>Sommerville (10th ed)</b> and <b>Pressman</b>.</div>
      <div style="text-align:right">Course coordinators<br><b>Mr. Pradeep Kumar D · Dr Shilpa S Chaudhari</b></div>
    </div>
  </div>
</div>'''


def main():
    out = os.path.join(build.ROOT, 'out')
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, 'SEM_CIE1_Likely_Questions')
    front = build.read('qa_front')
    paper = build.read('qa_paper')

    def assemble(pages, markers):
        mk = build.add_markers if markers else (lambda s: s)
        parts = [mk(front.replace('<!--TOC-->', toc(pages)))]
        parts += [mk(qa_frag(n)) for n, *_ in UNITS if qa_frag(n)]
        parts.append(mk(paper))
        return build.page('\n'.join(parts), title='SE&M CIE-1 Most Likely 5-Mark Questions')

    label = 'CIE-1 Likely Questions'
    mb.render(assemble({}, True), base + '.pass1.pdf', label=label)
    pages = mb.find_pages(base + '.pass1.pdf')
    mb.render(assemble(pages, False), base + '.body.pdf', label=label)
    mb.render(build.page(cover()), base + '.cover.pdf', cover=True)

    w = PdfWriter()
    w.append(PdfReader(base + '.cover.pdf'), import_outline=False)
    off = len(w.pages)
    w.append(PdfReader(base + '.body.pdf'), import_outline=False)
    w.add_outline_item('Read this first', off)
    if 'contents-top' in pages:
        w.add_outline_item('Contents', off + pages['contents-top'] - 1)
    for n, cls, short, _ in UNITS:
        if f'qa{n}-top' not in pages:
            continue
        u = w.add_outline_item(f'Unit {n}: {short}', off + pages[f'qa{n}-top'] - 1, bold=True)
        for hid, num, title in questions(n):
            if hid in pages:
                w.add_outline_item(f'{num} {title}'.strip()[:120], off + pages[hid] - 1, parent=u)
    if 'paper-top' in pages:
        w.add_outline_item('Predicted CIE-1 papers', off + pages['paper-top'] - 1, bold=True)
    w.add_metadata({'/Title': 'Software Engineering & Modelling (CS51) — CIE-1 Most Likely 5-Mark Questions'})
    w.page_mode = '/UseOutlines'
    with open(base + '.pdf', 'wb') as f:
        w.write(f)
    for ext in ('.pass1.pdf', '.pass1.html', '.body.pdf', '.body.html', '.cover.pdf', '.cover.html'):
        if os.path.exists(base + ext):
            os.remove(base + ext)
    print(base + '.pdf', len(w.pages), 'pages', len(pages), 'headings')


if __name__ == '__main__':
    main()
