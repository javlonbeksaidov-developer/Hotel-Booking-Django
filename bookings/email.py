from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string


def send_html_email(data):
    subject = data["title"]
    message = render_to_string("email/email.html", data)
    from_email = None
    recievers = [data["email"]]

    try:
        email = EmailMultiAlternatives(
            subject=subject, body=message, from_email=from_email, to=recievers
        )
        email.attach_alternative(message, "text/html")
        email.send()
        return HttpResponse(content="Sent all !")
    except Exception as e:  # noqa: BLE001
        return HttpResponse(content=f"Error: {e}")