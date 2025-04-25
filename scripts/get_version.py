# scripts/get_version.py
import requests, bs4, sys, re

def sanitize_for_tag(version_str):
    # Keep only numbers, dots, underscores, hyphens. Replace others with hyphen.
    sanitized = re.sub(r'[^a-zA-Z0-9._-]+', '-', version_str)
    # Collapse multiple hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized

try:
    main_url = "https://sonolus.com"
    response = requests.get(main_url, timeout=30)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    version_tag = soup.find('p', class_='font-bold')
    if not version_tag: raise ValueError("Version tag not found on main page")
    full_scraped_version = version_tag.text.strip()

    # Extract numeric part (match digits, dots, optionally underscores)
    numeric_match = re.match(r'([0-9._]+)', full_scraped_version)
    if not numeric_match: raise ValueError(f"Could not extract numeric part from '{full_scraped_version}'")
    numeric_only_version = numeric_match.group(1).strip('._') # Clean trailing dots/underscores

    # Sanitize the numeric version specifically for the tag
    tag_version = sanitize_for_tag(numeric_only_version)

    changelog_url = f"https://wiki.sonolus.com/release-notes/versions/{numeric_only_version}"

    # Output: 1. Full Version, 2. Tag Version (Numeric-Sanitized), 3. Changelog URL (Numeric)
    print(full_scraped_version)
    print(tag_version)
    print(changelog_url)

except Exception as e:
    print(f"ERROR get_version: {e}", file=sys.stderr)
    sys.exit(1)
