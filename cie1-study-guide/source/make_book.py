#!/usr/bin/env python3
"""Unit-wise build of the SE&M CIE-1 study guide.

  python3 make_book.py            -> out/SEM_CIE1_Complete_Guide.pdf + out/SEM_CIE1_Unit{1,2,3}.pdf
  python3 make_book.py --full     -> only the complete guide
"""
import html as H
import os
import re
import subprocess
import sys

from pypdf import PdfReader, PdfWriter

import build  # helpers: read, page, strip_tags, headings, add_markers, find_pages, sheets

ROOT = build.ROOT
OUT = os.path.join(ROOT, 'out')

UNITS = [
    dict(n=1, cls='unit-1', color='#4f46e5', light='#8b93ff',
         title='Software Process &amp; Agile Development',
         short='Process &amp; Agile',
         lede='What software engineering is, how software is built step by step (process models), and how modern teams build it in short iterations (agile, XP, Scrum).',
         chapters=['ch1', 'ch2', 'ch3'],
         syllabus=['<b>Introduction:</b> Professional software development, Software engineering ethics.',
                   '<b>Software processes:</b> Software process models, Process activities, Coping with change, Process improvement.',
                   '<b>Agile Software Development:</b> Agile methods, Agile development techniques, Agile project management.'],
         lab='Comparative analysis of software process models on the real-time case study application.',
         co='<b>CO1</b>: Explain professional software development practices, process models, ethical aspects, and apply agile principles and project management techniques in software engineering.',
         scope='<b>Whole unit</b> is in CIE-1.'),
    dict(n=2, cls='unit-2', color='#0d9488', light='#2dd4bf',
         title='Requirements Engineering &amp; Design Concepts',
         short='Requirements &amp; Design',
         lede='How to find out, write down, check and manage what a system must do, and the core ideas every good software design is built on.',
         chapters=['ch4', 'ch5'],
         syllabus=['<b>Requirements engineering:</b> Functional and Non-functional requirements, Requirements engineering processes, Requirements elicitation, Requirements specification, Requirements validation, Requirements change.',
                   '<b>Design Concepts:</b> Design Within the Context of Software Engineering, Design Concepts, The Design Model.'],
         lab='Analysis of the real-time case study application.',
         co='<b>CO2</b>: Analyze the functional and non-functional requirements and design concepts for the given problem.',
         scope='<b>Whole unit</b> is in CIE-1.'),
    dict(n=3, cls='unit-3', color='#d97706', light='#fbbf24',
         title='Architectural Design (CIE-1 part)',
         short='Architecture',
         lede='The big-picture structure of a system: the decisions architects make and the different views used to describe an architecture.',
         chapters=['ch6'],
         syllabus=['<b>Architectural Design:</b> Architectural design decisions, Architectural views, <span class="out">Architectural patterns.</span>',
                   '<span class="out"><b>Design and implementation:</b> Object-oriented design using the UML, Design patterns, Implementation issues.</span>'],
         lab='High level and low level design of the analysed real-time case study application.',
         co='<b>CO3</b>: Develop architectural and detailed design using UML and design patterns.',
         scope='<b>Only up to architectural views</b> is in CIE-1. Struck-through topics come later.'),
]


def render(html_text, out_pdf, cover=False, label=None):
    tmp = out_pdf[:-4] + '.html'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(html_text)
    cmd = ['node', os.path.join(ROOT, 'render.cjs'), tmp, out_pdf]
    if cover:
        cmd.append('--cover')
    if label:
        cmd.append('--label=' + label)
    subprocess.run(cmd, check=True)


def chapter_info(name):
    frag = build.read(name)
    t = re.search(r'<h1\b[^>]*>(.*?)</h1>', frag, flags=re.S)
    s = re.search(r'<p class="sub">(.*?)</p>', frag, flags=re.S)
    return (build.strip_tags(t.group(1)) if t else name,
            build.strip_tags(s.group(1)) if s else '')


def chno(name):
    m = re.match(r'ch(\d+)$', name)
    return m.group(1) if m else ''


def present(chs):
    return [c for c in chs if build.read(c)]


# ---------------------------------------------------------------- pieces
def divider(u, pages):
    cards = []
    for c in present(u['chapters']):
        title, sub = chapter_info(c)
        pg = pages.get(f'{c}-top')
        cards.append(f'<a href="#{c}-top" class="ud-ch"><div class="no"><small>CHAPTER</small>{chno(c)}</div>'
                     f'<div><div class="tt">{H.escape(title)}</div><div class="tp">{H.escape(sub)}</div></div>'
                     f'<div class="pg">{"page " + str(pg) if pg else ""}</div></a>')
    syl = ''.join(f'<p>{p}</p>' for p in u['syllabus'])
    return f'''<section class="unit-div {u['cls']}" id="unit{u['n']}">
<div class="ud">
  <div class="ud-num">{u['n']}</div>
  <span class="ud-tag">CIE-1 · Unit {u['n']}</span>
  <h1 class="ud-title" id="unit{u['n']}-top">Unit {u['n']}: {u['title']}</h1>
  <p class="ud-lede">{u['lede']}</p>
  <div class="ud-lbl">Syllabus, word for word</div>
  <div class="ud-box">{syl}</div>
  <div class="ud-lbl">Chapters in this unit</div>
  <div class="ud-chapters">{''.join(cards)}</div>
  <div class="ud-grid">
    <div><div class="ud-lbl">Course outcome</div>{u['co']}</div>
    <div><div class="ud-lbl">Lab component</div>{u['lab']}</div>
    <div><div class="ud-lbl">CIE-1 scope</div>{u['scope']}</div>
  </div>
</div>
</section>'''


def toc(units, pages, with_playbook=True):
    rows = []
    for u in units:
        upg = pages.get('unit%d-top' % u['n'], '00')
        rows.append(f'<a href="#unit{u["n"]}-top" class="{u["cls"]}"><div class="toc-unit"><span class="un">Unit {u["n"]}</span>'
                    f'<span class="t">{u["title"]}</span><span class="dots"></span>'
                    f'<span class="pg">{upg}</span></div></a>')
        for c in present(u['chapters']):
            for tag, hid, num, title in build.headings(build.read(c)):
                pg = pages.get(hid, '00')
                if tag == 'h1':
                    rows.append(f'<a href="#{hid}" class="{u["cls"]}"><div class="toc-ch"><span class="chn">CH {chno(c)}</span>'
                                f'<span class="t">{H.escape(title)}</span><span class="dots"></span>'
                                f'<span class="pg">{pg}</span></div></a>')
                else:
                    t = (num + '  ' if num else '') + title
                    rows.append(f'<a href="#{hid}" class="{u["cls"]}"><div class="toc-row"><span class="t">{H.escape(t)}</span>'
                                f'<span class="dots"></span><span class="pg">{pg}</span></div></a>')
    if with_playbook and build.read('back'):
        rows.append('<a href="#playbook-top" class="unit-1" style="--u:#1f2a5c;--u-dark:#1f2a5c;--u-soft:#eceffa">'
                    '<div class="toc-ch" style="margin-top:14pt"><span class="chn">EXAM</span><span class="t">Exam-Day Playbook</span>'
                    f'<span class="dots"></span><span class="pg">{pages.get("playbook-top", "00")}</span></div></a>')
    return '\n'.join(rows)


def front_parts():
    front = build.read('front')
    cut = front.index('<div class="pagebreak"></div>\n<h2 style="margin-top:0">Contents</h2>')
    start = front[:cut] + '</section>'
    return start


def contents_page(units, pages, heading):
    return (f'<section class="front unit-1" style="break-before:page">'
            f'<h2 style="margin-top:0">{heading}</h2><div class="toc">{toc(units, pages)}</div></section>')


def unit_cover(u):
    style = re.search(r'<style>.*?</style>', build.read('cover'), flags=re.S).group(0)
    chs = ''.join(f'<li><b>Chapter {chno(c)}</b> · {H.escape(chapter_info(c)[0])}</li>' for c in present(u['chapters']))
    syl = ''.join(f'<p>{p}</p>' for p in u['syllabus'])
    return style + f'''
<style>
  .cover .bignum {{ position:absolute; right:14mm; top:8mm; font-family:"Jakarta",sans-serif; font-weight:800; font-size:230pt; line-height:1; color:{u['light']}; opacity:.18; }}
  .cover .ucard {{ margin-top:auto; background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.14); border-top:4pt solid {u['light']}; border-radius:12pt; padding:6mm; }}
  .cover .ucard .lbl {{ font-size:7.6pt; font-weight:800; letter-spacing:.16em; text-transform:uppercase; color:{u['light']}; margin-bottom:2mm; }}
  .cover .ucard ul {{ list-style:none; padding:0; margin:0 0 4mm; font-size:11pt; color:#e3e7ff; line-height:1.6; }}
  .cover .ucard .syl p {{ margin:0 0 1.5mm; font-size:9pt; color:#c9cff5; line-height:1.45; }}
  .cover .ucard .syl .out {{ color:#7d86b8; text-decoration:line-through; }}
  .cover .ucard .syl b, .cover .ucard ul b {{ color:#fff; }}
  .cover .ucard .syl .out b {{ color:inherit; }}
</style>
<div class="cover">
  <svg class="bg" viewBox="0 0 794 1123" width="794" height="1123" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="uc-g1" cx="0.85" cy="0.12" r="0.6"><stop offset="0" stop-color="{u['color']}" stop-opacity=".6"/><stop offset="1" stop-color="{u['color']}" stop-opacity="0"/></radialGradient>
      <pattern id="uc-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#ffffff" fill-opacity=".07"/></pattern>
    </defs>
    <rect width="794" height="1123" fill="url(#uc-g1)"/><rect width="794" height="1123" fill="url(#uc-dots)"/>
  </svg>
  <div class="bignum">{u['n']}</div>
  <div class="inner">
    <div class="eyebrow"><span class="pill" style="background:{u['color']}">CIE-1 Study Guide</span><span>Unit {u['n']} of 3 · CS51</span></div>
    <div class="title" style="font-size:40pt">Unit {u['n']}<br><span style="color:{u['light']}">{u['short']}</span></div>
    <div class="code">SOFTWARE ENGINEERING &amp; MODELLING</div>
    <div class="lede">{u['lede']}</div>
    <div class="ucard">
      <div class="lbl">In this unit</div><ul>{chs}</ul>
      <div class="lbl">Syllabus</div><div class="syl">{syl}</div>
    </div>
    <div class="foot">
      <div>Built from <b>your lecture slides</b>, <b>Sommerville (10th ed)</b><br>and <b>Pressman</b>.</div>
      <div style="text-align:right">Course coordinators<br><b>Mr. Pradeep Kumar D · Dr Shilpa S Chaudhari</b></div>
    </div>
  </div>
</div>'''


def find_pages(pdf):
    """Heading id -> 1-based page: link targets (named destinations) first, text markers as fallback."""
    pages = build.find_pages(pdf)
    r = PdfReader(pdf)
    for k, v in r.named_destinations.items():
        pages[k.lstrip('/')] = r.get_destination_page_number(v) + 1
    return pages


# ---------------------------------------------------------------- outline
def add_outline(w, units, pages, offset, extras):
    """extras: list of (title, page) for top-level items before the units."""
    for title, pg in extras:
        w.add_outline_item(title, offset + pg - 1)
    for u in units:
        up = pages.get(f'unit{u["n"]}-top')
        if up is None:
            continue
        unode = w.add_outline_item(f'Unit {u["n"]}: {H.unescape(u["title"])}', offset + up - 1, bold=True)
        for c in present(u['chapters']):
            cnode = None
            for tag, hid, num, title in build.headings(build.read(c)):
                pg = pages.get(hid)
                if pg is None:
                    continue
                if tag == 'h1':
                    cnode = w.add_outline_item(f'Chapter {chno(c)} · {title}', offset + pg - 1, parent=unode)
                else:
                    w.add_outline_item((num + ' ' if num else '') + title, offset + pg - 1, parent=cnode or unode)
    if 'playbook-top' in pages:
        w.add_outline_item('Exam-Day Playbook', offset + pages['playbook-top'] - 1, bold=True)


# ---------------------------------------------------------------- builds
def make(units, out_name, cover_html, heading, label, with_start, title_meta):
    os.makedirs(OUT, exist_ok=True)
    back = build.read('back')
    start = front_parts() if with_start else ''

    def assemble(pages, markers):
        mk = build.add_markers if markers else (lambda s: s)
        parts = []
        if start:
            parts.append(start)
        parts.append(mk(contents_page(units, pages, heading).replace('<h2 style="margin-top:0">', '<h2 style="margin-top:0" id="contents-top">', 1)))
        for u in units:
            parts.append(mk(divider(u, pages)))
            parts += [mk(build.read(c)) for c in present(u['chapters'])]
        if back:
            parts.append(mk(back))
        return build.page('\n'.join(parts), title=title_meta)

    base = os.path.join(OUT, out_name)
    render(assemble({}, True), base + '.pass1.pdf', label=label)
    pages = find_pages(base + '.pass1.pdf')
    render(assemble(pages, False), base + '.body.pdf', label=label)
    pages2 = pages  # pass 2 has the same layout; only the (fixed-width) page numbers change
    render(build.page(cover_html), base + '.cover.pdf', cover=True)

    w = PdfWriter()
    w.append(PdfReader(base + '.cover.pdf'), import_outline=False)
    ncover = len(w.pages)
    w.append(PdfReader(base + '.body.pdf'), import_outline=False)
    extras = []
    if with_start:
        extras.append(('Start here: how to use this guide', 1))
    if 'contents-top' in pages2:
        extras.append(('Contents', pages2['contents-top']))
    add_outline(w, units, pages2, ncover, extras)
    w.add_metadata({'/Title': title_meta, '/Author': 'CIE-1 Study Guide',
                    '/Subject': 'Software Engineering and Modelling (CS51)'})
    w.page_mode = '/UseOutlines'
    final = os.path.join(OUT, out_name + '.pdf')
    with open(final, 'wb') as f:
        w.write(f)
    for ext in ('.pass1.pdf', '.pass1.html', '.body.html', '.cover.html'):
        p = base + ext
        if os.path.exists(p):
            os.remove(p)
    print(f'{final}: {len(w.pages)} pages, {len(pages2)} headings located')
    return final


def main():
    full_only = '--full' in sys.argv
    make(UNITS, 'SEM_CIE1_Complete_Guide', build.read('cover'), 'Contents', 'CIE-1 Study Guide', True,
         'Software Engineering & Modelling (CS51) — CIE-1 Study Guide (Units 1–3)')
    if full_only:
        return
    for u in UNITS:
        if not present(u['chapters']):
            continue
        make([u], f'SEM_CIE1_Unit{u["n"]}', unit_cover(u), f'Contents · Unit {u["n"]}',
             f'Unit {u["n"]} · CIE-1 Study Guide', True,
             f'Software Engineering & Modelling (CS51) — CIE-1 Study Guide, Unit {u["n"]}')


if __name__ == '__main__':
    main()
