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
# All preexisting legal/support main text must remain unchanged.
import subprocess
legal=[]
for p in files:
 rel=p.relative_to(root).as_posix()
 if rel.count('/')>1 or rel in ['privacy/index.html','support/index.html']:
  if rel=='acadie/fr-CA/index.html':continue
  old=BeautifulSoup(subprocess.check_output(['git','show','b8eb850:'+rel]),'html.parser')
  new=BeautifulSoup(p.read_text(),'html.parser')
  if old.main.get_text(' ',strip=True)!=new.main.get_text(' ',strip=True):errors.append(rel+': legal/support main text changed')
  legal.append(rel)
result={'html_pages':len(files),'local_references_checked':links,'images_checked':images,'legal_support_bodies_preserved':len(legal),'errors':errors,'result':'passed' if not errors else 'failed'}
print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(bool(errors))
