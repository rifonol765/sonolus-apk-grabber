import requests, bs4, os, re, cgi
from urllib.parse import urlparse, urljoin

FILENAME_OUTPUT, VERSION_OUTPUT, LINK_OUTPUT = "dl_apk.txt", "dl_version.txt", "dl_link.txt"

def get_filename(response):
    if cd := response.headers.get('Content-Disposition'):
        if filename := cgi.parse_header(cd)[1].get('filename'):
            return filename
    return os.path.basename(urlparse(response.url).path)

def cleanup_outputs():
    for f in [FILENAME_OUTPUT, VERSION_OUTPUT, LINK_OUTPUT]:
        if os.path.exists(f): os.remove(f)

def download():
    cleanup_outputs()
    try:
        print("Fetching version...")
        main_resp = requests.get("https://sonolus.com", timeout=30)
        main_resp.raise_for_status()
        version = bs4.BeautifulSoup(main_resp.text, 'html.parser').find('p', class_='font-bold').text.strip()
        print(f"Version: {version}")

        print("Fetching download link...")
        wiki_url = "https://wiki.sonolus.com/getting-started/installing/android.html"
        wiki_resp = requests.get(wiki_url, timeout=30)
        wiki_resp.raise_for_status()
        link = next((a['href'] for a in bs4.BeautifulSoup(wiki_resp.text, 'html.parser').find_all('a', href=True)
                     if 'download.sonolus.com' in a['href'] and a['href'].endswith('.apk')), None)
        if not link: raise ValueError("APK download link not found")
        if not link.startswith('http'): link = urljoin(wiki_url, link)
        print(f"Link: {link}")

        print("Downloading APK...")
        # Use GET directly, infer filename after download if HEAD fails or isn't preferred
        apk_resp = requests.get(link, stream=True, timeout=300, allow_redirects=True)
        apk_resp.raise_for_status()
        
        actual_filename = get_filename(apk_resp)
        if not actual_filename: raise ValueError("Could not determine filename")
        actual_filename = actual_filename.replace('/', '_').replace('\\', '_') # Sanitize
        print(f"Saving as: {actual_filename}")

        with open(actual_filename, 'wb') as f:
            for chunk in apk_resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")

        with open(FILENAME_OUTPUT, "w") as f_out: f_out.write(actual_filename)
        with open(VERSION_OUTPUT, "w") as f_out: f_out.write(version)
        with open(LINK_OUTPUT, "w") as f_out: f_out.write(link)
        print("Output files generated.")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        # Attempt cleanup even on error
        if 'actual_filename' in locals() and os.path.exists(actual_filename):
             try: os.remove(actual_filename)
             except OSError: pass
        cleanup_outputs() # Also remove text files on error
        return False

if __name__ == "__main__":
    if not download():
        exit(1)
