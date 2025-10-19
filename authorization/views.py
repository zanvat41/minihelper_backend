import json

from django.http import JsonResponse
from django.views import View

from apis.models import App
from authorization.models import User
from utils.auth import c2s, already_authorized, get_user
from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin


# Create your views here.

def test_session(request):
    request.session['message'] = 'Test Django Session OK'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def test_session2(request):
    print(request.session.items())
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def get_status(request):
    print('call get_status function...')
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)


def __authorize_by_code(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    print(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickName = post_data.get('nickName').strip()

    response = {}
    if not code or not app_id:
        response['message'] = 'authorization failed, need entire authorization data.'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)

    data = c2s(app_id, code)
    open_id = data.get('openid')
    print('openid: ' + open_id)
    if not open_id:
        response = wrap_json_response(code=ReturnCode.FAILED, message='auth failed')
        return JsonResponse(data=response, safe=False)

    request.session['open_id'] = open_id
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=open_id):
        new_user = User(open_id=open_id, nickName=nickName)
        print('creating user with nickname ' + nickName)
        new_user.save()

    response = wrap_json_response(code=ReturnCode.SUCCESS, message='auth success')
    return JsonResponse(data=response, safe=False)


def logout(request):
    request.session.clear()
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


class UserView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(message='Not login', code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)

        # open_id = request.session.get('open_id')
        # user = User.objects.get(open_id=open_id)
        user = get_user(request, True)

        data = {'focus': {}}
        data['focus']['cities'] = json.loads(user.focused_cities)
        data['focus']['constellations'] = json.loads(user.focused_constellations)
        data['focus']['stocks'] = json.loads(user.focused_stocks)

        apps = user.menu.all()

        '''
        apps_data = [
            {
                "appid": app.appid,
                "name": app.name,
                "application": app.application,
                "url": app.url,
                "publish_date": app.publish_date,
                "category": app.category,
                "desc": app.desc
            }
            for app in apps
        ]
        '''

        apps_data = [app.to_dict() for app in apps]

        data['focus']['menu'] = apps_data

        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(message='Not login', code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)

        # open_id = request.session.get('open_id')
        # user = User.objects.get(open_id=open_id)
        user = get_user(request, True)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('cities')
        constellations = received_body.get('constellations')
        stocks = received_body.get('stocks')
        menu = received_body.get('menu')

        user.focused_cities = json.dumps(cities)
        user.focused_constellations = json.dumps(constellations)
        user.focused_stocks = json.dumps(stocks)

        old_menu = user.menu.all()
        new_menu_ids = []

        for app in menu:
            appid = app.get('appid', 'wrongID')
            if not App.objects.filter(appid=appid):
                print("no such app obj " + appid)
                continue
            new_menu_ids.append(appid)
            app_obj = App.objects.get(appid=appid)
            user.menu.add(app_obj)

        for app_obj in old_menu:
            if app_obj.appid not in new_menu_ids:
                user.menu.remove(app_obj)


        user.save()

        response = self.wrap_json_response(message='modified user info', code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)
