from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
 
 
def send_email(subject, to_email, template_name, context=None):
    if context is None:
        context = {}
 
    html_content = render_to_string(template_name, context)
 
    email = EmailMultiAlternatives(
        subject=subject,
        body="Please open this email in an HTML-supported email client.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
 
    email.attach_alternative(html_content, "text/html")
 
    email.send(fail_silently=False)
 
    return True