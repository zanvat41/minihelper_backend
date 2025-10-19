from django.http import JsonResponse
from django.views import View

from utils.auth import already_authorized, get_user
from thirdparty import juhe
from thirdparty import hefeng

import json

from utils.response import CommonResponseMixin, ReturnCode


class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
        else:
            # open_id = request.session.get('open_id')
            # user = User.objects.get(open_id=open_id)
            user = get_user(request)

            data = []

            cities = json.loads(user.focused_cities)
            for city in cities:
                # result = juhe.weather(city)
                result = hefeng.weather(city.get('city'))
                result['city_info'] = city
                data.append(result)

            response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)

        return JsonResponse(data=response, safe=False)

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8') if request.body else '{}'
        received_body = json.loads(received_body)
        cities = received_body.get('cities') if received_body.get('cities') else []

        for city in cities:
            # result = juhe.weather(city)
            result = hefeng.weather(city)
            result['city'] = city
            data.append(result)

        data = self.wrap_json_response(data=data)
        return JsonResponse(data=data, safe=False)