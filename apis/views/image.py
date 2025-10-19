import hashlib
import os.path

from django.http import Http404, FileResponse, JsonResponse
from django.views import View

import utils.response
from utils.response import ReturnCode, CommonResponseMixin
from minihelper_backend import settings

class ImageView(View, utils.response.CommonResponseMixin):
    def get(self, request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')

        if not os.path.exists(imgfile):
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_EXIST)
            return JsonResponse(data=response, safe=False)
        else:
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')

    def post(self, request):
        files = request.FILES
        response = []
        for key, value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            with open(path, 'wb') as f:
                f.write(content)
            response.append({
                'name': key,
                'md5': md5
            })
        message = 'post method success'
        response = self.wrap_json_response(data=response, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response, safe=False)

    def delete(self, request):
        md5 = request.GET.get('md5')
        imgname = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, imgname)

        if os.path.exists(path):
            os.remove(path)
            message = 'remove success'
        else:
            message = 'file (%s) not found' % imgname
        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response, safe=False)


def image(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')

        if not os.path.exists(imgfile):
            return Http404()
        else:
            # data = open(imgFile, 'rb').read()
            # return HttpResponse(content=data, content_type='image/jpg')
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
    elif request.met == 'POST':
        print('post')
    elif request.method == 'PUT':
        print('put')
    elif request.method == 'DELETE':
        print('delete')
    else:
        print("not supported")

def image_text(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')

        if not os.path.exists(imgfile):
            response = utils.response.wrap_json_response(code=utils.response.ReturnCode.RESOURCE_NOT_EXIST)
            return JsonResponse(data=response, safe=False)
        else:
            response_data = {'name': md5 + '.jpg', 'url': '/service/image?md5=%s' % md5}
            response = utils.response.wrap_json_response(data=response_data)
            return JsonResponse(data=response, safe=False)


class ImageListView(View, CommonResponseMixin):
    def get(self, request):
        imgDir = settings.IMAGES_DIR
        imgNames = []
        for imgName in os.listdir(imgDir):
            full_path = os.path.join(imgDir, imgName)
            if os.path.isfile(full_path):
                name_without_ext = os.path.splitext(imgName)[0]
                imgNames.append(name_without_ext)
        response_data = {'imgNames': imgNames}
        response = utils.response.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)