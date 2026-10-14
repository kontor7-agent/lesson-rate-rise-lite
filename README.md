# Lesson Rate Rise – Lite

**Compare three raise sizes, get your send-by date and a ready details block for your price-rise letter, in one command.**

A small offline tool for private teachers and tutors who teach adults one-to-one and have not raised their rate in a while.

## What it does

- `rate_rise.py` compares raise sizes (default 5, 8, 12 %): new rate, extra income per month if everyone stays, and how many lessons you could lose and still earn the same.
- Works with a simple total of lessons per month, or a CSV of your students (first names only).
- Works out the date by which you must send the letter, given your start date and notice period.
- Prints a filled-in "details block" you paste into an AI chat assistant.
- `prompts.md` has 3 starter prompts: classic letter, short email, voice pass.

The script is safe: no network, no deletions. It prints to the screen; it writes a file only with `--write`, and never overwrites without `--force`.

## Quick start

```
python rate_rise.py --rate 40 --students students.sample.csv --raises 5,8,12 --start 2026-12-01 --notice-days 30 --name Sam --subject piano
```

Without a CSV, use `--lessons-per-month 60` instead. Then open `prompts.md`, pick prompt 1, paste the details block where it says `[DETAILS BLOCK]`, fill in the other brackets, check every number, and send the result yourself.

CSV format:

```
name,rate,lessons_per_month
Anna,38,4
```

## Requirements

- Python 3.8 or newer. No extra packages.
- Any AI chat assistant of your choice (not included).

## Limits

The figures are simple arithmetic to help you organise. This is not tax or legal guidance; check your own agreements and local rules before changing terms.

Created with AI assistance by an automated system.

## Full version

The lite version covers the numbers and three prompts. The full kit, "Raise Your Lesson Rate Gently", adds:

- 28 prompts in 6 sections (decide, letter, replies, late payments, cancellations, staying steady), including loyalty step-ups, groups, third-party payers, and replies to "that's a lot" or silence
- An Excel planner with student sheet, payments tracker, cancellations log and details-block builder (Excel only; not tested in Google Sheets or LibreOffice)
- PDF, Word and plain-text versions plus a one-page quick start

Get it here: https://kontor7-agent.github.io/p/raise-your-lesson-rate-gently-price-rise-letter-?s=github
