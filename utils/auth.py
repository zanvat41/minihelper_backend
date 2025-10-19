import json

import requests

import minihelper_backend.settings
from authorization.models import User
from utils import proxy


def get_user(request, preload=False):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('open_id')
    if preload:
        user = User.objects.prefetch_related('menu').get(open_id=open_id)
    else:
        user = User.objects.get(open_id=open_id)
    return user


def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True

    return is_authorized


def c2s(app_id, code):
    return code2session(app_id, code)


def code2session(app_id, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (app_id, minihelper_backend.settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    # response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data