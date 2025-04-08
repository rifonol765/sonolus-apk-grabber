import requests, sys, os, re

def parse_version_tuple(v_str):
    parts = re.split(r'[._]', v_str)
    try: return tuple(int(p) for p in parts)
    except ValueError: return None

try:
    url = "https://api.github.com/repos/Sonolus/wiki/contents/src/en/release-notes/versions"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token := os.environ.get('GH_API_TOKEN'): headers['Authorization'] = f"token {token}"
    r = requests.get(url, headers=headers, timeout=20); r.raise_for_status()
    files = r.json()
    if not isinstance(files, list): raise ValueError("Bad API response")
    v_strings = [f['name'][:-3] for f in files if f['type']=='file' and f['name'].endswith('.md')]
    if not v_strings: raise ValueError("No version files found")
    latest_v_str, max_v_tuple = "", (-1,)
    for v_str in v_strings:
        if (v_tuple := parse_version_tuple(v_str)) and v_tuple > max_v_tuple:
            max_v_tuple, latest_v_str = v_tuple, v_str
    if not latest_v_str: raise ValueError("No valid version determined")
    changelog_url = f"https://wiki.sonolus.com/release-notes/versions/{latest_v_str}"
    print(latest_v_str); print(changelog_url)
except Exception as e: print(f"ERROR get_version: {e}", file=sys.stderr); sys.exit(1)
