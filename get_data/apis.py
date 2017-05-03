from django.http import HttpRequest, HttpResponse, Http404, HttpResponseForbidden
from .models import Hotel
from .function import spider, spider_comments
from spider.settings import CITIES, AGENT_HEADER, ALLOWED_HOSTS
from rest_framework.decorators import api_view
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import logging
logging.basicConfig(level=logging.INFO)


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
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = AGENT_HEADER
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            n = 1
            while True:
                status = spider_comments(driver, hid, n)
                if status == 1:
                    break
                n += 1
    return HttpResponse()


@api_view(['GET', ])
def get_comments(request):
    if request.method == 'GET':
        if request.query_params.get('passwd') == 'lichenxi':
            for i in range(5, 101, 5):
                hotels = Hotel.objects.filter(page=i)
                logging.info("\n%s\n" % len(hotels))
                for hotel in hotels:
                    resp = requests.get('http://%s:9000/api/get_data/save_comments?hid=%s' % (ALLOWED_HOSTS[0], hotel.hid))
                    logging.info(resp.status_code)
            return HttpResponse()
