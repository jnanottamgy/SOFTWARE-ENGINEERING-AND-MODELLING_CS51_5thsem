# SE&M CIE-1 Study Guide — writer's brief

You are writing ONE chapter of a printed A4 study guide (PDF) for a 5th-semester engineering student preparing for
**CIE-1 (Continuous Internal Evaluation 1)** in *Software Engineering and Modelling (CS51)*. The PDF is built from
HTML fragments by `build.py` (Chromium print). You write one fragment file; the build adds the CSS, cover, contents
page, page numbers and PDF bookmarks.

Paths (all absolute):
- BOOK = /tmp/claude-0/-home-user-SOFTWARE-ENGINEERING-AND-MODELLING-CS51-5thsem/db22c00d-e9f6-5b54-9f7d-d9fa28a5c550/scratchpad/book
- Stylesheet (read it once, do not edit it): BOOK/styles.css
- Reference fragment showing every component: BOOK/fragments/sample.html
- Your output: BOOK/fragments/chN.html (N given in your task)
- Sources: TEXT = BOOK/../text (slide text `chX.txt`, textbook text `somm_chX.txt`, `press_*.txt`)
- Slide images: BOOK/../slides/chX/s-NN.png (one PNG per slide; look at the ones with diagrams before redrawing them)
- Textbook PDFs (render a page with `pdftoppm -r 70 -f P -l P -png file.pdf /tmp/...` if you need to see a figure):
  BOOK/../drive/files/sommerville10.pdf, BOOK/../drive/files/pressman7.pdf

## The reader
- Knows **nothing** about software engineering and is starting today. Explain every term the first time it appears.
- Needs to **score in the exam**: answers must use the textbook's own terms and structure.
- Wants it **easy to study and finish**: short paragraphs, lists, tables, diagrams, clear priorities. No padding.

## Content rules (most important)
1. **Nothing from the slides may be missing.** The slides are the teacher's notes: every bullet on every slide in your
   range must appear somewhere in your chapter (rephrased simply is fine; facts, lists and terms must be intact).
   Then add the textbook detail the slides compress, so each point is actually understandable.
2. **Stay inside the syllabus scope given in your task.** Anything outside it is either omitted or (only where your
   task says so) put in a clearly labelled low-priority section.
3. **Accuracy**: facts, lists and definitions come from the sources. Analogies and everyday examples may come from
   you. Do not invent textbook claims, figure numbers, statistics or quotes.
4. For each concept follow this rhythm where it fits: **plain-English idea → exam-ready definition/points →
   example (prefer the textbook case studies: insulin pump, Mentcare, wilderness weather station, iLearn) → diagram
   if it helps → exam tip / watch-out if useful.**
5. Lists that the exam asks for verbatim (e.g. "essential attributes of good software", "principles of agile
   methods", "types of non-functional requirements") must be given **complete and in exam wording**, ideally as a
   table or numbered list, plus a memory trick if one genuinely helps.
6. Every **h2** and every important **h3** gets a priority badge:
   `<span class="prio p3">Must know</span>`, `<span class="prio p2">Important</span>`, `<span class="prio p1">Read once</span>`.
   Be honest: definitions, models, diagrams and comparison questions are usually p3.

## Structure of your fragment (copy the skeleton exactly)
```html
<section class="chapter unit-U" id="chN">
<header class="opener">
  <span class="tag">Unit U · Chapter N</span>
  <h1 id="chN-top">Chapter title</h1>
  <p class="sub">Topic · Topic · Topic</p>
  <div class="meta">
    <div><b>Study time</b>About X hours</div>
    <div><b>Sources</b>Your slides (Ch X) + Sommerville Ch X</div>
    <div><b>Exam weight</b>One line on how heavily this is examined</div>
  </div>
  <div class="learn"><h4>After this chapter you can</h4><ul><li>…</li></ul></div>
</header>

<h2 id="chN-1"><span class="num">N.1</span> Section title <span class="prio p3">Must know</span></h2>
… content, h3 subsections …
<h2 id="chN-2"><span class="num">N.2</span> …</h2>
…
<section class="recap"><div class="recap-box">
  <h2 id="chN-recap">Chapter N in one page</h2>
  … a dense one-page revision sheet: key definitions, lists, diagrams to practise, comparisons (use .cols-2) …
</div></section>

<section class="qbank">
  <h2 id="chN-q">Likely exam questions</h2>
  <div class="q"><span class="marks">10M</span><div class="qt">Question…</div><div class="hint">What to write, in order; which figure to draw; which section to revise.</div></div>
  … 10–16 questions: a mix of 2M definitions, 4–6M explain/differentiate, 8–10M explain-with-diagram / apply-to-a-case-study …
</section>
</section>
```
- `U` = unit number (1, 2 or 3). It sets the colour theme automatically.
- Only `h1` and `h2` with an `id` go into the contents page. Use h3/h4 for everything below section level.
- h2 ids: `chN-1`, `chN-2`, … ; recap `chN-recap`; questions `chN-q`. Section numbers `N.1`, `N.2`, … in `<span class="num">`.
- Figures are numbered `Fig N.1`, `Fig N.2`, … in your chapter; cite the source at the end of the caption:
  `<span class="src">Sommerville Fig 2.1</span>` / `<span class="src">Your slides, slide 8</span>` / `<span class="src">Drawn for this guide</span>`.

## Components (all defined in styles.css — see sample.html)
| Use | Markup |
|---|---|
| Must-remember fact | `<div class="key"><p>…</p></div>` |
| Definition to learn word for word | `<div class="def"><p><span class="term">Term</span> — definition.</p></div>` |
| How to write it in the exam / what examiners want | `<div class="tip"><p>…</p></div>` |
| Plain-English explanation or analogy | `<div class="simple"><p>…</p></div>` |
| Worked example / case study | `<div class="eg"><p>…</p></div>` |
| Common confusion / mistake | `<div class="warn"><p>…</p></div>` |
| Mnemonic | `<div class="mem"><p>…</p></div>` |
| Self-test with answer | `<div class="check"><p>Question?<span class="ans">Answer.</span></p></div>` |
| Custom label on any box | add `data-title="Your label"` to the div |
| Highlighter on a key phrase | `<mark>…</mark>` — sparingly, 1–3 per section |
| Coloured keyword | `<span class="kw">…</span>` |
| Advantages / disadvantages | `<div class="proscons"><div class="pros"><h4>Advantages</h4><ul>…</ul></div><div class="cons"><h4>Disadvantages</h4><ul>…</ul></div></div>` |
| Numbered process steps | `<ol class="steps"><li><b>Step</b> — …</li></ol>` |
| Comparison table | `<table><thead><tr><th>…</th></tr></thead><tbody><tr><td class="rowhead">…</td><td>…</td></tr></tbody></table>` |
| Side-by-side | `<div class="cols-2">…</div>` / `cols-3`; `<div class="card">` or `<div class="card tinted">` for small panels |
| Term list | `<dl class="terms"><dt>Term</dt><dd>Meaning</dd></dl>` |
| Force a page break (rarely) | `<div class="pagebreak"></div>` |

Use boxes with purpose: roughly one or two per page on average, never three in a row. Body text, lists and
tables carry most of the content. Escape `&` as `&amp;`, `<` as `&lt;`.

## Diagrams (inline SVG only — no images, no external files, no scripts)
Wrap every diagram:
```html
<figure class="fig"><div class="canvas">
<svg viewBox="0 0 W H" width="W" xmlns="http://www.w3.org/2000/svg"> … </svg>
</div><figcaption><b>Fig N.k</b> Caption. <span class="src">Source</span></figcaption></figure>
```
- Draw at **1:1 scale**: `width` = viewBox width, **max 640**. Height as needed (keep under ~520 so it fits a page).
- Text: font-size **11–13** (never below 10.5), `text-anchor="middle"` inside boxes. SVG does not wrap — split long
  labels into 2–3 `<text>` lines yourself. Width budget: ~**7.3 px per character** at 12.5 px semibold,
  ~6.6 px at 12 px regular. Leave ≥ 10 px padding between text and the box edge.
- **All ids inside SVGs must be prefixed with your chapter**, e.g. `<marker id="chN-arr">`; a second figure can reuse
  the same id only if you define it again identically — safer: `chN-arr2`, etc.
- Palette (fill / stroke):
  indigo `#eef0ff`/`#4f46e5` · teal `#e5f6f3`/`#0d9488` · amber `#fff3e0`/`#d97706` · green `#e8f8ee`/`#16a34a` ·
  rose `#fdeeee`/`#dc2626` · violet `#f4efff`/`#7c3aed` · slate `#f2f5f9`/`#64748b` · white `#ffffff`/`#94a3b8`.
  Text `#1b1f2a`, secondary text `#6b7385`, arrows `#475569` (width 1.6), dashed feedback `#94a3b8` (dasharray "4 3").
  Boxes: `rx="9"`, stroke-width 1.5. Prefer your unit's colour for the main boxes (Unit 1 indigo, Unit 2 teal,
  Unit 3 amber) and other colours to distinguish categories.
- Arrowhead: `<marker id="chN-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker>`
- Redraw **every diagram an exam might ask you to draw** (all process/model/flow diagrams in the slides and textbook
  sections in scope) and add your own explanatory diagrams where a beginner would benefit (e.g. a visual comparison,
  a timeline, a classification tree). Keep the textbook's labels on redrawn figures so the student can reproduce them.

## Check your work visually (required)
```
cd BOOK && python3 build.py --only chN
```
This writes `preview/chN.pdf` and `preview/chN/sheet-01.png`, `sheet-02.png`, … (two pages per sheet). Look at **every**
sheet with the Read tool. Fix: text overflowing SVG boxes, overlapping lines/arrows, unreadably small diagrams,
tables too wide, huge blank gaps caused by a big unbreakable block (split it or move it), headings stranded at a
page bottom, boxes that look cluttered. Re-run until every page looks clean and professional.

Finally do a **coverage pass**: walk through your slide text file slide by slide and confirm each bullet is covered;
fix any gaps.

## Your final reply (short)
Page count; one line per section; list of figures; anything from the slides or textbook you deliberately left out
and why; anything you were unsure about. Do not paste the HTML.

Never mention AI, Claude, prompts or "this brief" inside the guide.
