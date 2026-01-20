---
name: email_skill
description: Send emails via SMTP.
allowed-tools:
  - send_email
---

# Email Skill

This skill enables the agent to send emails using SMTP.

## Tools

### send_email
Send an email via SMTP.
- `smtp_server`: SMTP server address (e.g., smtp.gmail.com).
- `port`: SMTP port (e.g., 587 for TLS).
- `username`: SMTP username (usually the sender email).
- `password`: SMTP password or app‑specific password.
- `from_addr`: Sender email address.
- `to_addrs`: List of recipient email addresses (strings).
- `subject`: Email subject.
- `body`: Email body (plain text).
- `use_tls`: Whether to use TLS (default True).
- `use_ssl`: Whether to use SSL (default False). If both TLS and SSL are False, connection is plain.
