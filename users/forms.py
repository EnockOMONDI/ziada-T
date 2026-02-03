from django import forms

from .models import ContactInquiry, CorporateInquiry


TRAVEL_CATEGORY_CHOICES = (
    ("Safari Experience", "Safari Experience"),
    ("Beach Holiday", "Beach Holiday"),
    ("Corporate Travel", "Corporate Travel"),
    ("Ticketing & Reservations", "Ticketing & Reservations"),
)


class ContactForm(forms.ModelForm):
    subject = forms.ChoiceField(choices=TRAVEL_CATEGORY_CHOICES)

    class Meta:
        model = ContactInquiry
        fields = [
            "full_name",
            "email",
            "phone",
            "company",
            "subject",
            "message",
            "privacy_consent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["full_name"].required = True
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Brian Otieno",
            }
        )

        self.fields["email"].required = True
        self.fields["email"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "brian.otieno@gmail.com",
            }
        )

        self.fields["phone"].required = False
        self.fields["phone"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "07XX XXX XXX (optional)",
            }
        )

        self.fields["company"].required = False
        self.fields["company"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Ziada Holdings (optional)",
            }
        )

        self.fields["subject"].required = True
        self.fields["subject"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none appearance-none",
            }
        )

        self.fields["message"].required = True
        self.fields["message"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "E.g. 5-day Maasai Mara safari for a family of 4, travel dates in June.",
                "rows": 4,
            }
        )

        self.fields["privacy_consent"].required = False
        self.fields["privacy_consent"].widget = forms.HiddenInput()


class CorporateInquiryForm(forms.ModelForm):
    class Meta:
        model = CorporateInquiry
        fields = [
            "full_name",
            "email",
            "phone",
            "company_name",
            "role_title",
            "monthly_travelers",
            "service_needs",
            "message",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["full_name"].required = True
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Your full name",
            }
        )

        self.fields["email"].required = True
        self.fields["email"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Work email",
            }
        )

        self.fields["phone"].required = False
        self.fields["phone"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "+254 XXX XXX XXX",
            }
        )

        self.fields["company_name"].required = True
        self.fields["company_name"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Company name",
            }
        )

        self.fields["role_title"].required = False
        self.fields["role_title"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Your role/title",
            }
        )

        self.fields["monthly_travelers"].required = False
        self.fields["monthly_travelers"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Estimated travelers per month",
                "min": "1",
            }
        )

        self.fields["service_needs"].required = True
        self.fields["service_needs"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none appearance-none",
            }
        )

        self.fields["message"].required = True
        self.fields["message"].widget.attrs.update(
            {
                "class": "w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-primary outline-none",
                "placeholder": "Share your corporate travel requirements, timelines, and priorities.",
                "rows": 5,
            }
        )
