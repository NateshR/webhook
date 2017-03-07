import os
from sys import platform as _platform
from django.http import HttpResponse
import logging
import json

ngrok = 'curofyhook'
logger = logging.getLogger(__name__)

def displayHTML(request):
    if ngrok:
        return HttpResponse('Webhook server online! Go to <a href="https://bitbucket.com">Bitbucket</a> to configure your repository webhook for <a href="http://%s.ngrok.io/webhook">http://%s.ngrok.io/webhook</a> <br />\
            You can access ngrok\'s web interface via <a href="http://localhost:4040">http://localhost:4040</a>' % (
            ngrok, ngrok))
    else:
        return HttpResponse(
            'Webhook server online! Go to <a href="https://bitbucket.com">Bitbucket</a> to configure your repository webhook for <a href="%s">%s</a>' % (
                request.build_absolute_uri(), request.build_absolute_uri()))


def hooked(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        commit_author = data['actor']['username']
        commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
        commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
        # Show notification if operating system is OS X
        if _platform == "darwin":
            from pync import Notifier
            Notifier.notify('%s committed %s\nClick to view in Bitbucket' % (commit_author, commit_hash),
                            title='Webhook received!', open=commit_url)
        else:
            return HttpResponse('Webhook received! %s committed %s' % (commit_author, commit_hash))
        return HttpResponse(status=200)
    else:
        return displayHTML(request)


def displayIntro(request):
    if ngrok:
        return HttpResponse('You can access this webhook publicly via at http://%s.ngrok.io/webhook\
            You can access ngrok\'s web interface via http://localhost:4040' % ngrok)
    else:
        return HttpResponse('Webhook server online! Go to http://localhost:9001')
