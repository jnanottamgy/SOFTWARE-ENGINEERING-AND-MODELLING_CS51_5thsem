#!/usr/bin/env python3
"""Regenerate the 'Diagrams you must be able to draw' checklist and the cover counts from the chapter fragments."""
import re, html as H
import build
titles = {'ch1': 'Introduction', 'ch2': 'Software Processes', 'ch3': 'Agile', 'ch4': 'Requirements Engineering',
          'ch5': 'Design Concepts', 'ch6': 'Architectural Design'}
units = {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 2, 'ch5': 2, 'ch6': 3}
tot_f = tot_q = 0
rows = []
for c in titles:
    f = build.read(c)
    caps = re.findall(r'<figcaption>(.*?)</figcaption>', f, flags=re.S)
    tot_q += len(re.findall(r'class="q"', f)); tot_f += len(caps)
    keep = []
    for cap in caps:
        src = re.search(r'<span class="src">(.*?)</span>', cap, flags=re.S)
        s = build.strip_tags(src.group(1)) if src else ''
        if not re.search(r'Sommerville|Pressman|slide', s, re.I):
            continue
        m = re.match(r'(Fig\s*\d+\.\d+)\s*(.*)', build.strip_tags(cap))
        if not m:
            continue
        name = m.group(2)
        if s and name.endswith(s):
            name = name[:-len(s)].strip()
        name = re.split(r'(?<=[a-z\)])[.:;] ', name)[0].rstrip('.')
        if len(name) > 90:
            name = name[:88].rsplit(' ', 1)[0] + '…'
        keep.append((m.group(1), name))
    rows.append((c, keep))
total = sum(len(k) + 2 for _, k in rows)
cols, ci, cnt = [[], []], 0, 0
for c, keep in rows:
    if ci == 0 and cnt + (len(keep) + 2) / 2 > total / 2:
        ci = 1
    cols[ci].append(f'<h4 class="unit-{units[c]}" style="margin:6pt 0 2pt;color:var(--u-dark)">Ch {c[2]} · {titles[c]}</h4>'
                    '<ul style="list-style:none;padding-left:0;margin-bottom:4pt">' +
                    ''.join(f'<li style="margin:0 0 2pt"><span style="font-family:\'DejaVu Sans\';color:var(--muted)">☐</span> '
                            f'<b>{fig}</b> {H.escape(n)}</li>' for fig, n in keep) + '</ul>')
    cnt += len(keep) + 2
out = ('<h2>Diagrams you must be able to draw</h2>'
       '<p>Every textbook or slide diagram in this guide. Tick each one when you can draw it from memory with all labels. '
       'Diagrams drawn only to help understanding are not listed.</p>'
       f'<div class="cols-2 small" style="color:var(--ink-2)"><div>{"".join(cols[0])}</div><div>{"".join(cols[1])}</div></div>')
p = build.os.path.join(build.FRAG, 'back.html')
s = open(p, encoding='utf-8').read()
s = re.sub(r'<!--BACK-EXTRA-->.*?(?=</section>\s*$)', '<!--BACK-EXTRA-->\n' + out + '\n', s, flags=re.S)
open(p, 'w', encoding='utf-8').write(s)
p = build.os.path.join(build.FRAG, 'cover.html')
c = open(p, encoding='utf-8').read()
c = re.sub(r'<span>\d+\+ diagrams</span>', f'<span>{(tot_f // 10) * 10}+ diagrams</span>', c)
c = re.sub(r'<span>\d+ likely questions \+ how to answer</span>', f'<span>{tot_q} likely questions + how to answer</span>', c)
open(p, 'w', encoding='utf-8').write(c)
print('figures', tot_f, 'questions', tot_q, 'checklist', sum(len(k) for _, k in rows))
