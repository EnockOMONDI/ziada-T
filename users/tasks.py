from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

try:
    from mailtrap import Mail, Address, MailtrapClient
except Exception:
    Mail = None
    Address = None
    MailtrapClient = None


def send_email_via_mailtrap(subject, html_message, from_email, recipient_list):
    if MailtrapClient is None:
        raise RuntimeError("Mailtrap client is not available. Install mailtrap package.")

    client = MailtrapClient(token=settings.MAILTRAP_API_TOKEN)

    if "<" in from_email and ">" in from_email:
        from_name = from_email.split("<")[0].strip()
        from_email_addr = from_email.split("<")[1].split(">")[0].strip()
    else:
        from_name = "Ziada Travel"
        from_email_addr = from_email.strip()

    mail = Mail(
        sender=Address(email=from_email_addr, name=from_name),
        to=[Address(email=email.strip()) for email in recipient_list],
        subject=subject,
        html=html_message,
    )

    client.send(mail)
    return True


def send_email(subject, html_message, recipient_list):
    provider = getattr(settings, "EMAIL_PROVIDER", "mailtrap_api")
    from_email = settings.DEFAULT_FROM_EMAIL

    if provider == "mailtrap_api":
        return send_email_via_mailtrap(subject, html_message, from_email, recipient_list)

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = "html"
    email.send(fail_silently=False)
    return True


def send_contact_emails(inquiry):
    user_subject = "We received your request"
    admin_subject = "New contact inquiry"

    extra_recipients = [
        email.strip()
        for email in getattr(settings, "EXTRA_EMAIL_RECIPIENTS", [])
        if email.strip()
    ]

    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    user_html = render_to_string(
        "users/emails/user_confirmation.html",
        {
            "inquiry": inquiry,
            "site_url": site_url,
        },
    )
    admin_html = render_to_string(
        "users/emails/admin_notification.html",
        {
            "inquiry": inquiry,
            "site_url": site_url,
        },
    )

    send_email(user_subject, user_html, [inquiry.email] + extra_recipients)
    send_email(admin_subject, admin_html, [settings.ADMIN_EMAIL] + extra_recipients)
