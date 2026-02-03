import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KEYWORDS

BASE_URL = "https://www.tenderafrica.net"


def fetch():
    """Fetch tenders from TenderAfrica that match our keywords."""
    results = []

    try:
        r = requests.get(BASE_URL, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; KamagramTenderRadar/1.0)"
        })

        if r.status_code != 200:
            print(f"[TenderAfrica] HTTP {r.status_code}")
            return results

        soup = BeautifulSoup(r.text, "html.parser")

        # Try different selectors based on site structure
        tender_selectors = [
            ".tender",
            ".tender-item",
            ".listing",
            "article",
            ".item",
            "tr",
        ]

        for selector in tender_selectors:
            items = soup.select(selector)
            if items and len(items) > 1:  # Avoid header rows, etc.
                for item in items:
                    title_elem = (
                        item.select_one("a") or
                        item.select_one("h2") or
                        item.select_one("h3") or
                        item.select_one(".title")
                    )

                    if not title_elem:
                        continue

                    title_text = title_elem.get_text(strip=True).lower()

                    # Check if any keyword matches
                    if any(k.lower() in title_text for k in KEYWORDS):
                        link = title_elem.get("href", "") if title_elem.name == "a" else ""
                        if not link:
                            link_elem = item.select_one("a")
                            if link_elem:
                                link = link_elem.get("href", "")

                        if link and not link.startswith("http"):
                            link = BASE_URL + link

                        deadline_elem = (
                            item.select_one(".deadline") or
                            item.select_one(".date") or
                            item.select_one("time")
                        )
                        deadline = deadline_elem.get_text(strip=True) if deadline_elem else "N/A"

                        results.append({
                            "title": title_elem.get_text(strip=True),
                            "org": "TenderAfrica Listing",
                            "deadline": deadline,
                            "link": link or BASE_URL,
                            "source": "TenderAfrica"
                        })
                break  # Found items with this selector

    except Exception as e:
        print(f"[TenderAfrica] Error fetching: {e}")

    return results


if __name__ == "__main__":
    # Test the scraper
    tenders = fetch()
    print(f"Found {len(tenders)} matching listings:")
    for t in tenders:
        print(f"  - {t['title']}")
