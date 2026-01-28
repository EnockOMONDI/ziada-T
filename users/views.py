from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .tasks import send_contact_emails


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            send_contact_emails(inquiry)
            messages.success(request, "Thank you! We received your request.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
