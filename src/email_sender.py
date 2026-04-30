"""
Email Sender Module

This module handles sending Excel reports by email using SMTP with TLS.
It creates a professional plain text email summary, attaches the generated
report file, and includes retry logic for temporary connection issues.

Author: Intern Project - Day 4
Date: 2026-04-25
"""

import os
import socket
import smtplib
import time
from datetime import datetime
from typing import Optional, Tuple
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _create_email_body(daily_metrics: dict, mtd_metrics: dict) -> str:
    """
    Create a readable plain text email body containing key report metrics.

    The email body includes:
    - Daily totals
    - Daily processing and error rates
    - Month-to-date totals
    - Number of MTD days and daily average

    Args:
        daily_metrics: Dictionary containing daily metrics
        mtd_metrics: Dictionary containing month-to-date metrics

    Returns:
        Formatted plain text email body
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Read daily values with safe defaults
    total_count = daily_metrics.get("total_count", 0)
    total_processed = daily_metrics.get("total_processed", 0)
    total_errors = daily_metrics.get("total_errors", 0)
    daily_processing_rate = daily_metrics.get("processing_rate", 0.0)
    daily_error_rate = daily_metrics.get("error_rate", 0.0)

    # Read MTD values with support for both expected and existing project keys
    mtd_total = mtd_metrics.get("mtd_total", mtd_metrics.get("mtd_total_count", 0))
    mtd_processed = mtd_metrics.get("mtd_processed", mtd_metrics.get("mtd_total_processed", 0))
    mtd_errors = mtd_metrics.get("mtd_errors", mtd_metrics.get("mtd_total_errors", 0))
    mtd_processing_rate = mtd_metrics.get("processing_rate", 0.0)
    mtd_error_rate = mtd_metrics.get("error_rate", 0.0)
    num_days = mtd_metrics.get("num_days", 0)
    daily_average = mtd_metrics.get("daily_average", 0)

    # Build the email body line by line for readability
    body_lines = [
        f"Dear Team,",
        "",
        f"Please find attached the daily report for {current_date}.",
        "",
        "Daily Summary",
        "-------------",
        f"Total Count:        {total_count:,}",
        f"Total Processed:    {total_processed:,}",
        f"Total Errors:       {total_errors:,}",
        f"Processing Rate:    {daily_processing_rate:.1f}%",
        f"Error Rate:         {daily_error_rate:.1f}%",
        "",
        "Month-to-Date Summary",
        "---------------------",
        f"MTD Total Count:    {mtd_total:,}",
        f"MTD Processed:      {mtd_processed:,}",
        f"MTD Errors:         {mtd_errors:,}",
        f"Processing Rate:    {mtd_processing_rate:.1f}%",
        f"Error Rate:         {mtd_error_rate:.1f}%",
        f"Number of Days:     {num_days:,}",
        f"Daily Average:      {daily_average:,.0f}",
        "",
        "Please review the attached Excel report for full details.",
        "",
        "Best regards,",
        "Enterprise Reporting Automation System"
    ]

    return "\n".join(body_lines)


def _attach_file(msg: MIMEMultipart, file_path: str) -> None:
    """
    Attach an Excel file to the email message.

    Args:
        msg: Email message object to attach the file to
        file_path: Path to the Excel report file

    Raises:
        FileNotFoundError: If the file does not exist
        OSError: If the file cannot be read
    """
    file_name = os.path.basename(file_path)

    # Create the attachment part for Excel files
    attachment = MIMEBase(
        "application",
        "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    try:
        with open(file_path, "rb") as file:
            attachment.set_payload(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Attachment file not found: {file_path}")
    except OSError as e:
        raise OSError(f"Unable to read attachment file: {str(e)}")

    # Encode the file so it can be sent safely by email
    encoders.encode_base64(attachment)

    # Add header so email clients recognize it as an attachment
    attachment.add_header(
        "Content-Disposition",
        f'attachment; filename="{file_name}"'
    )

    msg.attach(attachment)


def send_email_with_report(
    report_file_path: str,
    daily_metrics: dict,
    mtd_metrics: dict,
    config: dict,
    sender_email: str,
    sender_password: str
) -> Tuple[bool, Optional[str]]:
    """
    Send the generated Excel report by email using SMTP with TLS and retry logic.

    This function:
    1. Reads email settings from the config dictionary
    2. Creates a professional plain text email summary
    3. Attaches the Excel report file
    4. Connects to the SMTP server using TLS
    5. Retries sending up to 3 times with 2-second delays on temporary failures

    Args:
        report_file_path: Path to the generated Excel report file
        daily_metrics: Dictionary containing daily report metrics
        mtd_metrics: Dictionary containing month-to-date metrics
        config: Configuration dictionary with email settings
        sender_email: Sender email address used for SMTP login
        sender_password: Sender email password or app password

    Returns:
        Tuple containing:
        - success (bool): True if email was sent successfully, False otherwise
        - error_message (str or None): Error message if sending failed, None if successful
    """
    try:
        email_config = config.get("email", {})
        recipients = email_config.get("recipients", [])
        smtp_server = email_config.get("smtp_server")
        smtp_port = email_config.get("smtp_port")
    except Exception as e:
        error_msg = f"Invalid email configuration: {str(e)}"
        print(f"[X] Error: {error_msg}")
        return False, error_msg

    # Validate required email configuration values
    if not recipients:
        error_msg = "Email recipients list is missing or empty."
        print(f"[X] Error: {error_msg}")
        return False, error_msg

    if not smtp_server:
        error_msg = "SMTP server is missing in configuration."
        print(f"[X] Error: {error_msg}")
        return False, error_msg

    if not smtp_port:
        error_msg = "SMTP port is missing in configuration."
        print(f"[X] Error: {error_msg}")
        return False, error_msg

    subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    body = _create_email_body(daily_metrics, mtd_metrics)

    # Try sending the email up to 3 times
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        print(f"Sending email (attempt {attempt}/{max_attempts})...")

        try:
            # Create a fresh email message for each attempt
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            # Attach the plain text body
            msg.attach(MIMEText(body, "plain"))

            print("Attaching Excel report...")
            _attach_file(msg, report_file_path)

            print("Connecting to SMTP server...")
            with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
                print("Starting TLS encryption...")
                server.starttls()

                print("Logging in to SMTP server...")
                server.login(sender_email, sender_password)

                print("Sending email message...")
                server.sendmail(sender_email, recipients, msg.as_string())

            print("[OK] Email sent successfully.")
            return True, None

        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP authentication failed. Check sender email and password."
            print(f"[X] Error: {error_msg}")
            return False, error_msg

        except FileNotFoundError as e:
            error_msg = str(e)
            print(f"[X] Error: {error_msg}")
            return False, error_msg

        except smtplib.SMTPException as e:
            error_msg = f"SMTP connection or sending error: {str(e)}"
            print(f"[X] Error: {error_msg}")

        except OSError as e:
            error_msg = f"File or network error: {str(e)}"
            print(f"[X] Error: {error_msg}")

        except Exception as e:
            error_msg = f"Unexpected error while sending email: {str(e)}"
            print(f"[X] Error: {error_msg}")

        # Wait before retrying, unless this was the final attempt
        if attempt < max_attempts:
            print("Retrying in 2 seconds...")
            time.sleep(2)

    final_error = "Failed to send email after 3 attempts."
    print(f"[X] Error: {final_error}")
    return False, final_error

# Made with Bob