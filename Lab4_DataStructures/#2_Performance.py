# %% [markdown]
# # Additional Exercise 2: Student Performance Data Analyzer

# %% Student-specific inputs
from collections import Counter

LAST_NAME = input("Enter LAST_NAME: ").strip().upper()
SEED_NUM = int(input("Enter SEED_NUM (integer): "))
FAVORITE_ARTIST = input("Enter FAVORITE_ARTIST: ").strip()

LETTERS = [c for c in FAVORITE_ARTIST.upper() if c.isalpha()]
STUDENTS = [f"{LAST_NAME}_S{n}" for n in range(1, 6)]
SUBJECTS = ["PROGRAMMING", "MATHEMATICS", "ELECTRONICS", "PHYSICS", "ENGLISH"]


def gen_score(i):
    """Score (50-99) from SEED_NUM and the character position/code of FAVORITE_ARTIST."""
    ch = LETTERS[i % len(LETTERS)]
    return (SEED_NUM * (i + 1) + ord(ch) * (i + 1)) % 50 + 50


def category(score):
    if score >= 90: return "Outstanding"
    if score >= 80: return "Very Good"
    if score >= 70: return "Good"
    if score >= 60: return "Fair"
    return "Needs Improvement"


def line(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# %% 1. Generated Performance Records
records = []
for si, stu in enumerate(STUDENTS):
    for sj, sub in enumerate(SUBJECTS):
        records.append({"student": stu, "subject": sub, "score": gen_score(si * 5 + sj)})
# Incomplete record: one student-subject score is missing
records[7]["score"] = None
# Repeated record: same student-subject appears again (retake with a new score)
records.append({"student": records[0]["student"], "subject": records[0]["subject"],
                "score": gen_score(25)})
for n, r in enumerate(records, 1):
    r["id"] = n

line("1. GENERATED PERFORMANCE RECORDS")
print(f"LAST_NAME={LAST_NAME} | SEED_NUM={SEED_NUM} | FAVORITE_ARTIST={FAVORITE_ARTIST}")
print(f"{'ID':<4}{'STUDENT':<14}{'SUBJECT':<14}{'SCORE':>6}")
for r in records:
    print(f"{r['id']:<4}{r['student']:<14}{r['subject']:<14}{'MISSING' if r['score'] is None else r['score']:>7}")

# %% 2. Organized Student/Subject Data
organized = {s: {} for s in STUDENTS}
for r in records:
    organized[r["student"]].setdefault(r["subject"], []).append(r["score"])

line("2. ORGANIZED STUDENT/SUBJECT DATA")
print(f"{'':<14}" + "".join(f"{s[:7]:>9}" for s in SUBJECTS))
for stu in STUDENTS:
    row = ""
    for sub in SUBJECTS:
        v = organized[stu].get(sub, [])
        row += f"{'/'.join('--' if x is None else str(x) for x in v):>9}"
    print(f"{stu:<14}{row}")
print("(entries with '/' are repeated records; '--' is a missing score)")

# Valid data: ignore missing scores, use the latest score for repeated records
valid = {}
for r in records:
    if r["score"] is not None:
        valid[(r["student"], r["subject"])] = r["score"]

# %% 3. Repeated / Incomplete Records
pair_counts = Counter((r["student"], r["subject"]) for r in records)
repeated = {p: organized[p[0]][p[1]] for p, n in pair_counts.items() if n > 1}
incomplete = [r for r in records if r["score"] is None]

line("3. REPEATED / INCOMPLETE RECORDS")
for (stu, sub), vals in repeated.items():
    print(f"Repeated  : {stu} / {sub} -> scores {vals} (latest score {vals[-1]} used)")
for r in incomplete:
    print(f"Incomplete: record #{r['id']} {r['student']} / {r['subject']} has a missing score (excluded)")
print(f"Valid student-subject scores used: {len(valid)}")

# %% 4. Performance Categories
line("4. PERFORMANCE CATEGORIES")
print(f"{'STUDENT':<14}{'SUBJECT':<14}{'SCORE':>6}  CATEGORY")
for (stu, sub), sc in valid.items():
    print(f"{stu:<14}{sub:<14}{sc:>6}  {category(sc)}")
cat_counts = Counter(category(s) for s in valid.values())
print("\nCategory distribution:", dict(cat_counts))

# %% 5. Student and Subject Summaries
stu_scores = {s: [sc for (st, _), sc in valid.items() if st == s] for s in STUDENTS}
sub_scores = {s: [sc for (_, sb), sc in valid.items() if sb == s] for s in SUBJECTS}


def summarize(d):
    out = {}
    for k, v in d.items():
        if v:
            out[k] = {"n": len(v), "avg": sum(v) / len(v), "hi": max(v), "lo": min(v)}
    return out


stu_sum, sub_sum = summarize(stu_scores), summarize(sub_scores)

line("5. STUDENT AND SUBJECT SUMMARIES")
print(f"{'STUDENT':<14}{'N':>3}{'AVG':>8}{'HIGH':>6}{'LOW':>5}  OVERALL")
for s, st in stu_sum.items():
    print(f"{s:<14}{st['n']:>3}{st['avg']:>8.2f}{st['hi']:>6}{st['lo']:>5}  {category(st['avg'])}")
print(f"\n{'SUBJECT':<14}{'N':>3}{'AVG':>8}{'HIGH':>6}{'LOW':>5}")
for s, st in sub_sum.items():
    print(f"{s:<14}{st['n']:>3}{st['avg']:>8.2f}{st['hi']:>6}{st['lo']:>5}")

# %% 6. Ordered Results
line("6. ORDERED RESULTS")
print("Students ranked by average (highest first):")
for rank, (s, st) in enumerate(sorted(stu_sum.items(), key=lambda x: -x[1]["avg"]), 1):
    print(f"   {rank}. {s:<14}{st['avg']:.2f}")
print("Subjects ranked by average (highest first):")
for rank, (s, st) in enumerate(sorted(sub_sum.items(), key=lambda x: -x[1]["avg"]), 1):
    print(f"   {rank}. {s:<14}{st['avg']:.2f}")
print("All valid scores (highest first):")
for (stu, sub), sc in sorted(valid.items(), key=lambda x: (-x[1], x[0])):
    print(f"   {sc:>3}  {stu:<14}{sub:<14}{category(sc)}")

# %% Final Output
all_sc = list(valid.values())
best = max(stu_sum, key=lambda s: stu_sum[s]["avg"])
weak = min(sub_sum, key=lambda s: sub_sum[s]["avg"])
line("FINAL STUDENT PERFORMANCE REPORT")
print(f"Records generated   : {len(records)} ({len(valid)} valid, "
      f"{len(repeated)} repeated, {len(incomplete)} incomplete)")
print(f"Class average       : {sum(all_sc)/len(all_sc):.2f}")
print(f"Top student         : {best} ({stu_sum[best]['avg']:.2f})")
print(f"Weakest subject     : {weak} ({sub_sum[weak]['avg']:.2f})")
print(f"Category distribution: {dict(cat_counts)}")