import json
d = json.load(open('ocr_test_10pages.json', encoding='utf-8'))
print(f"Total chars: {d['total_chars']}\n")
for p in d['pages']:
    if p['chars'] > 100:
        print(f"=== Page {p['page']} ({p['chars']} chars) ===")
        print(p['content'][:400])
        print()
