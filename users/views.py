import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

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
                logger.info("Contact inquiry %s emails sent successfully.", inquiry.id)
                return redirect(f"{reverse('inquiry-success')}?id={inquiry.id}")
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
                logger.info("Corporate inquiry %s emails sent successfully.", inquiry.id)
                return redirect(f"{reverse('inquiry-success')}?id={inquiry.id}")
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


def inquiry_success_view(request):
    inquiry_id = request.GET.get("id", "").strip()
    return render(request, "pages/inquiry-success.html", {"inquiry_id": inquiry_id})
