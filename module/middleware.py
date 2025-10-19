import time
import logging


logger = logging.getLogger('stat')
logger2 = logging.getLogger('django')

from minihelper_backend import settings


class StatMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger2.info("Build StatMiddleware")

    def __call__(self, request):
        tick = time.time()
        response = self.get_response(request)
        path = request.path
        full_path = request.get_full_path()
        tock = time.time()
        cost = tock - tick

        content_list = ['now=[%d]' % tock, 'path=[%s]' % path, 'full_path=[%s]' % full_path, 'cost=[%.6f]' % cost]
        content = settings.STATISTICS_SPLIT_FLAG.join(content_list)
        logger.info(content)
        return response