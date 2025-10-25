from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

def send_custom_email(subject, template_path, context, to_email):
    context = {
        **context,
        'subject': subject,
        'app_name': getattr(settings, 'APP_NAME', 'App'),
        'year': datetime.now().year,
    }
    html = render_to_string(template_path, context)
    msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html, 'text/html')
    msg.send()
