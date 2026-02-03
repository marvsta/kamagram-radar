"""
Google Custom Search API scraper.

This scraper uses Google Custom Search to find tenders across multiple sites.
You need to set up:
1. Google Custom Search Engine at https://programmablesearchengine.google.com/
2. Get an API key from Google Cloud Console

Set environment variables:
- GOOGLE_API_KEY: Your Google API key
- GOOGLE_CSE_ID: Your Custom Search Engine ID
"""

import os
import requests
from datetime import datetime, timedelta
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KEYWORDS

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")

# Sites to search within
SITES_TO_SEARCH = [
    "jobinrwanda.com",
    "devex.com",
    "reliefweb.int",
    "etenders.gov.za",
    "ungm.org",
    "worldbank.org",
]


def fetch():
    """Use Google Custom Search to find tender opportunities."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("[GoogleSearch] API key or CSE ID not set. Skipping.")
        print("[GoogleSearch] Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.")
        return []

    results = []

    # Build search query
    keyword_query = " OR ".join([f'"{k}"' for k in KEYWORDS[:5]])  # Limit to avoid query length issues

    # Search recent results (last 7 days)
    date_restrict = "d7"  # Last 7 days

    for site in SITES_TO_SEARCH:
        query = f"site:{site} tender ({keyword_query})"

        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_CSE_ID,
                "q": query,
                "dateRestrict": date_restrict,
                "num": 10,
            }

            r = requests.get(url, params=params, timeout=15)

            if r.status_code != 200:
                print(f"[GoogleSearch] API error for {site}: {r.status_code}")
                continue

            data = r.json()
            items = data.get("items", [])

            for item in items:
                title = item.get("title", "")
                link = item.get("link", "")
                snippet = item.get("snippet", "")

                # Extract date from snippet if possible
                deadline = "Check listing"

                results.append({
                    "title": title,
                    "org": site,
                    "deadline": deadline,
                    "link": link,
                    "source": f"Google ({site})"
                })

            print(f"[GoogleSearch] {site}: Found {len(items)} results")

        except Exception as e:
            print(f"[GoogleSearch] Error searching {site}: {e}")

    return results


if __name__ == "__main__":
    tenders = fetch()
    print(f"\nFound {len(tenders)} total results")
    for t in tenders:
        print(f"  - {t['title'][:60]}...")
