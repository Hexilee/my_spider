from django.http import HttpRequest, HttpResponse, Http404, HttpResponseForbidden

from .function import spider, spider_comments
from spider.settings import CITIES
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET', ])
def save_hotels(request):
    if request.method == 'GET':
        if request.query_params.get('passwd') == 'lichenxi':
            for city in CITIES:
                spider(city)
            return HttpResponse('OK')


@api_view(['GET', ])
def save_comments(request):
    if request.method == 'GET':
        hid = request.query_params.get('hid')
        if hid:
            n = 1
            while True:
                status = spider_comments(hid, n)
                if status != 0:
                    break
                n += 1


@api_view(['GET', ])
def get_comments(request):
    # if request.method == 'GET':
    #     hid = request.query_params.get('hid')
    #     if hid:
    #         resp_list = {}
    #         n = 1
    #         while True:
    #             resp_list['resp%s' % n] =
    pass
