import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KEYWORDS

BASE_URL = "https://www.devex.com"

# Devex search URLs for IT/software opportunities
SEARCH_URLS = [
    f"{BASE_URL}/jobs/search?query=software+development",
    f"{BASE_URL}/jobs/search?query=web+development",
    f"{BASE_URL}/jobs/search?query=mobile+app",
    f"{BASE_URL}/jobs/search?query=IT+consultant",
    f"{BASE_URL}/jobs/search?query=database",
    f"{BASE_URL}/funding/search?query=software",
    f"{BASE_URL}/funding/search?query=digital",
]


def fetch():
    """Fetch IT/software jobs and funding opportunities from Devex."""
    results = []
    seen_links = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    for url in SEARCH_URLS:
        try:
            r = requests.get(url, timeout=20, headers=headers)
            if r.status_code != 200:
                print(f"[Devex] {url} returned {r.status_code}")
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            # Devex job/funding cards - try multiple selectors
            cards = soup.select("article, .job-card, .funding-card, .search-result, .listing-item")

            # Also try finding links directly
            if not cards:
                cards = soup.select("a[href*='/jobs/'], a[href*='/funding/']")

            for card in cards:
                try:
                    # Get title and link
                    if card.name == "a":
                        link_elem = card
                        title_elem = card.select_one("h2, h3, h4, .title") or card
                    else:
                        link_elem = card.select_one("a[href*='/jobs/'], a[href*='/funding/']") or card.select_one("a")
                        title_elem = card.select_one("h2, h3, h4, .title, .job-title")

                    if not link_elem:
                        continue

                    href = link_elem.get("href", "")

                    # Skip non-job/funding links
                    if "/jobs/" not in href and "/funding/" not in href:
                        continue

                    title_text = ""
                    if title_elem:
                        title_text = title_elem.get_text(strip=True)
                    if not title_text:
                        title_text = link_elem.get_text(strip=True)

                    if not href or not title_text:
                        continue

                    # Build full link
                    if href.startswith("/"):
                        full_link = BASE_URL + href
                    elif href.startswith("http"):
                        full_link = href
                    else:
                        continue

                    if full_link in seen_links:
                        continue
                    seen_links.add(full_link)

                    # Check keyword match
                    title_lower = title_text.lower()
                    if not any(k.lower() in title_lower for k in KEYWORDS):
                        continue

                    # Determine source type
                    source_type = "Devex Jobs" if "/jobs/" in full_link else "Devex Funding"

                    # Try to get organization
                    org = "Devex"
                    org_elem = card.select_one(".organization, .company, .employer, .org-name")
                    if org_elem:
                        org = org_elem.get_text(strip=True)

                    # Try to get deadline
                    deadline = "Check listing"
                    deadline_elem = card.select_one(".deadline, .date, .closing-date, time")
                    if deadline_elem:
                        deadline = deadline_elem.get_text(strip=True)[:30]

                    results.append({
                        "title": title_text[:200],
                        "org": org,
                        "deadline": deadline,
                        "link": full_link,
                        "source": source_type
                    })

                except Exception:
                    continue

            print(f"[Devex] {url.split('=')[-1]}: {len(results)} matches total")

        except requests.RequestException as e:
            print(f"[Devex] Error fetching {url}: {e}")
            continue

    print(f"[Devex] Total: {len(results)} matches")
    return results


if __name__ == "__main__":
    tenders = fetch()
    print(f"\nFound {len(tenders)} matching listings:")
    for t in tenders:
        print(f"  - {t['title'][:60]}...")
        print(f"    Org: {t['org']}")
        print(f"    Link: {t['link']}")
