from django.core.mail import send_mail


def send_notification(subject, msg, from_email, to_email):
    return send_mail(
        subject,
        msg,
        from_email,
        [to_email],
        fail_silently=False,
    )
