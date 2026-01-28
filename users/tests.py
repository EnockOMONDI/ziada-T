from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactInquiry


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_PROVIDER="smtp",
    DEFAULT_FROM_EMAIL="Ziada Tours and Travel.com <info@ziadatoursandtravel.com>",
    ADMIN_EMAIL="info@ziadatoursandtravel.com",
)
class ContactInquiryEmailTests(TestCase):
    def test_contact_inquiry_saves_and_sends_emails(self):
        payload = {
            "full_name": "Test User",
            "email": "user@example.com",
            "phone": "0700000000",
            "company": "Test Co",
            "subject": "Safari Experience",
            "message": "I want to plan a safari.",
            "privacy_consent": "on",
        }

        response = self.client.post(reverse("contact"), data=payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactInquiry.objects.count(), 1)

        inquiry = ContactInquiry.objects.first()
        self.assertEqual(inquiry.email, payload["email"])
        self.assertEqual(inquiry.subject, payload["subject"])

        self.assertEqual(len(mail.outbox), 2)
        subjects = {email.subject for email in mail.outbox}
        self.assertIn("We received your request", subjects)
        self.assertIn("New contact inquiry", subjects)

        to_addresses = {email.to[0] for email in mail.outbox}
        self.assertIn("user@example.com", to_addresses)
        self.assertIn("info@ziadatoursandtravel.com", to_addresses)

        for email in mail.outbox:
            self.assertEqual(email.from_email, "Ziada Tours and Travel.com <info@ziadatoursandtravel.com>")
