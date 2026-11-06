import openpyxl

wb = openpyxl.load_workbook("workflow-fixes/data1.xlsx", data_only=True)
ws = wb["nodejs"]

max_r = ws.max_row
max_c = ws.max_column

print(f"Sheet 'nodejs' max_row: {max_r}, max_column: {max_c}")

# Check headers
headers = [ws.cell(row=1, column=c).value for c in range(1, max_c + 1)]
print(f"Total headers: {len(headers)}")

# Check for empty cells or anomalies
empty_counts = {c: 0 for c in range(1, max_c + 1)}
for r in range(2, max_r + 1):
    for c in range(1, max_c + 1):
        val = ws.cell(row=r, column=c).value
        if val is None or str(val).strip() == "":
            empty_counts[c] += 1

empty_cols = {headers[c-1]: empty_counts[c] for c in range(1, max_c + 1) if empty_counts[c] > 0}
print(f"Columns with empty values: {empty_cols}")

# Analysis for List 1: Purchase Orders / Quotes / Paid / Blocked
po_rows = []
free_rows = []
tool_summary = {}

for r in range(2, max_r + 1):
    tool = ws.cell(row=r, column=1).value
    rec_type = ws.cell(row=r, column=4).value
    paid_status = ws.cell(row=r, column=8).value
    blocked = ws.cell(row=r, column=9).value
    spdx = ws.cell(row=r, column=11).value
    copyleft = ws.cell(row=r, column=12).value
    redist = ws.cell(row=r, column=13).value
    verdict = ws.cell(row=r, column=16).value
    pipe = ws.cell(row=r, column=22).value
    yml = ws.cell(row=r, column=23).value
    req_purchase = ws.cell(row=r, column=29).value
    price_link = ws.cell(row=r, column=36).value
    best_alt = ws.cell(row=r, column=40).value
    evidence = ws.cell(row=r, column=44).value
    
    tool_summary[tool] = tool_summary.get(tool, 0) + 1
    
    # List 1: Purchase Orders, Vendor Quotes, Paid items, or Blocked Upstream infra needing purchase/replacement
    if (str(req_purchase).startswith("Yes") or 
        "paid" in str(paid_status).lower() or 
        str(blocked).startswith("Yes")):
        po_rows.append((r, pipe, yml, tool, rec_type, paid_status, req_purchase, blocked, price_link, best_alt))
    
    # List 2: Free and open-source tools for legal compliance
    if "free" in str(paid_status).lower():
        free_rows.append((r, pipe, yml, tool, rec_type, spdx, copyleft, redist, verdict))

print(f"\n========================================================")
print(f"LIST 1: CANDIDATES FOR PURCHASE ORDERS / VENDOR QUOTES / BLOCKED UPSTREAM INFRA")
print(f"Total matching rows: {len(po_rows)}")
print(f"========================================================")
seen_po_tools = set()
for r, pipe, yml, tool, rec_type, paid_status, req_purchase, blocked, price_link, best_alt in po_rows:
    if tool not in seen_po_tools:
        print(f"Tool: {tool[:35]:35} | Type: {rec_type[:22]:22} | Paid: {paid_status[:25]:25} | Req PO: {req_purchase[:25]:25}")
        seen_po_tools.add(tool)

print(f"\n========================================================")
print(f"LIST 2: FREE & OPEN SOURCE TOOLS FOR LEGAL COMPLIANCE")
print(f"Total matching rows: {len(free_rows)}")
print(f"========================================================")
seen_free_tools = set()
for r, pipe, yml, tool, rec_type, spdx, copyleft, redist, verdict in free_rows:
    if tool not in seen_free_tools:
        print(f"Tool: {tool[:32]:32} | SPDX: {spdx[:20]:20} | Copyleft: {copyleft[:15]:15} | Verdict: {verdict[:15]:15}")
        seen_free_tools.add(tool)

print(f"\n========================================================")
print(f"ALL 21 UNIQUE TOOLS BREAKDOWN (Total: {sum(tool_summary.values())} rows)")
print(f"========================================================")
for t, cnt in sorted(tool_summary.items(), key=lambda x: -x[1]):
    print(f"{t:42}: {cnt:3} rows")
