# %% [markdown]
# # Additional Exercise 3: Transaction History Analyzer

# %% Student-specific inputs
from collections import Counter

LAST_NAME = input("Enter LAST_NAME: ").strip().upper()
SEED_NUM = int(input("Enter SEED_NUM (integer): "))
FAVORITE_ARTIST = input("Enter FAVORITE_ARTIST: ").strip()

LETTERS = [c for c in FAVORITE_ARTIST.upper() if c.isalpha()]
CUSTOMERS = [f"{LAST_NAME}_C{n}" for n in range(1, 6)]
PRICES = {"NOTEBOOK": 45.00, "PEN": 15.00, "USB": 250.00,
          "HEADPHONES": 800.00, "CALCULATOR": 350.00}   # fixed prices (PHP)
PRODUCTS = list(PRICES)


def gen_qty(i):
    """Quantity (1-9) from SEED_NUM and the character position/code of FAVORITE_ARTIST."""
    ch = LETTERS[i % len(LETTERS)]
    return (SEED_NUM * (i + 1) + ord(ch) * (i + 1)) % 9 + 1


def line(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# %% 1. Generated Transaction Records
NUM_TX = 12
records = []
for i in range(NUM_TX):
    records.append({"customer": CUSTOMERS[i % 5],
                    "product": PRODUCTS[(i + i // 5 + SEED_NUM) % 5],
                    "qty": gen_qty(i)})
# Required repeated customer-product purchase (same pair as transaction 1)
records.append({"customer": records[0]["customer"], "product": records[0]["product"],
                "qty": gen_qty(NUM_TX)})
for n, r in enumerate(records, 1):
    r["id"] = n
    r["price"] = PRICES[r["product"]]
    r["value"] = r["qty"] * r["price"]     # transaction value

line("1. GENERATED TRANSACTION RECORDS")
print(f"LAST_NAME={LAST_NAME} | SEED_NUM={SEED_NUM} | FAVORITE_ARTIST={FAVORITE_ARTIST}")
print("Fixed prices:", PRICES)
print(f"{'ID':<4}{'CUSTOMER':<14}{'PRODUCT':<12}{'QTY':>4}{'PRICE':>10}")
for r in records:
    print(f"{r['id']:<4}{r['customer']:<14}{r['product']:<12}{r['qty']:>4}{r['price']:>10.2f}")

# %% 2. Organized Transaction Data
organized = {c: {} for c in CUSTOMERS}
for r in records:
    organized[r["customer"]].setdefault(r["product"], []).append((r["qty"], r["value"]))

line("2. ORGANIZED TRANSACTION DATA (customer -> product -> [(qty, value)])")
for c in CUSTOMERS:
    print(f"{c}:")
    for p, tx in organized[c].items():
        print(f"   {p:<12} {[(q, f'{v:.2f}') for q, v in tx]}")

# %% 3. Repeated / Distinct Transactions
pair_counts = Counter((r["customer"], r["product"]) for r in records)
repeated = {p: n for p, n in pair_counts.items() if n > 1}

line("3. REPEATED / DISTINCT TRANSACTIONS")
for (c, p), n in repeated.items():
    q = sum(x[0] for x in organized[c][p])
    print(f"Repeated purchase: {c} bought {p} {n} times (total qty {q})")
print(f"Distinct customers : {len({r['customer'] for r in records})} -> {sorted({r['customer'] for r in records})}")
print(f"Distinct products  : {len({r['product'] for r in records})} -> {sorted({r['product'] for r in records})}")
print(f"Distinct customer-product pairs: {len(pair_counts)} of {len(records)} transactions")

# %% 4. Transaction Values
grand_total = sum(r["value"] for r in records)
line("4. TRANSACTION VALUES")
print(f"{'ID':<4}{'CUSTOMER':<14}{'PRODUCT':<12}{'QTY x PRICE':<18}{'VALUE':>10}")
for r in records:
    print(f"{r['id']:<4}{r['customer']:<14}{r['product']:<12}{str(r['qty'])+' x '+format(r['price'],'.2f'):<18}{r['value']:>10.2f}")
print(f"{'OVERALL DATASET VALUE':<48}{grand_total:>10.2f}")

# %% 5. Customer Summaries
cust = {c: {"tx": 0, "units": 0, "value": 0.0, "products": set()} for c in CUSTOMERS}
for r in records:
    s = cust[r["customer"]]
    s["tx"] += 1; s["units"] += r["qty"]; s["value"] += r["value"]; s["products"].add(r["product"])

line("5. CUSTOMER SUMMARIES")
print(f"{'CUSTOMER':<14}{'TX':>3}{'UNITS':>6}{'DISTINCT':>9}{'TOTAL':>11}{'AVG/TX':>10}")
for c, s in cust.items():
    avg = s["value"] / s["tx"] if s["tx"] else 0
    print(f"{c:<14}{s['tx']:>3}{s['units']:>6}{len(s['products']):>9}{s['value']:>11.2f}{avg:>10.2f}")

# %% 6. Product Summaries
prod = {p: {"tx": 0, "units": 0, "value": 0.0, "buyers": set()} for p in PRODUCTS}
for r in records:
    s = prod[r["product"]]
    s["tx"] += 1; s["units"] += r["qty"]; s["value"] += r["value"]; s["buyers"].add(r["customer"])

line("6. PRODUCT SUMMARIES")
print(f"{'PRODUCT':<12}{'PRICE':>9}{'TX':>3}{'UNITS':>6}{'BUYERS':>7}{'REVENUE':>11}{'SHARE':>8}")
for p, s in prod.items():
    print(f"{p:<12}{PRICES[p]:>9.2f}{s['tx']:>3}{s['units']:>6}{len(s['buyers']):>7}"
          f"{s['value']:>11.2f}{s['value']/grand_total*100:>7.1f}%")

# %% 7. Ordered Results
line("7. ORDERED RESULTS")
print("Customers by total spending (highest first):")
for rank, (c, s) in enumerate(sorted(cust.items(), key=lambda x: -x[1]["value"]), 1):
    print(f"   {rank}. {c:<14}{s['value']:>10.2f}")
print("Products by revenue (highest first):")
for rank, (p, s) in enumerate(sorted(prod.items(), key=lambda x: -x[1]["value"]), 1):
    print(f"   {rank}. {p:<12}{s['value']:>10.2f}  ({s['units']} units)")
print("Products by units sold (highest first):")
for rank, (p, s) in enumerate(sorted(prod.items(), key=lambda x: -x[1]["units"]), 1):
    print(f"   {rank}. {p:<12}{s['units']:>4}")
print("Transactions by value (highest first):")
for r in sorted(records, key=lambda r: (-r["value"], r["id"])):
    print(f"   #{r['id']:<3}{r['customer']:<14}{r['product']:<12}{r['value']:>10.2f}")

# %% 8. Overall Transaction Summary
top_c = max(cust, key=lambda c: cust[c]["value"])
top_p = max(prod, key=lambda p: prod[p]["value"])
big = max(records, key=lambda r: r["value"])
line("8. OVERALL TRANSACTION SUMMARY - FINAL CONSOLIDATED TRANSACTION REPORT")
print(f"Total transactions   : {len(records)}")
print(f"Total units sold     : {sum(r['qty'] for r in records)}")
print(f"Total transaction value: {grand_total:.2f}")
print(f"Average per transaction: {grand_total/len(records):.2f}")
print(f"Top customer         : {top_c} ({cust[top_c]['value']:.2f})")
print(f"Top product (revenue): {top_p} ({prod[top_p]['value']:.2f})")
print(f"Largest transaction  : #{big['id']} {big['customer']} - {big['product']} ({big['value']:.2f})")
print(f"Repeated purchases   : {len(repeated)} -> {list(repeated)}")