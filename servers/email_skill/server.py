"""
Email sending skill via SMTP.
"""

import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional


def send_email(
    smtp_server: str,
    port: int,
    username: str,
    password: str,
    from_addr: str,
    to_addrs: List[str],
    subject: str,
    body: str,
    use_tls: bool = True,
    use_ssl: bool = False,
) -> str:
    """
    Send an email via SMTP.

    Args:
        smtp_server: SMTP server hostname.
        port: SMTP port number.
        username: Authentication username (often the sender email).
        password: Authentication password.
        from_addr: Sender email address.
        to_addrs: List of recipient email addresses.
        subject: Email subject line.
        body: Plain‑text email body.
        use_tls: If True, start TLS after connecting (default True).
        use_ssl: If True, connect using SSL from the start (default False).

    Returns:
        A success message or error description.
    """
    # Create message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, port)
        else:
            server = smtplib.SMTP(smtp_server, port)  # type: ignore[assignment]

        if use_tls and not use_ssl:
            server.starttls()

        if username or password:
            server.login(username, password)

        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
        return f"Email sent successfully to {', '.join(to_addrs)}"
    except Exception as e:
        return f"Failed to send email: {e}"
