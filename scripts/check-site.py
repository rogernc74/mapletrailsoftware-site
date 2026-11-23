"""Validate static routes, fragments, local images, metadata and release statements."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import json,re,sys
from hashlib import sha256
root=Path(__file__).resolve().parents[1]
files=sorted(root.rglob('*.html'));errors=[];links=0;images=0
for p in files:
 s=BeautifulSoup(p.read_text(),'html.parser')
 for label,count in [('h1',len(s.find_all('h1'))),('main',len(s.find_all('main')))]:
  if count!=1:errors.append(f'{p.relative_to(root)}: {label} count {count}')
 if not s.find('title') or not s.select_one('meta[name="description"]'):errors.append(f'{p}: missing SEO')
 for t in s.select('[href],[src]'):
  value=t.get('href') or t.get('src');url=urlsplit(value)
  if url.scheme or url.netloc:continue
  links+=1;target=root/unquote(url.path.lstrip('/')) if url.path.startswith('/') else p.parent/unquote(url.path)
  if not url.path:target=p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(root)}: missing {value}');continue
  if url.fragment and target.suffix=='.html':
   dest=BeautifulSoup(target.read_text(),'html.parser')
   if not dest.find(id=unquote(url.fragment)):errors.append(f'{p.relative_to(root)}: missing fragment {value}')
 for im in s.find_all('img'):
  images+=1
  if not im.has_attr('alt'):errors.append(f'{p}: missing image alt')
  if not im.get('width') or not im.get('height'):errors.append(f'{p}: image dimensions {im.get("src")}')
 if re.search(r'coming soon|will carry over to Mac|Apple-first',s.get_text(),re.I):errors.append(f'{p}: obsolete positioning/release copy')
 for m in s.select('meta[content]'):
  if re.search(r'coming soon|Apple-first',m['content'],re.I):errors.append(f'{p}: stale metadata')
# Preserve legal/support text, allowing only Roger’s company-name correction.
import subprocess
legal=[]
launch_disclosures={
 'acadie/privacy/index.html': '9b3d4e7d2142e3af83606ac58628b39407c990ab44ad015ba521ad625f649bfb',
 'acadie/fr-CA/privacy/index.html': 'dfa780c5ad9015c4f40820fd14c8f59203c23ae52ac9983da372c4ccde1183b6',
 'acadie/terms/index.html': 'ca69e5f57aeb7fcd611b8044978e6ff2fcd05b855a35ce8f7328245295c76e2b',
 'acadie/fr-CA/terms/index.html': '2fbffe8123bbc5c7085ce99a968016d44b68709992471c0ff464cd69f5bd43fc',
}
for p in files:
 rel=p.relative_to(root).as_posix()
 # Protect actual legal/support routes. Nesting alone also matches new product
 # pages, which have no historical legal body in the pre-redesign baseline.
 if any(part in {'privacy','support','terms','account-deletion'} for part in p.relative_to(root).parts[:-1]):
  # PR13 deliberately updated these published privacy disclosures. Preserve
  # their approved current bodies; retain the original baseline everywhere else.
  if rel in launch_disclosures:
   new=BeautifulSoup(p.read_text(),'html.parser')
   if sha256(new.main.get_text(' ',strip=True).encode()).hexdigest()!=launch_disclosures[rel]:errors.append(rel+': reviewed legal text changed')
   legal.append(rel)
   continue
  baseline='b8eb850'
  old=BeautifulSoup(subprocess.check_output(['git','show',baseline+':'+rel]),'html.parser')
  new=BeautifulSoup(p.read_text(),'html.parser')
  if re.sub(r'MapleTrail Software(?! Inc\.)','MapleTrail Software Inc.',old.main.get_text(' ',strip=True)).replace('MapleTrail Software Inc..','MapleTrail Software Inc.')!=new.main.get_text(' ',strip=True):errors.append(rel+': legal/support main text changed')
  legal.append(rel)
# Product copy recovered from the pre-redesign site must remain visible.
content=json.loads((root/'content/product-details.json').read_text())
for page,sections in content['pages'].items():
 current=BeautifulSoup((root/page/'index.html').read_text(),'html.parser')
 visible=' '.join(current.main.get_text(' ',strip=True).split())
 for section in sections:
  for text in [section['heading']]+[unit['text'] for unit in section['units']]:
   if text not in visible:errors.append(f'{page}: missing recovered content: {text[:75]}')
# Current Acadie capabilities and locale-specific raw screenshots remain visible.
current_features=json.loads((root/'content/acadie-current.json').read_text())
for locale,page in [('en','acadie'),('fr','acadie/fr-CA')]:
 soup=BeautifulSoup((root/page/'index.html').read_text(),'html.parser');visible=' '.join(soup.main.get_text(' ',strip=True).split());data=current_features[locale]
 for value in [data['title'],data['radio_title'],data['radio_copy'],data['plus_copy']]+[value for card in data['cards'] for value in [card['title'],card['copy'],card['note']]]:
  if value not in visible:errors.append(f'{page}: missing current Acadie feature content')
 for card in data['cards']:
  src='/images/'+page+'/'+card['image']
  if not soup.find('img',src=src):errors.append(f'{page}: missing native feature screenshot {src}')
 # Guard against returning to the superseded screenshots or text-only Radio section.
 for name in ('current-names.webp','current-explore.webp','current-stories.webp',data['radio_image']):
  src='/images/'+page+'/'+name
  if not soup.find('img',src=src):errors.append(f'{page}: missing refreshed screenshot {src}')
 if not soup.select_one('#web-radio img'):errors.append(f'{page}: Radio has no player screenshot')
 if data['names_note'] not in visible:errors.append(f'{page}: missing Names screenshot locale note')
 for node in soup.select('img[src]'):
  if any(old in node['src'] for old in ('names-app-2026','explore-app-2026','stories-app-2026')):errors.append(f'{page}: superseded Acadie screenshot remains')
for p in files:
 ids=[tag['id'] for tag in BeautifulSoup(p.read_text(),'html.parser').select('[id]')]
 if len(ids)!=len(set(ids)):errors.append(f'{p}: duplicate ids')
from PIL import Image
for og in (root/'images/og').glob('*.jpg'):
 if Image.open(og).size!=(1200,630):errors.append(f'{og}: expected 1200x630 sharing card')
result={'html_pages':len(files),'local_references_checked':links,'images_checked':images,'legal_support_bodies_preserved':len(legal),'product_sections_preserved':sum(len(v) for v in content['pages'].values()),'product_content_units_preserved':sum(1+len(s['units']) for v in content['pages'].values() for s in v),'errors':errors,'result':'passed' if not errors else 'failed'}
print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(bool(errors))
