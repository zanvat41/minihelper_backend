import os
import yaml
from django.http import JsonResponse

import utils
from apis.models import App
from utils import response

from minihelper_backend import settings


''' This old method gets app list from yaml file'''
'''

def init_app_data():
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with(open(data_file, 'r', encoding='utf-8')) as f:
        apps = yaml.safe_load(f)
        return apps

def get_menu(request):
    global_app_data = init_app_data()
    published_app_data = global_app_data.get('published')
    response = utils.response.wrap_json_response(data=published_app_data,
                                                 code=utils.response.ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

'''


''' New method gets app list from db'''
def get_menu(request):
    apps = App.objects.all()
    apps_data = [app.to_dict() for app in apps]

    response = utils.response.wrap_json_response(data=apps_data,
                                                 code=utils.response.ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)