"""Unit tests for email_skill server."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from email_skill.server import send_email


def test_send_email_success():
    """Test successful email sending with mocked SMTP."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        # Simulate successful send
        result = send_email(
            smtp_server="smtp.example.com",
            port=587,
            username="user",
            password="pass",
            from_addr="from@example.com",
            to_addrs=["to@example.com"],
            subject="Test",
            body="Test body",
            use_tls=True,
            use_ssl=False,
        )
        # Check that SMTP was called correctly
        mock_smtp.assert_called_once_with("smtp.example.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user", "pass")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        assert "sent successfully" in result


def test_send_email_ssl():
    """Test email sending with SSL."""
    with patch("smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server
        result = send_email(
            smtp_server="smtp.example.com",
            port=465,
            username="user",
            password="pass",
            from_addr="from@example.com",
            to_addrs=["to@example.com"],
            subject="Test",
            body="Test body",
            use_tls=False,
            use_ssl=True,
        )
        mock_smtp_ssl.assert_called_once_with("smtp.example.com", 465)
        mock_server.login.assert_called_once_with("user", "pass")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        assert "sent successfully" in result


def test_send_email_no_auth():
    """Test email sending without authentication."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        result = send_email(
            smtp_server="localhost",
            port=25,
            username="",
            password="",
            from_addr="from@example.com",
            to_addrs=["to@example.com"],
            subject="Test",
            body="Test body",
            use_tls=False,
            use_ssl=False,
        )
        mock_smtp.assert_called_once_with("localhost", 25)
        mock_server.login.assert_not_called()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
        assert "sent successfully" in result


def test_send_email_failure():
    """Test email sending failure."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("Login failed")
        mock_smtp.return_value = mock_server
        result = send_email(
            smtp_server="smtp.example.com",
            port=587,
            username="user",
            password="pass",
            from_addr="from@example.com",
            to_addrs=["to@example.com"],
            subject="Test",
            body="Test body",
            use_tls=True,
            use_ssl=False,
        )
        assert "Failed to send email" in result
