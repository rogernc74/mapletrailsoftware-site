"""Validate static routes, fragments, local images, metadata and release statements."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import json,re,sys
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
for p in files:
 rel=p.relative_to(root).as_posix()
 if rel.count('/')>1 or rel in ['privacy/index.html','support/index.html']:
  if rel=='acadie/fr-CA/index.html':continue
  old=BeautifulSoup(subprocess.check_output(['git','show','b8eb850:'+rel]),'html.parser')
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
for p in files:
 ids=[tag['id'] for tag in BeautifulSoup(p.read_text(),'html.parser').select('[id]')]
 if len(ids)!=len(set(ids)):errors.append(f'{p}: duplicate ids')
from PIL import Image
for og in (root/'images/og').glob('*.jpg'):
 if Image.open(og).size!=(1200,630):errors.append(f'{og}: expected 1200x630 sharing card')
result={'html_pages':len(files),'local_references_checked':links,'images_checked':images,'legal_support_bodies_preserved':len(legal),'product_sections_preserved':sum(len(v) for v in content['pages'].values()),'product_content_units_preserved':sum(1+len(s['units']) for v in content['pages'].values() for s in v),'errors':errors,'result':'passed' if not errors else 'failed'}
print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(bool(errors))
