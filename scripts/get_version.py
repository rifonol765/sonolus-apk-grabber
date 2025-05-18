import requests,bs4,sys,re
try:
    r=requests.get("https://sonolus.com",timeout=30);r.raise_for_status()
    vt=bs4.BeautifulSoup(r.text,'html.parser').find('p',class_='font-bold')
    if not vt:raise ValueError("TagNF")
    fsv=vt.text.strip()
    m=re.match(r'([0-9._]+)(?:\s*\(([0-9]+)\))?(.*)',fsv)
    if not m:raise ValueError(f"ParseErr:'{fsv}'")
    bvp=m.group(1).strip('._');pnd=m.group(2)
    dvp=bvp
    if pnd:dvp+=f" ({pnd})"
    tuk=bvp
    if pnd:tuk+=f"_{pnd}"
    cu=f"https://wiki.sonolus.com/release-notes/versions/{tuk}"
    print(dvp);print(tuk);print(cu)
except Exception as e:print(f"ERRgv:{e}",file=sys.stderr);sys.exit(1)
