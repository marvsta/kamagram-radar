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

# SendGrid settings - use environment variables for security
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "d-11064e123cf445bcab85f0d5fd2c4ec9")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "alerts@kamagram.com")
EMAIL_TO = os.environ.get("EMAIL_TO", "marvin@kamagram.com")

# Sources to enable/disable
SOURCES = {
    "jobinrwanda": True,
    "brightermonday": True,  # East Africa: Kenya, Uganda, Tanzania
    "devex": False,  # Requires JavaScript rendering - use google_search instead
    "tenderafrica": False,  # Site currently returning 404
    "reliefweb": False,  # Requires RELIEFWEB_APPNAME (register at apidoc.reliefweb.int)
    "google_search": False,  # Requires GOOGLE_API_KEY and GOOGLE_CSE_ID
}

# Google Custom Search settings (optional)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")
