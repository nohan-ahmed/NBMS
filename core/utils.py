from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user, borrow, subject, template):
    message = render_to_string(template, {
        'user': user,
        'book':borrow.book,
        'borrow_date':borrow.borrow_date,
        'return_date':borrow.return_date,
    })
    
    send_mail = EmailMultiAlternatives(subject, '', to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()