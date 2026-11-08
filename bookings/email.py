from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_html_email(data):
    subject = data["title"]
    recipient = data["email"]

    html_message = render_to_string("email/email.html", data)

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your booking status has been updated.",
        from_email=None,
        to=[recipient],
    )

    email.attach_alternative(html_message, "text/html")

    try:
        email.send(fail_silently=False)
        return True

    except Exception:  # noqa: BLE001
        return False
