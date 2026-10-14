#!/usr/bin/env python3
"""rate_rise.py - compare lesson-rate raises and build a ready-to-paste details block.

Offline, standard library only. Prints to the screen by default.
Writes a file only if you pass --write PATH (and never overwrites without --force).

Examples:
  python rate_rise.py --rate 40 --lessons-per-month 60 --start 2026-12-01
  python rate_rise.py --rate 40 --students students.sample.csv --raises 5,8,12 --name Sam --subject piano
"""
import argparse
import csv
import datetime as dt
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Compare rate-rise options for one-to-one lessons.")
    p.add_argument("--rate", type=float, required=True, help="current rate per lesson")
    p.add_argument("--raises", default="5,8,12", help="comma list of percentages (default 5,8,12)")
    p.add_argument("--lessons-per-month", type=float, default=0, help="total lessons you teach per month")
    p.add_argument("--students", help="optional CSV with columns: name,rate,lessons_per_month")
    p.add_argument("--start", help="date the new rate starts, YYYY-MM-DD")
    p.add_argument("--notice-days", type=int, default=30, help="days of notice (default 30)")
    p.add_argument("--name", default="[your first name]")
    p.add_argument("--subject", default="[subject]")
    p.add_argument("--currency", default="", help="symbol to print, e.g. EUR")
    p.add_argument("--write", help="save the report to this file (dry-run/print if omitted)")
    p.add_argument("--force", action="store_true", help="allow overwriting the --write file")
    return p.parse_args()


def load_students(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            try:
                rows.append((r["name"].strip(), float(r["rate"]), float(r["lessons_per_month"])))
            except (KeyError, ValueError, AttributeError):
                sys.exit("CSV needs columns name,rate,lessons_per_month with numbers in the last two.")
    return rows


def main():
    a = parse_args()
    cur = a.currency
    try:
        pcts = [float(x) for x in a.raises.split(",") if x.strip()]
    except ValueError:
        sys.exit("--raises must be numbers like 5,8,12")
    if a.rate <= 0 or not pcts or any(x <= 0 for x in pcts):
        sys.exit("Rate and percentages must be positive.")

    students = load_students(a.students) if a.students else []
    total_lessons = sum(s[2] for s in students) if students else a.lessons_per_month

    out = []
    out.append("RATE-RISE COMPARISON (simple arithmetic, check it yourself)")
    out.append(f"Current rate: {a.rate:.2f} {cur}".rstrip())
    out.append(f"Lessons per month: {total_lessons:g}")
    out.append("")
    out.append(f"{'Raise':>6} {'New rate':>9} {'Extra/month':>12} {'Can lose*':>10}")
    for p in pcts:
        new = round(a.rate * (1 + p / 100), 2)
        if students:
            extra = sum(round(s[1] * (1 + p / 100), 2) * s[2] - s[1] * s[2] for s in students)
        else:
            extra = (new - a.rate) * total_lessons
        lose = p / (100 + p) * 100
        out.append(f"{p:>5g}% {new:>9.2f} {extra:>12.2f} {lose:>9.1f}%")
    out.append("* share of lessons you could lose and still earn the same as today")

    start = None
    if a.start:
        try:
            start = dt.date.fromisoformat(a.start)
        except ValueError:
            sys.exit("--start must look like 2026-12-01")
        send_by = start - dt.timedelta(days=a.notice_days)
        out.append("")
        out.append(f"TIMELINE: new rate starts {start}; send the letter by {send_by} "
                   f"({a.notice_days} days of notice).")
        if send_by < dt.date.today():
            out.append("Note: that send-by date has already passed. Move the start date later.")

    out.append("")
    out.append("DETAILS BLOCK (paste into a prompt from prompts.md)")
    out.append("ABOUT ME")
    out.append(f"- First name: {a.name}")
    out.append(f"- I teach: {a.subject}, one-to-one, mostly adult learners")
    out.append(f"- Current rate: {a.rate:.2f} per lesson")
    out.append(f"- New rate: [pick one from the table] per lesson, starting {start or '[date]'}")
    out.append(f"- Notice I am giving: {a.notice_days} days")
    out.append("- My tone: warm, clear, no grovelling.")
    text = "\n".join(out) + "\n"

    if not a.write:
        print(text)
        print("(Dry run: nothing saved. Add --write report.txt to save.)")
        return
    if os.path.exists(a.write) and not a.force:
        sys.exit(f"{a.write} exists. Use --force to overwrite.")
    with open(a.write, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to {a.write}")


if __name__ == "__main__":
    main()
