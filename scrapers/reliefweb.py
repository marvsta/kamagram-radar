"""
ReliefWeb Jobs API scraper.

ReliefWeb API requires an approved appname.
Register at: https://apidoc.reliefweb.int/parameters#appname

Set environment variable:
- RELIEFWEB_APPNAME: Your approved appname
"""

import requests
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KEYWORDS

API_URL = "https://api.reliefweb.int/v1/jobs"
RELIEFWEB_APPNAME = os.environ.get("RELIEFWEB_APPNAME", "")


def fetch():
    """Fetch IT/technology jobs from ReliefWeb API."""
    results = []

    if not RELIEFWEB_APPNAME:
        print("[ReliefWeb] RELIEFWEB_APPNAME not set. Skipping.")
        print("[ReliefWeb] Register at: https://apidoc.reliefweb.int/parameters#appname")
        return results

    try:
        # Use GET with query parameters
        params = {
            "appname": RELIEFWEB_APPNAME,
            "filter[field]": "career_categories.name",
            "filter[value]": "Information Technology",
            "fields[include][]": ["title", "source.name", "date.closing", "url", "country.name"],
            "sort[]": "date.created:desc",
            "limit": 50,
        }

        r = requests.get(API_URL, params=params, timeout=20)

        if r.status_code != 200:
            print(f"[ReliefWeb] API returned {r.status_code}: {r.text[:200]}")
            return results

        data = r.json()
        jobs = data.get("data", [])

        for job in jobs:
            fields = job.get("fields", {})
            title = fields.get("title", "")
            title_lower = title.lower()

            # Check if any keyword matches
            if any(k.lower() in title_lower for k in KEYWORDS):
                source = fields.get("source", [{}])
                org = source[0].get("name", "Unknown") if source else "Unknown"

                closing = fields.get("date", {}).get("closing", "N/A")
                if closing and closing != "N/A":
                    closing = closing[:10]

                country = fields.get("country", [{}])
                country_name = country[0].get("name", "") if country else ""

                results.append({
                    "title": f"{title} ({country_name})" if country_name else title,
                    "org": org,
                    "deadline": closing,
                    "link": fields.get("url", "https://reliefweb.int/jobs"),
                    "source": "ReliefWeb"
                })

        print(f"[ReliefWeb] Found {len(results)} matching jobs from {len(jobs)} IT jobs")

    except Exception as e:
        print(f"[ReliefWeb] Error: {e}")

    return results


if __name__ == "__main__":
    tenders = fetch()
    print(f"\nFound {len(tenders)} matching jobs:")
    for t in tenders:
        print(f"  - {t['title'][:60]}...")
