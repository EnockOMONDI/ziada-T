import logging

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm, CorporateInquiryForm
from .tasks import send_contact_emails, send_corporate_emails

logger = logging.getLogger(__name__)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            try:
                send_contact_emails(inquiry)
                messages.success(request, "Thank you! We received your request and sent a confirmation email.")
                logger.info("Contact inquiry %s emails sent successfully.", inquiry.id)
            except Exception as exc:
                messages.warning(
                    request,
                    "Your request was received, but the confirmation email could not be sent. Our team will still contact you.",
                )
                logger.exception("Contact inquiry %s email send failed: %s", inquiry.id, exc)
            return redirect("contact")
        messages.error(request, "Please check the form and try again.")
        logger.warning("Contact form validation failed. Errors: %s", form.errors.as_json())
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def corporate_view(request):
    if request.method == "POST":
        form = CorporateInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            try:
                send_corporate_emails(inquiry)
                messages.success(request, "Thank you! Your corporate inquiry was received and a confirmation email was sent.")
                logger.info("Corporate inquiry %s emails sent successfully.", inquiry.id)
            except Exception as exc:
                messages.warning(
                    request,
                    "Your corporate inquiry was received, but the confirmation email could not be sent. Our team will still contact you.",
                )
                logger.exception("Corporate inquiry %s email send failed: %s", inquiry.id, exc)
            return redirect("corporates")
        messages.error(request, "Please check the form and try again.")
        logger.warning("Corporate form validation failed. Errors: %s", form.errors.as_json())
    else:
        form = CorporateInquiryForm()

    return render(request, "pages/corporates.html", {"form": form})
