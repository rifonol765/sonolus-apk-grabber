import requests, bs4, os, cgi, sys
from urllib.parse import urlparse, urljoin
FN, LK = "dl_apk.txt", "dl_link.txt"
for f in [FN, LK]:
    if os.path.exists(f): os.remove(f)
afn=None
try:
    wu="https://wiki.sonolus.com/getting-started/installing/android.html"
    wr=requests.get(wu, timeout=30);wr.raise_for_status()
    link=next((a['href'] for a in bs4.BeautifulSoup(wr.text,'html.parser').find_all('a',href=True) if 'download.sonolus.com' in a['href'] and a['href'].endswith('.apk')),None)
    if not link: raise ValueError("Link not found")
    if not link.startswith('http'): link=urljoin(wu, link)
    ar=requests.get(link, stream=True, timeout=300, allow_redirects=True);ar.raise_for_status()
    cd=ar.headers.get('Content-Disposition'); afn = cgi.parse_header(cd)[1].get('filename') if cd else os.path.basename(urlparse(ar.url).path)
    if not afn: raise ValueError("Filename not found")
    afn = afn.replace('/', '_').replace('\\', '_')
    with open(afn, 'wb') as f:
        for c in ar.iter_content(chunk_size=8192): f.write(c)
    with open(FN, "w") as fo: fo.write(afn)
    with open(LK, "w") as fo: fo.write(link)
except Exception as e:
    print(f"ERROR download_sonolus: {e}", file=sys.stderr)
    if afn and os.path.exists(afn):
        try: os.remove(afn)
        except OSError: pass
    for f in [FN, LK]:
        if os.path.exists(f): os.remove(f)
    sys.exit(1)
