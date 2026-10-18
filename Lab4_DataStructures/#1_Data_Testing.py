_# %% [markdown]
# # Additional Exercise 1: Engineering Test Data Organizer

# %% Student-specific inputs
from collections import Counter

LAST_NAME = input("Enter LAST_NAME: ").strip().upper()
SEED_NUM = int(input("Enter SEED_NUM (integer): "))
FAVORITE_ARTIST = input("Enter FAVORITE_ARTIST: ").strip()

LETTERS = [c for c in FAVORITE_ARTIST.upper() if c.isalpha()]
SOURCES = [f"{LAST_NAME}_T{n}" for n in range(1, 6)]
CATEGORIES = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]
UNITS = {"TEMPERATURE": "C", "VOLTAGE": "V", "CURRENT": "A", "PRESSURE": "kPa", "SPEED": "rpm"}


def gen_value(i):
    """Value from SEED_NUM and the character position/code of FAVORITE_ARTIST (10-99)."""
    ch = LETTERS[i % len(LETTERS)]
    return (SEED_NUM * (i + 1) + ord(ch) * (i + 1)) % 90 + 10


def line(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# %% 1. Generated Test Data
NUM_RECORDS = 12
records = []
for i in range(NUM_RECORDS):
    # (source, category) pairs stay unique for i < 25
    records.append({
        "id": i + 1,
        "source": SOURCES[i % 5],
        "category": CATEGORIES[(i + i // 5 + SEED_NUM) % 5],
        "value": gen_value(i),
    })
# Required repeated source/category record (same pair as record 1, new reading)
records.append({"id": NUM_RECORDS + 1, "source": records[0]["source"],
                "category": records[0]["category"], "value": gen_value(NUM_RECORDS)})

line("1. GENERATED TEST DATA")
print(f"LAST_NAME={LAST_NAME} | SEED_NUM={SEED_NUM} | FAVORITE_ARTIST={FAVORITE_ARTIST}")
print(f"{'ID':<4}{'SOURCE':<16}{'CATEGORY':<14}{'VALUE':>7}  UNIT")
for r in records:
    print(f"{r['id']:<4}{r['source']:<16}{r['category']:<14}{r['value']:>7}  {UNITS[r['category']]}")

# %% 2. Organized Test Data
organized = {s: {} for s in SOURCES}
for r in records:
    organized[r["source"]].setdefault(r["category"], []).append(r["value"])

line("2. ORGANIZED TEST DATA (source -> category -> values)")
for s in SOURCES:
    print(f"{s}:")
    if not organized[s]:
        print("   (no records)")
    for c, vals in organized[s].items():
        print(f"   {c:<12} {vals}")

# %% 3. Repeated / Distinct Data
pair_counts = Counter((r["source"], r["category"]) for r in records)
repeated = {p: n for p, n in pair_counts.items() if n > 1}
distinct_pairs = [p for p, n in pair_counts.items() if n == 1]
cat_counts = Counter(r["category"] for r in records)
multi_cats = [c for c, n in cat_counts.items() if n > 1]

line("3. REPEATED / DISTINCT DATA")
print("Repeated source/category records:")
for (s, c), n in repeated.items():
    vals = organized[s][c]
    print(f"   {s} / {c}: {n} entries -> {vals}")
print(f"Distinct source/category pairs : {len(pair_counts)} ({len(distinct_pairs)} appear once)")
print(f"Distinct sources used          : {sorted({r['source'] for r in records})}")
print(f"Distinct categories used       : {sorted(cat_counts)}")
print(f"Distinct measurement values    : {len({r['value'] for r in records})} of {len(records)}")
print(f"Categories with multiple readings: {multi_cats}")

# %% 4. Numerical and Categorical Summaries
def stats(vals):
    return {"n": len(vals), "min": min(vals), "max": max(vals),
            "mean": sum(vals) / len(vals), "total": sum(vals)}


by_cat, by_src = {}, {}
for r in records:
    by_cat.setdefault(r["category"], []).append(r["value"])
    by_src.setdefault(r["source"], []).append(r["value"])
cat_stats = {c: stats(v) for c, v in by_cat.items()}
src_stats = {s: stats(v) for s, v in by_src.items()}

line("4. NUMERICAL AND CATEGORICAL SUMMARIES")
print("By category:")
print(f"{'CATEGORY':<14}{'N':>3}{'MIN':>6}{'MAX':>6}{'MEAN':>8}{'TOTAL':>7}")
for c, st in cat_stats.items():
    print(f"{c:<14}{st['n']:>3}{st['min']:>6}{st['max']:>6}{st['mean']:>8.2f}{st['total']:>7}")
print("\nBy source:")
print(f"{'SOURCE':<16}{'N':>3}{'MIN':>6}{'MAX':>6}{'MEAN':>8}{'TOTAL':>7}")
for s, st in src_stats.items():
    print(f"{s:<16}{st['n']:>3}{st['min']:>6}{st['max']:>6}{st['mean']:>8.2f}{st['total']:>7}")
print("\nCategorical counts:", dict(cat_counts))
print("Most frequent category:", cat_counts.most_common(1)[0])
all_vals = [r["value"] for r in records]
print(f"Overall: n={len(all_vals)}, min={min(all_vals)}, max={max(all_vals)}, "
      f"mean={sum(all_vals)/len(all_vals):.2f}")

# %% 5. Processed Results
line("5. PROCESSED RESULTS")
print("Average of repeated source/category readings:")
for (s, c) in repeated:
    v = organized[s][c]
    print(f"   {s} / {c}: values {v} -> mean {sum(v)/len(v):.2f}, spread {max(v)-min(v)}")
print("\nSource x Category mean matrix:")
print(f"{'':<16}" + "".join(f"{c[:6]:>9}" for c in CATEGORIES))
for s in SOURCES:
    row = ""
    for c in CATEGORIES:
        v = organized[s].get(c)
        row += f"{sum(v)/len(v):>9.1f}" if v else f"{'-':>9}"
    print(f"{s:<16}{row}")

# %% 6. Ordered Results
line("6. ORDERED RESULTS")
print("Categories by mean value (highest first):")
for rank, (c, st) in enumerate(sorted(cat_stats.items(), key=lambda x: -x[1]["mean"]), 1):
    print(f"   {rank}. {c:<12} mean={st['mean']:.2f}")
print("Sources by mean value (highest first):")
for rank, (s, st) in enumerate(sorted(src_stats.items(), key=lambda x: -x[1]["mean"]), 1):
    print(f"   {rank}. {s:<14} mean={st['mean']:.2f}")
print("Records by value (highest first):")
for r in sorted(records, key=lambda r: (-r["value"], r["id"])):
    print(f"   #{r['id']:<3}{r['source']:<14}{r['category']:<12}{r['value']}")

# %% 7. Final Summary
top_cat = max(cat_stats, key=lambda c: cat_stats[c]["mean"])
low_cat = min(cat_stats, key=lambda c: cat_stats[c]["mean"])
line("7. FINAL SUMMARY - FINAL ORGANIZED AND SUMMARIZED TEST DATASET")
print(f"Records generated      : {len(records)} from {len(src_stats)} sources")
print(f"Categories covered     : {len(cat_stats)} of {len(CATEGORIES)}")
print(f"Repeated records       : {len(repeated)} -> {list(repeated)}")
print(f"Highest mean category  : {top_cat} ({cat_stats[top_cat]['mean']:.2f})")
print(f"Lowest mean category   : {low_cat} ({cat_stats[low_cat]['mean']:.2f})")
print(f"Overall mean value     : {sum(all_vals)/len(all_vals):.2f}")