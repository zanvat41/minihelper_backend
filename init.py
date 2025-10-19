# This file is used to load data from app.yaml into database

import os
import yaml
import hashlib
import django
from django.conf import settings  # 推荐使用 django.conf.settings

# 设置正确的 Django 配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minihelper_backend.settings')  # 确保是完整路径
django.setup()

from apis.models import App  # 必须在 django.setup() 之后导入


def init_app_data():
    old_apps = App.objects.all()
    path = os.path.join(settings.BASE_DIR, 'app.yaml')

    with open(path, 'r', encoding='utf-8') as f:
        apps = yaml.safe_load(f)  # 使用 safe_load 更安全

    published = apps.get('published')
    for item in published:
        item = item.get('app')
        src = item.get('category') + item.get('application')
        appid = hashlib.md5(src.encode('utf8')).hexdigest()

        if old_apps.filter(appid=appid).exists():  # 更高效的查询方式
            print('already exist, appid:', appid)
            app = old_apps.get(appid=appid)  # 直接获取
        else:
            app = App()
            print('not exist, appid:', appid)
            app.appid = appid
            app.name = item.get('name')
            app.application = item.get('application')
            app.url = item.get('url')
            app.publish_date = item.get('publish_date')
            app.category = item.get('category')
            app.desc = item.get('desc')
            app.save()


if __name__ == '__main__':
    init_app_data()
