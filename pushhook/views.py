from sys import platform as _platform
from django.http import HttpResponse
import logging
import json
from .tasks import send_email
import datetime
import requests

logger = logging.getLogger(__name__)


def displayHTML(request):
    return HttpResponse('Welcome to push-HOOK!!')


def hooked(request):
    logger.info('hooked - ' + request.method)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        type = data['repository']['type']
        repository = data['repository']['name']
        if 'tag' == type:
            response = requests.get('http://35.187.144.233:4390/update_tags')
            logger.info('status of push - %s' % response.status_code)
            logger.info('pushed tag -- %s' % repository)
        else:
            if 'Curofy' == repository:
                if 'pullrequest' in data:
                    branch_name = data['pullrequest']['destination']['name']
                    logger.info('hooked - merged in %s:%s' % (repository, branch_name))
                    if branch_name == 'development' or branch_name == 'master':
                        commit_author = data['pullrequest']['author']
                        commit_hash = data['pullrequest']['merge_commit']['hash'][:7]
                        commit_url = data['pullrequest']['links']['html']['href']
                        logger.info(_platform)
                        send_email.delay(subject='%s committed %s in %s' % (commit_author, commit_hash, repository),
                                         template='pushhook/pull_hook.html',
                                         context={'author': commit_author, 'link': commit_url,
                                                  'date': datetime.date.today()},
                                         to_emails=['diwas.sharma@curofy.com', 'natesh.relhan@curofy.com',
                                                    'simar.arora@curofy.com'])
                elif 'push' in data:
                    branch_name = data['push']['changes'][0]['new']['name']
                    logger.info('hooked - pushed in %s:%s' % (repository, branch_name))
                    if branch_name == 'development' or branch_name == 'master':
                        commit_author = data['actor']['username']
                        commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
                        commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
                        logger.info(_platform)
                        send_email.delay(subject='%s committed %s in %s' % (commit_author, commit_hash, repository),
                                         template='pushhook/pull_hook.html',
                                         context={'author': commit_author, 'link': commit_url,
                                                  'date': datetime.date.today()},
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
