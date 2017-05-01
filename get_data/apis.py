from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .function import spider
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


def save_comments(request: HttpRequest):
    pass


def get_comments(request: HttpRequest):
    pass
