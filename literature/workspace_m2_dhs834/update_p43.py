import json, hashlib

p = 'literature/workspace_m2_dhs834/blind_read_p0043.json'
with open(p, 'r', encoding='utf-8') as f:
    d = json.load(f)
d['entries'][0]['source_H'] = '[疑:邀/慇/殀]'
d['entries'][1]['source_H'] = '[疑:邀/慇/殀] 君'
content = json.dumps(d, ensure_ascii=False, indent=2).encode('utf-8')
with open(p, 'wb') as f:
    f.write(content)
sha = hashlib.sha256(content).hexdigest()

m_path = 'literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json'
with open(m_path, 'r', encoding='utf-8') as f:
    m = json.load(f)
m['pages']['0043']['blind_first_read_sha256'] = sha
with open(m_path, 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)
print('Updated 0043 SHA-256:', sha)
