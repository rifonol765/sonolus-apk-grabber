# scripts/get_version.py
import requests, bs4, sys, os, re

def sanitize_for_url(v_str):
    # Replace spaces and non-alphanumeric/dot/underscore/hyphen with hyphen
    s = re.sub(r'[^\w._-]+', ' ', v_str)
    s = re.sub(r'\s+', '-', s)
    return s.strip('-')

try:
    main_url = "https://sonolus.com"
    response = requests.get(main_url, timeout=20)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    version_tag = soup.find('p', class_='font-bold')
    if not version_tag:
        raise ValueError("Version tag (<p class='font-bold'>) not found on sonolus.com")
    scraped_version = version_tag.text.strip()
    if not scraped_version:
         raise ValueError("Scraped version string is empty")

    # Generate the likely changelog URL based on the scraped version
    url_version_part = sanitize_for_url(scraped_version)
    changelog_url = f"https://wiki.sonolus.com/release-notes/versions/{url_version_part}"

    print(scraped_version)
    print(changelog_url)

except Exception as e:
    print(f"ERROR get_version: {e}", file=sys.stderr)
    sys.exit(1)
