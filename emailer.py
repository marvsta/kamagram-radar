import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import EMAIL_FROM, EMAIL_TO, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


def send_email(tenders):
    """Send HTML email with tender opportunities."""

    if not SMTP_PASSWORD:
        print("[Email] SMTP_PASSWORD not set. Skipping email send.")
        print("[Email] Set the SMTP_PASSWORD environment variable to enable emails.")
        return False

    today = datetime.now().strftime("%d %b %Y")

    # Build HTML body
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            h2 {{ color: #2c5aa0; }}
            .tender {{
                background: #f9f9f9;
                border-left: 4px solid #2c5aa0;
                padding: 15px;
                margin: 15px 0;
            }}
            .tender-title {{ font-weight: bold; font-size: 16px; color: #1a1a1a; }}
            .tender-meta {{ color: #666; font-size: 14px; margin: 5px 0; }}
            a {{ color: #2c5aa0; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <h2>Kamagram Tender Radar</h2>
        <p>Hi Marvin,</p>
        <p>Here are <strong>{len(tenders)}</strong> new tender/RFP opportunities for website, web app, and mobile app development:</p>
    """

    for i, t in enumerate(tenders, 1):
        # t is a tuple: (id, title, organization, deadline, link, source)
        body += f"""
        <div class="tender">
            <div class="tender-title">{i}. {t[1]}</div>
            <div class="tender-meta">Organization: {t[2]}</div>
            <div class="tender-meta">Deadline: {t[3]}</div>
            <div class="tender-meta">Source: {t[5]}</div>
            <div class="tender-meta"><a href="{t[4]}">View Full Tender &rarr;</a></div>
        </div>
        """

    body += f"""
        <div class="footer">
            <p>This email was sent by Kamagram Tender Radar on {today}.</p>
            <p>To stop receiving these emails, disable the cron job or update your config.</p>
        </div>
    </body>
    </html>
    """

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Kamagram Tender Radar - {len(tenders)} New Opportunities ({today})"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    # Plain text version
    plain_text = f"Kamagram Tender Radar - {len(tenders)} new opportunities found.\n\n"
    for i, t in enumerate(tenders, 1):
        plain_text += f"{i}. {t[1]}\n   Org: {t[2]}\n   Deadline: {t[3]}\n   Link: {t[4]}\n\n"

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[Email] Successfully sent to {EMAIL_TO}")
        return True
    except Exception as e:
        print(f"[Email] Failed to send: {e}")
        return False


if __name__ == "__main__":
    # Test with dummy data
    test_tenders = [
        (1, "Website Development for Ministry", "Ministry of ICT", "15 Feb 2026", "https://example.com/tender1", "TestSource"),
        (2, "Mobile App Development", "Rwanda Revenue Authority", "20 Feb 2026", "https://example.com/tender2", "TestSource"),
    ]
    send_email(test_tenders)
