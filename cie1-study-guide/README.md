# SE&M (CS51) — CIE-1 Study Guide

Unit-wise study guide for the CIE-1 portion of Software Engineering and Modelling:
Unit 1, Unit 2, and Unit 3 up to architectural views.

| File | Contents |
|---|---|
| `SEM_CIE1_Complete_Guide.pdf` | All three units in one book (140 pages) |
| `SEM_CIE1_Unit1.pdf` | Unit 1: Introduction, Software Processes, Agile |
| `SEM_CIE1_Unit2.pdf` | Unit 2: Requirements Engineering, Design Concepts |
| `SEM_CIE1_Unit3.pdf` | Unit 3 (CIE-1 part): Architectural design decisions and views |

Sources: lecture slides, Sommerville *Software Engineering* (10th ed), Pressman *Software Engineering: A Practitioner's Approach*.

## Rebuilding

`source/` holds one HTML fragment per chapter plus the stylesheet and build scripts (Chromium via Playwright, pypdf, poppler-utils).

```sh
cd source
python3 build.py --only ch2   # preview one chapter
python3 gen_back.py           # refresh diagram checklist and cover counts
python3 make_book.py          # build the complete guide and the three unit PDFs into out/
```
