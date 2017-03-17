from __future__ import absolute_import
from celery import shared_task
from .mailer import Mailer

@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task(ignore_result=True)
def print_hello():
    print('hello there')

@shared_task()
def gen_prime(x):
    multiples = []
    results = []
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
    return results

@shared_task()
def send_email(subject, template, context, to_emails):
    mailer = Mailer()
    mailer.send_messages(subject=subject,template=template,context=context,to_emails=to_emails)