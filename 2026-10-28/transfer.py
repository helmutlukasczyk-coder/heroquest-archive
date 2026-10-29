import hashlib,json,pathlib,urllib.request,urllib.parse,concurrent.futures
rows=json.loads(pathlib.Path('2026-10-28/manifest.json').read_text())['archived_images']
def copy(r):
 url='https://raw.githubusercontent.com/helmutlukasczyk-coder/'+r['repo']+'/'+r['source_commit']+'/'+urllib.parse.quote(r['path'],safe='/')
 data=urllib.request.urlopen(url,timeout=90).read()
 sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert sha==r['sha'] and len(data)==r['size'],r['path']
 p=pathlib.Path('2026-10-28')/r['repo']/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return str(p)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for p in pool.map(copy,rows):print(p)
print('All original blob hashes and sizes verified.')
