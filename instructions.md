Let's get abit smart with this. I want to build a script or service the searches for these opportunities for Kamagram and emails them To me daily if it gets any hits. That way I can get them as soon as they are live



Ahhh, now we’re talking! That’s smart, Marvin — we can basically **build a “tender radar” for Kamagram** that automatically monitors the web for new RFPs, tenders, or calls for **web, web app, mobile app development** across Africa (or your preferred countries) and emails them to you in real-time/daily.

Here’s a clear plan and technical breakdown for it.

---

## **1️⃣ How It Would Work**

### Flow:

1. **Source Identification**
   Define which sources to monitor:

   * Country eProcurement portals: Kenya, Uganda, Tanzania, South Africa, Rwanda
   * NGO / IGO / multilateral aggregator portals: TendersInfo, TenderImpulse, TenderAfrica, GlobalTenders
   * Job portals that post RFPs: JobInRwanda, Devex (Africa section), UNGM (UN Global Marketplace)

2. **Search / Filter Criteria**
   Use a **set of keywords** relevant to Kamagram:

   ```
   "website development" OR "web app" OR "mobile app" OR "software development" OR "digital platform"
   ```

   Optional: Include phrases like `"IT consultancy"` or `"application development"`.

3. **Scraping / API Fetching**
   For each portal:

   * If they have an **official API**, use that (preferred).
   * If not, **web scraping** using Python (BeautifulSoup, Selenium, or Playwright) for new listings.
   * Check for new tenders posted **since last run** (so you only get new ones).

4. **Filtering & Deduplication**

   * Filter results by **deadline > today**.
   * Remove duplicates across multiple portals.

5. **Email Notification**

   * Send a daily or real-time summary email to yourself with:

     * Tender title
     * Organization / Client
     * Location / Country
     * Deadline
     * Link to full tender

---

## **2️⃣ Tech Stack / Tools**

* **Language:** Python (lightweight, easy to maintain)
* **Libraries:**

  * Web scraping: `requests` + `BeautifulSoup` or `playwright` (for JS-heavy sites)
  * Parsing PDFs (if tender details are PDFs): `PyPDF2` or `pdfplumber`
  * Email: `smtplib` or `sendgrid` for HTML emails
  * Scheduling: `cron` (Linux/macOS) or `schedule` module in Python
* Optional: Store results in **SQLite or JSON** to track what’s already sent (prevents duplicates).

---

## **3️⃣ Pseudocode / Workflow**

```python
# Step 1: Define sources
sources = [
    "https://www.jobinrwanda.com",
    "https://www.tenderimpulse.com",
    "https://www.tendersinfo.com",
    "https://www.tenderafrica.net"
]

# Step 2: Define search keywords
keywords = ["website development", "web app", "mobile app", "software development"]

# Step 3: Fetch tenders from each source
for source in sources:
    tenders = fetch_tenders(source)  # API or scraping
    for tender in tenders:
        if any(keyword in tender.title.lower() for keyword in keywords):
            if tender.deadline > today:
                store_in_db(tender)

# Step 4: Compile email
new_tenders = get_unsent_tenders()
if new_tenders:
    email_body = format_email(new_tenders)
    send_email(to="marvin@example.com", body=email_body)
    mark_as_sent(new_tenders)
```

---

## **4️⃣ Email Format (Example)**

**Subject:** New Kamagram Tender Opportunities – 16 Jan 2026

**Body:**

```
Hi Marvin,

Here are the new tender/RFP opportunities for website, web app, and mobile app development:

1. Title: Website & Mobile App Development for CETA
   Org: Construction Education & Training Authority (South Africa)
   Deadline: 29 Jan 2026
   Link: [https://aitenders.co.za/tender/13643]

2. Title: ICASA Website Development & Maintenance
   Org: Independent Communications Authority of SA
   Deadline: 19 Jan 2026
   Link: [https://aitenders.co.za/tender/12827]

No other new tenders found today.

Cheers,
Kamagram Tender Radar
```

---

## **5️⃣ Deployment & Automation**

* Host it on a small server / VPS (Ubuntu) or even **Heroku / Railway / Render**.
* **Cron job**: Run **daily at 7 AM** to fetch, filter, and send email.
* Optional: Push notifications via **WhatsApp/Telegram** instead of email for faster alerts.

---

## **6️⃣ Extras / Smart Features**

* Automatically **download PDFs and parse key details** (deadline, country, keywords)
* Track **previously submitted tenders**
* Filter by **country or organization**
* Optional: **Slack/Telegram integration** instead of email
* Extend to include **global NGOs** if you want opportunities outside Africa

---

If you want, I can **write a full Python script skeleton** for this “Kamagram Tender Radar” right now, including scraping JobInRwanda and TenderImpulse, filtering by your keywords, and sending daily emails — basically a ready-to-run prototype.

Do you want me to do that next?











Perfect. Let’s build a **real, usable v1** of the **Kamagram Tender Radar** 🚀
I’ll give you a **clean, production-lean Python setup** you can actually run, extend, and deploy.

This will:

* Scrape **multiple tender sites**
* Filter for **website / web app / mobile app / software** work
* Avoid duplicates
* Email you **daily only if there are new hits**

I’ll also point out where you can easily add more sources later.

---

## 🧠 Overall Architecture (Simple & Solid)

**Opinion:** Keep v1 boring and reliable. Fancy AI comes later.

**Components**

* Python script
* SQLite DB (to avoid duplicates)
* Keyword filtering
* HTML email summary
* Cron job (daily)

---

## 📁 Project Structure

```text
kamagram_tender_radar/
│
├── radar.py               # main script
├── config.py              # keywords, email, sources
├── db.py                  # sqlite helpers
├── scrapers/
│   ├── jobinrwanda.py
│   └── tenderafrica.py
│
├── requirements.txt
└── tenders.db
```

---

## 📦 requirements.txt

```txt
requests
beautifulsoup4
python-dateutil
```

---

## ⚙️ config.py

```python
# Keywords relevant to Kamagram
KEYWORDS = [
    "website",
    "web development",
    "web application",
    "mobile app",
    "software development",
    "digital platform",
    "system development",
    "IT consultancy"
]

# Email settings
EMAIL_FROM = "alerts@kamagram.com"
EMAIL_TO = "marvin@kamagram.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "alerts@kamagram.com"
SMTP_PASSWORD = "YOUR_APP_PASSWORD"

# Sources to enable/disable
SOURCES = {
    "jobinrwanda": True,
    "tenderafrica": True
}
```

---

## 🗄️ db.py (SQLite – deduplication)

```python
import sqlite3

DB_NAME = "tenders.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tenders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            organization TEXT,
            deadline TEXT,
            link TEXT UNIQUE,
            source TEXT,
            sent INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_tender(t):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO tenders (title, organization, deadline, link, source)
            VALUES (?, ?, ?, ?, ?)
        """, (t["title"], t["org"], t["deadline"], t["link"], t["source"]))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_unsent():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tenders WHERE sent = 0")
    rows = c.fetchall()
    conn.close()
    return rows

def mark_sent(ids):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executemany("UPDATE tenders SET sent = 1 WHERE id = ?", [(i,) for i in ids])
    conn.commit()
    conn.close()
```

---

## 🌍 scrapers/jobinrwanda.py

```python
import requests
from bs4 import BeautifulSoup
from config import KEYWORDS

BASE_URL = "https://www.jobinrwanda.com"

def fetch():
    results = []
    url = f"{BASE_URL}/jobs"
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select(".job-listing"):
        title = job.select_one(".job-listing-title")
        link = job.get("href")

        if not title or not link:
            continue

        title_text = title.text.lower()
        if any(k in title_text for k in KEYWORDS):
            results.append({
                "title": title.text.strip(),
                "org": "Unknown",
                "deadline": "Check listing",
                "link": BASE_URL + link,
                "source": "JobInRwanda"
            })

    return results
```

---

## 🌍 scrapers/tenderafrica.py

```python
import requests
from bs4 import BeautifulSoup
from config import KEYWORDS

BASE_URL = "https://www.tenderafrica.net"

def fetch():
    results = []
    r = requests.get(BASE_URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select(".tender"):
        title = item.select_one("a")
        deadline = item.select_one(".deadline")

        if not title:
            continue

        title_text = title.text.lower()
        if any(k in title_text for k in KEYWORDS):
            results.append({
                "title": title.text.strip(),
                "org": "Various",
                "deadline": deadline.text.strip() if deadline else "N/A",
                "link": BASE_URL + title.get("href"),
                "source": "TenderAfrica"
            })

    return results
```

---

## 📬 Email Sender (inside radar.py)

```python
import smtplib
from email.mime.text import MIMEText

def send_email(tenders):
    body = "<h3>New Kamagram Opportunities</h3><ul>"

    for t in tenders:
        body += f"""
        <li>
            <strong>{t[1]}</strong><br/>
            Org: {t[2]}<br/>
            Deadline: {t[3]}<br/>
            <a href="{t[4]}">View Tender</a><br/><br/>
        </li>
        """

    body += "</ul>"

    msg = MIMEText(body, "html")
    msg["Subject"] = "Kamagram Tender Radar – New Opportunities"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
```

---

## 🚀 radar.py (Main Runner)

```python
from db import init_db, save_tender, get_unsent, mark_sent
from scrapers import jobinrwanda, tenderafrica
from config import SOURCES
from emailer import send_email

def main():
    init_db()

    if SOURCES["jobinrwanda"]:
        for t in jobinrwanda.fetch():
            save_tender(t)

    if SOURCES["tenderafrica"]:
        for t in tenderafrica.fetch():
            save_tender(t)

    unsent = get_unsent()
    if unsent:
        send_email(unsent)
        mark_sent([t[0] for t in unsent])

if __name__ == "__main__":
    main()
```

---

## ⏰ Automation (Daily Email)

### On Linux / VPS / macOS

```bash
crontab -e
```

```cron
0 7 * * * /usr/bin/python3 /path/kamagram_tender_radar/radar.py
```

Runs every day at **7 AM**.

---

## 🔮 Next Smart Upgrades (When You’re Ready)

**Opinion:** These are high-ROI.

* Add **UNGM, Devex, World Bank, AfDB**
* WhatsApp alerts via Twilio
* Auto-rank tenders by relevance
* Auto-draft bid checklists per tender
* Store PDFs and extract deadlines automatically

---

If you want, next I can:

1. **Add UN / NGO tender sources**
2. Convert this into a **Rails microservice**
3. Deploy it to **Heroku/Render**
4. Add a **WhatsApp alert instead of email**

Just tell me where you want to take it next.
