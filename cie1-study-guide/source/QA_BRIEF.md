# CIE-1 "Most likely 5-mark questions" — writer's brief

You are writing ONE unit of a printed Q&A booklet: model answers for the 5-mark questions most likely to appear in
CIE-1 of Software Engineering and Modelling (CS51) at Ramaiah Institute of Technology. Same design system as the
existing 140-page study guide.

BOOK = /tmp/claude-0/-home-user-SOFTWARE-ENGINEERING-AND-MODELLING-CS51-5thsem/db22c00d-e9f6-5b54-9f7d-d9fa28a5c550/scratchpad/book

Read first:
- BOOK/STYLE_GUIDE.md — the components, SVG rules and preview workflow. Follow its SVG rules exactly (1:1 scale,
  max width 640, font 11–13, ids prefixed, palette). Note: SVG <text> colours work with fill="…" attributes.
- BOOK/styles.css (do not edit).
- The finished study-guide chapters for your unit in BOOK/fragments/chN.html. They are your SOURCE: they already contain
  the verified textbook wording, lists, tables and SVG diagrams. Reuse their content and diagrams (copy an SVG and
  re-prefix every id inside it to your fragment prefix, e.g. `qa1-arr`). Do not introduce facts that aren't in those
  chapters.

## The exam
- CIE-1: 30 marks, 1 hour. Q1 compulsory (parts a, b, c — 5 marks each, one per course outcome/unit); then Q2 OR Q3
  (each 3 × 5 marks). So a 5-mark answer gets about 10 minutes: roughly one A4 page in the answer booklet.
- Last year's paper (CIE-1, Oct 2024) is given in your task; questions repeated from it are tagged.

## How to write each answer
The answer is a MODEL ANSWER the student can reproduce in ~10 minutes — not a chapter. Write it the way a top
student writes it in the exam:
1. Opening definition in textbook words (1–2 lines).
2. A diagram if the question says "diagram" or if one is standard for the topic. Use a SIMPLIFIED, easy-to-draw
   version (keep the textbook's labels exactly; the student must be able to draw it in 2–3 minutes).
3. Numbered points with a **bold keyword** + one line each. Use a compact table where a comparison or list is
   asked (e.g. metrics, types).
4. Advantages/disadvantages, example or conclusion if the question asks for it.
5. Length: about 180–320 words plus the diagram. It should fit in about one printed page. Complete, but no padding.
After the answer, optionally ONE short `.tip` box (how to score full marks / what not to forget) or `.mem` box
(memory trick) — not more.

## Markup (copy exactly)
```html
<section class="chapter unit-U" id="qaU">
<header class="opener">
  <span class="tag">Unit U · Most likely 5-mark questions</span>
  <h1 id="qaU-top">Unit U: N questions you must prepare</h1>
  <p class="sub">CO-U · topics covered …</p>
  <div class="meta">
    <div><b>Questions</b>N model answers + backups</div>
    <div><b>From</b>Study guide Chapters …</div>
    <div><b>Time per answer</b>About 10 minutes in the exam</div>
  </div>
  <div class="learn"><h4>Questions at a glance</h4><ol class="glance"><li>short title of Q1</li>…</ol></div>
</header>

<h2 class="qa-h" id="qaU-1"><span class="num">Q1</span> Full question text exactly as it would be printed?</h2>
<div class="qa-tags"><span class="t-marks">5 marks</span><span class="t-co">CO1</span><span class="t-bloom">L2</span>
  <span class="t-pyq">Asked in CIE-1 2024</span><span class="t-vlike">Very likely</span></div>
<div class="qa-split">Definition 1 + Diagram 2 + Explanation 2</div>
<div class="ans-label">Model answer</div>
… answer …
<div class="tip"><p>…</p></div>

<h2 class="qa-h" id="qaU-2"> … </h2>
…
<section class="qbank backup">
  <h2 id="qaU-backup">Backup questions (prepare if you have time)</h2>
  <div class="q"><span class="marks">5M</span><div class="qt">Question</div><div class="hint">3–5 line answer outline: key points, diagram to draw, where to revise in the study guide (chapter.section).</div></div>
  …
</section>
</section>
```
- Tags: `t-pyq` only for questions asked in the 2024 paper. Likelihood: `t-vlike` "Very likely" or `t-like` "Likely".
- Bloom level: L1 (list/define) or L2 (explain/describe) as appropriate.
- Every h2 must have an id `qaU-k`. No other h2s except the backup heading.

## Check visually (required)
`cd BOOK && python3 build.py --only qaU` → look at every sheet in BOOK/preview/qaU/ with the Read tool. Fix overflow,
clipped text, diagrams too small/large, awkward page breaks (a diagram pushed to the next page leaving a big gap —
reorder or shrink). Then report back briefly: page count, question list, anything uncertain. Work quickly — the
student is studying now. Never mention AI or this brief in the booklet.
