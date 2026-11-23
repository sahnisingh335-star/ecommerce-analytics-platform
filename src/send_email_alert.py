"""Email the weekly business summary with Resend.

Needs two settings (environment variables or your .env file):
  RESEND_API_KEY   your key from resend.com
  ALERT_EMAIL_TO   the email address that receives the report
Optional: ALERT_EMAIL_FROM (default: onboarding@resend.dev, which Resend allows
for testing; it can only send to the email you signed up to Resend with).

Without RESEND_API_KEY the script runs in preview mode and prints the email.
Run:  python src/send_email_alert.py
"""
import html
import os
from pathlib import Path
import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS = BASE_DIR / "reports"


def md_to_html(md):
    """Tiny converter for our own report (headings, bold, paragraphs)."""
    out = []
    for line in md.splitlines():
        line = html.escape(line.strip())
        if not line or line.startswith("&gt;"):
            continue
        while "**" in line:
            line = line.replace("**", "<b>", 1).replace("**", "</b>", 1)
        if line.startswith("##"):
            out.append(f"<h3>{line.lstrip('# ')}</h3>")
        elif line.startswith("#"):
            out.append(f"<h2>{line.lstrip('# ')}</h2>")
        else:
            out.append(f"<p>{line}</p>")
    return "\n".join(out)


def forecast_block():
    path = REPORTS / "sales_forecast.csv"
    if not path.exists():
        return ""
    f = pd.read_csv(path)
    rows = "".join(
        f"<li>{r.month}: ₹{r.forecast_revenue / 1e7:,.1f} Cr "
        f"(range ₹{r.lower_80 / 1e7:,.1f}–{r.upper_80 / 1e7:,.1f} Cr)</li>"
        for r in f.itertuples())
    return f"<h3>Revenue forecast (next 3 months)</h3><ul>{rows}</ul>"


def main():
    report = REPORTS / "ai_insights.md"
    if not report.exists():
        raise SystemExit("Run python src/ai_insights.py first.")
    body = md_to_html(report.read_text(encoding="utf-8")) + forecast_block()
    subject = "Weekly E-Commerce Business Insights"
    key, to = os.getenv("RESEND_API_KEY"), os.getenv("ALERT_EMAIL_TO")

    if not key or not to:
        print("PREVIEW MODE (set RESEND_API_KEY and ALERT_EMAIL_TO to send)\n")
        print(subject, "\n", body)
        return

    import resend
    resend.api_key = key
    res = resend.Emails.send({
        "from": os.getenv("ALERT_EMAIL_FROM", "onboarding@resend.dev"),
        "to": [to], "subject": subject, "html": body})
    print("Email sent:", res)


if __name__ == "__main__":
    main()
