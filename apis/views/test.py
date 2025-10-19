import random
import time

from django.http import HttpResponse


def test(request):
    time.sleep(random.randint(1, 100) * 0.01 * 3.1415)
    return HttpResponse("Hello Test")