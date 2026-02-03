import os

# Keywords relevant to Kamagram
KEYWORDS = [
    "website",
    "web development",
    "web application",
    "mobile app",
    "software development",
    "digital platform",
    "system development",
    "IT consultancy",
    "app development",
    "digital solution",
    "IT services",
    "IT equipment",
    "IT system",
    "information technology",
    "ICT",
    "database",
    "e-commerce",
    "portal",
    "online platform",
]

# Email settings - use environment variables for security
EMAIL_FROM = os.environ.get("EMAIL_FROM", "alerts@kamagram.com")
EMAIL_TO = os.environ.get("EMAIL_TO", "marvin@kamagram.com")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "alerts@kamagram.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

# Sources to enable/disable
SOURCES = {
    "jobinrwanda": True,
    "tenderafrica": False,  # Site currently returning 404
    "reliefweb": False,  # Requires RELIEFWEB_APPNAME (register at apidoc.reliefweb.int)
    "google_search": False,  # Requires GOOGLE_API_KEY and GOOGLE_CSE_ID
}

# Google Custom Search settings (optional)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")
