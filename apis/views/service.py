import json
import os.path
import random
import logging

from django.core.cache import cache
from django.http import JsonResponse

from minihelper_backend import settings
from thirdparty import juhe
from utils.auth import already_authorized, get_user
from utils.response import CommonResponseMixin, ReturnCode, wrap_json_response
from utils.timeutil import get_day_left_in_second

popular_stocks = [
    {
        'code': '000001',
        'name': '平安银行',
        'market': 'sz'
    },
    {
        'code':'000002',
        'name':'万科A',
        'market': 'sz'
    },
    {
        'code': '600036',
        'name': '招商银行',
        'market': 'sh'
    },
    {
        'code': '601398',
        'name': '工商银行',
        'market': 'sh'
    }
]

all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座',
                      '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

all_jokes = []

logger = logging.getLogger('django')

def stock(request):
    data = []
    if already_authorized(request):
        user = get_user(request)
        stocks = json.loads(user.focused_stocks)
    else:
        stocks=  popular_stocks

    for stock in stocks:
        key = stock['market'] + '-' + stock['code']
        result = cache.get(key)
        if not result:
            result = juhe.stock(stock['market'], stock['code'])
            timeout = 500
            cache.set(key, result, timeout)
            logger.info('set cache. key = [%s], value = [%s], timeout = [%d]' % (
                key, result, timeout
            ))
        else:
            logger.info(key + ' info is in cache')
        data.append(result)

    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def constellation(request):
    data = []
    if already_authorized(request):
        user = get_user(request)
        constellations = json.loads(user.focused_constellations)
    else:
        constellations = all_constellations

    for xz in constellations:
        result = cache.get(xz)
        if not result:
            result = juhe.constellation(xz)
            timeout = get_day_left_in_second()
            cache.set(xz, result, timeout)
            logger.info('set cache. key = [%s], value = [%s], timeout = [%d]' % (
                xz, result, timeout
            ))
        else:
            logger.info(xz + ' info is in cache')
        data.append(result)

    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def jokes(request):
    if request.method != 'GET':
        print('method not supported')
        return

    global all_jokes

    if not all_jokes:
        all_jokes = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r', encoding='utf-8'))

    limit = 10
    sample_jokes = random.sample(all_jokes, limit)

    response = CommonResponseMixin.wrap_json_response(data=sample_jokes, code=ReturnCode.SUCCESS)

    return JsonResponse(data=response, safe=False)