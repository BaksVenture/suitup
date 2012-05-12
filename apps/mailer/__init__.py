VERSION = (0, 2, 0, "a", 1) # following PEP 386
DEV_N = 3


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version


__version__ = get_version()


PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
}


# replacement for django.core.mail.send_mail


def send_mail(subject, html_content, from_email, recipient_list, attachments=[], priority="medium",
              fail_silently=False, auth_user=None, auth_password=None):
    
    from django.utils.encoding import force_unicode
    from django.core.mail import EmailMultiAlternatives
    from mailer.models import make_message
    from django.utils.html import strip_tags
    
    priority = PRIORITY_MAPPING[priority]
    
    message = strip_tags(html_content)
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    msg = make_message(subject=subject,
                       body=message,
                       from_email=from_email,
                       to=recipient_list,
                       priority=priority)
    email = msg.email
    email = EmailMultiAlternatives(email.subject, email.body, email.from_email, email.to)
    email.attach_alternative(html_content, "text/html")
    
    for att in attachments:
        email.attach(att)
    
    msg.email = email
    msg.save()
    return 1
    

def send_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    from mailer.models import make_message
    num_sent = 0
    for subject, message, sender, recipient in datatuple:
        num_sent += send_mail(subject, message, sender, recipient)
    return num_sent


def mail_admins(subject, message, fail_silently=False, connection=None, priority="medium"):
    from django.conf import settings
    from django.utils.encoding import force_unicode
    
    return send_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.ADMINS])


def mail_managers(subject, message, fail_silently=False, connection=None, priority="medium"):
    from django.conf import settings
    from django.utils.encoding import force_unicode
    
    return send_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.MANAGERS])
