from sys import platform as _platform
from django.http import HttpResponse
import logging
import json
from .tasks import send_email
import datetime

logger = logging.getLogger(__name__)


def displayHTML(request):
    return HttpResponse('Welcome to push-HOOK!!')


def hooked(request):
    logger.info('hooked - ' + request.method)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        repository = data['repository']['name']
        if 'Curofy' == repository:
            branch_name = data['push']['changes'][0]['new']['name']
            logger.info('hooked - pushed in %s:%s' % (repository, branch_name))
            if branch_name == 'development' or branch_name == 'master':
                commit_author = data['actor']['username']
                commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
                commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
                logger.info(_platform)
                send_email.delay(subject='%s committed %s in %s' % (commit_author, commit_hash, repository),
                                 template='pushhook/pull_hook.html',
                                 context={'author': commit_author, 'link': commit_url, 'date': datetime.date.today()},
                                 to_emails=['diwas.sharma@curofy.com', 'natesh.relhan@curofy.com',
                                            'simar.arora@curofy.com'])
        else:
            logger.info('hooked - pushed in %s' % repository)
        return HttpResponse(status=200)
    else:
        return displayHTML(request)


def displayIntro(request):
    logger.info('displayIntro')
    return HttpResponse('Welcome to Curofy web-HOOK!!')
