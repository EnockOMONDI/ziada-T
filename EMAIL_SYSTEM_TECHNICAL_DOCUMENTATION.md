# Ziada Email System: Technical Design & Configuration

This document describes the full email system implementation in this project, including all touchpoints needed to replicate it.

---

## 1) System Overview

The app sends transactional emails for two inquiry flows:

1. Contact inquiry (`/contact/`)
2. Corporate inquiry (`/corporates/`)

For each successful form submission, the system sends **two emails**:

- A user confirmation email to the submitter
- An internal notification email to `ADMIN_EMAIL`

Email sending is done **synchronously inside the web request** (no queue worker/celery currently in use for these sends).

---

## 2) End-to-End Flow (Per Form Submit)

1. User submits HTML form (contact or corporate).
2. Django `ModelForm` validates request data.
3. Valid form is saved to DB (`ContactInquiry` or `CorporateInquiry`).
4. `send_*_emails()` builds HTML email templates.
5. `send_email()` dispatches through provider selected by `EMAIL_PROVIDER`:
   - `smtp` (Django SMTP backend)
   - `brevo_api` / `brevo` (Brevo HTTP API via `requests`)
   - `mailtrap_api` (Mailtrap SDK)
6. On success: redirect to `/inquiry-success/?id=<inquiry_id>`.
7. On send failure: show warning message and redirect back to form page.

---

## 3) Code Touchpoints

## 3.1 Models (data persisted before send)

File: `users/models.py`

- `ContactInquiry`
  - `full_name`, `email`, `phone`, `company`, `subject`, `message`, `privacy_consent`, `created_at`, `is_resolved`
- `CorporateInquiry`
  - `full_name`, `email`, `phone`, `company_name`, `role_title`, `monthly_travelers`, `service_needs`, `message`, `created_at`, `is_resolved`

## 3.2 Forms (input validation + widgets)

File: `users/forms.py`

- `ContactForm` (`ModelForm` for `ContactInquiry`)
- `CorporateInquiryForm` (`ModelForm` for `CorporateInquiry`)

Notes:
- Contact `privacy_consent` is hidden (`HiddenInput`) and optional in form config.
- Contact `subject` uses `TRAVEL_CATEGORY_CHOICES`.

## 3.3 Views (save, send, redirect)

File: `users/views.py`

- `contact_view(request)`
  - Saves inquiry
  - Calls `send_contact_emails(inquiry)`
  - On success: redirect to `inquiry-success` with query param `id`
  - On send error: warning flash message + redirect to `contact`

- `corporate_view(request)`
  - Saves inquiry
  - Calls `send_corporate_emails(inquiry)`
  - On success: redirect to `inquiry-success` with query param `id`
  - On send error: warning flash message + redirect to `corporates`

- `inquiry_success_view(request)`
  - Renders success page and displays optional inquiry id

## 3.4 URL routing

File: `adminside/urls.py`

- `/contact/` -> `contact_view`
- `/corporates/` -> `corporate_view`
- `/inquiry-success/` -> `inquiry_success_view`

## 3.5 Email dispatch layer

File: `users/tasks.py`

Primary methods:

- `send_email(subject, html_message, recipient_list)`
  - Provider switch using `EMAIL_PROVIDER`
  - `mailtrap_api` -> `send_email_via_mailtrap(...)`
  - `brevo_api`/`brevo` -> `send_email_via_brevo_api(...)`
  - fallback -> Django `EmailMessage(...).send()` (SMTP backend)

- `send_contact_emails(inquiry)`
  - Renders:
    - `users/emails/user_confirmation.html`
    - `users/emails/admin_notification.html`
  - Sends both emails

- `send_corporate_emails(inquiry)`
  - Renders:
    - `users/emails/corporate_user_confirmation.html`
    - `users/emails/corporate_admin_notification.html`
  - Sends both emails

### Important behavior

`EXTRA_EMAIL_RECIPIENTS` is appended to **both** user and admin recipient lists.

- User confirmation goes to: `[inquiry.email] + extra_recipients`
- Admin notification goes to: `[ADMIN_EMAIL] + extra_recipients`

This means extra recipients receive a copy of user-facing emails too.

## 3.6 HTML Email templates

Files:

- `users/templates/users/emails/user_confirmation.html`
- `users/templates/users/emails/admin_notification.html`
- `users/templates/users/emails/corporate_user_confirmation.html`
- `users/templates/users/emails/corporate_admin_notification.html`

Common template variables:

- `inquiry`
- `site_url`

Templates use `{{ site_url }}/static/ziada-logo.png` for the logo image.

## 3.7 Form pages showing messages

- `templates/pages/contact.html`
- `templates/pages/corporates.html`

Both render Django flash messages (`{% if messages %}` blocks), so send failures are visible to users.

## 3.8 Success page

- `templates/pages/inquiry-success.html`

Rendered only after successful save + successful send.

## 3.9 Admin visibility of inquiries

File: `users/admin.py`

- `ContactInquiryAdmin`
- `CorporateInquiryAdmin`

Allows staff to review submissions even if sending fails.

## 3.10 Operational test command

File: `users/management/commands/send_test_email.py`

Command:

```bash
python3 manage.py send_test_email --user-email you@example.com
```

What it does:
- Creates a `ContactInquiry` test row
- Calls `send_contact_emails(...)`
- Prints key runtime email settings

---

## 4) Configuration Surface

## 4.1 Core settings

File: `tours_travels/settings.py`

Configured variables:

- `EMAIL_PROVIDER` (default: `smtp`)
- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`
- `EXTRA_EMAIL_RECIPIENTS` (comma-separated string -> list)
- `SITE_URL`
- `MAILTRAP_API_TOKEN`
- `BREVO_API_KEY`
- `BREVO_SENDER_EMAIL`
- `BREVO_SENDER_NAME`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `EMAIL_TIMEOUT`
- `EMAIL_RATE_LIMIT_PER_MINUTE`
- `EMAIL_RATE_LIMIT_PER_HOUR`

## 4.2 Production overrides

File: `tours_travels/settings_prod.py`

Re-reads all email variables from OS environment for production deployment.

## 4.3 Deployment environment (Render)

File: `render.yaml`

Email-related env keys present:

- `EMAIL_PROVIDER`
- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`
- `EXTRA_EMAIL_RECIPIENTS`
- `SITE_URL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER` (secret)
- `EMAIL_HOST_PASSWORD` (secret)
- `MAILTRAP_API_TOKEN` (secret)
- `BREVO_API_KEY` (secret)
- `BREVO_SENDER_EMAIL`
- `BREVO_SENDER_NAME`
- `EMAIL_TIMEOUT`

## 4.4 Local env files

Relevant files in repo:

- `.env`
- `.env.development`
- `.env.production`
- `.env.production.template`
- `.env.production.fixed`

For replication, use `.env.production.template` as baseline and inject real secrets at deploy time.

---

## 5) Provider Modes

## 5.1 SMTP mode (`EMAIL_PROVIDER=smtp`)

Path used:
- `send_email()` fallback branch -> Django `EmailMessage.send()`

Required values:
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`

## 5.2 Brevo API mode (`EMAIL_PROVIDER=brevo_api` or `brevo`)

Path used:
- `send_email_via_brevo_api()`
- HTTP POST to `https://api.brevo.com/v3/smtp/email`

Required values:
- `BREVO_API_KEY`
- `BREVO_SENDER_EMAIL` (or parsable fallback from `DEFAULT_FROM_EMAIL`)
- `BREVO_SENDER_NAME` (or parsable fallback from `DEFAULT_FROM_EMAIL`)
- `EMAIL_TIMEOUT` (recommended)
- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`

SMTP variables can still exist but are not used by this branch.

## 5.3 Mailtrap API mode (`EMAIL_PROVIDER=mailtrap_api`)

Path used:
- `send_email_via_mailtrap()`

Required values:
- `MAILTRAP_API_TOKEN`

---

## 6) Dependencies Required

From `requirements.txt` (email-related):

- `requests` (Brevo API HTTP calls)
- `mailtrap` (Mailtrap API SDK)
- Django core mail backend (built-in, no extra package needed)

---

## 7) Replication Guide (Fresh Environment)

## 7.1 Step 1: install dependencies

```bash
pip install -r requirements.txt
```

## 7.2 Step 2: choose provider

Set one:

- `EMAIL_PROVIDER=smtp`, or
- `EMAIL_PROVIDER=brevo_api`, or
- `EMAIL_PROVIDER=mailtrap_api`

## 7.3 Step 3: set minimum env vars

Common minimum:

- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`
- `SITE_URL`
- `EXTRA_EMAIL_RECIPIENTS` (can be empty)

Provider-specific:

- SMTP:
  - `EMAIL_HOST`
  - `EMAIL_PORT`
  - `EMAIL_USE_TLS`
  - `EMAIL_HOST_USER`
  - `EMAIL_HOST_PASSWORD`
  - `EMAIL_TIMEOUT` (recommended)

- Brevo API:
  - `BREVO_API_KEY`
  - `BREVO_SENDER_EMAIL`
  - `BREVO_SENDER_NAME`
  - `EMAIL_TIMEOUT`

- Mailtrap API:
  - `MAILTRAP_API_TOKEN`

## 7.4 Step 4: migrate DB

```bash
python3 manage.py migrate
```

## 7.5 Step 5: run app and test

- Submit `/contact/` form
- Submit `/corporates/` form
- Verify:
  - DB row created
  - expected two emails sent
  - redirect to `/inquiry-success/?id=<id>`

## 7.6 Optional: command-line test

```bash
python3 manage.py send_test_email --user-email you@example.com
```

---

## 8) Error Handling Behavior

- Inquiry data is persisted **before** email sending.
- If send fails:
  - user sees warning flash message
  - request redirects back to originating form
  - inquiry remains in admin for manual follow-up
- If form is invalid:
  - validation error message shown
  - no send attempt

---

## 9) Testing Coverage

File: `users/tests.py`

Covers:

- contact inquiry: save + email subject/recipient assertions
- corporate inquiry: save + email subject/recipient assertions

Test setup uses:
- `EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"`
- `EMAIL_PROVIDER="smtp"`

---

## 10) Operational Notes & Risks

1. **Synchronous sending in request path**
   - Slow provider responses can delay form submission response and may trigger web worker timeout under load.

2. **Extra recipient fan-out**
   - `EXTRA_EMAIL_RECIPIENTS` receives copies of user confirmations and admin notifications.

3. **Timeout consistency**
   - Keep `EMAIL_TIMEOUT` aligned across `.env.production` and `render.yaml`.

4. **Secrets hygiene**
   - Do not commit real SMTP or API secrets.
   - Use secret manager / Render secret env vars.
   - Rotate any credentials that were previously exposed.

---

## 11) Quick Reference Matrix

| Touchpoint | File |
|---|---|
| Contact form + flow | `users/forms.py`, `users/views.py`, `templates/pages/contact.html` |
| Corporate form + flow | `users/forms.py`, `users/views.py`, `templates/pages/corporates.html` |
| Send orchestration | `users/tasks.py` |
| Email templates | `users/templates/users/emails/*.html` |
| Success page | `templates/pages/inquiry-success.html` |
| URL routes | `adminside/urls.py` |
| Settings/env parsing | `tours_travels/settings.py`, `tours_travels/settings_prod.py` |
| Deploy env contract | `render.yaml` |
| Test command | `users/management/commands/send_test_email.py` |
| Automated tests | `users/tests.py` |

