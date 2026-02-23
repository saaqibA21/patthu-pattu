import json
d = json.load(open('knowledge_base_ocr.json', encoding='utf-8'))
pages = d['pages']
has_content = [p for p in pages if p['char_count'] > 50]
print(f'Total pages extracted: {len(pages)}')
print(f'Pages with content: {len(has_content)}')
print(f'Total chars: {sum(p["char_count"] for p in pages):,}')
print(f'Sample (page {has_content[0]["page"]}):')
print(has_content[0]['content'][:300])
