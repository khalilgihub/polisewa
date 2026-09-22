import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('final_report.html', 'r', encoding='utf-8') as f:
    html = f.read()

ref_block = re.search(r'<!-- REFERENCES -->.*', html, re.DOTALL)
if ref_block:
    items = re.findall(r'<li class="ref-item">(.*?)</li>', ref_block.group(0), re.DOTALL)
    for i, it in enumerate(items):
        clean = re.sub(r'<[^>]+>', ' ', it).strip()
        clean = re.sub(r'\s+', ' ', clean)
        print(f"[{i+1}] {clean}")
