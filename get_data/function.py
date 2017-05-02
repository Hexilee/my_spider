from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from spider.settings import ROOT_URL, RE_COMMENT, AGENT_HEADER
import re
import json
from typing import Iterable
import logging
import time
import urllib.error

from .models import Hotel, Comment

logging.basicConfig(level=logging.INFO)


def to_json(iterable: Iterable) -> str:
    return json.dumps(iterable, ensure_ascii=False)


def get_hotel(driver: WebDriver, city: str, n: int) -> None:
    driver.get('%s/%s/p%d' % (ROOT_URL, city, n))

    driver.implicitly_wait(1)

    hotel_list = driver.find_element_by_id('hotel_list')
    hotels = hotel_list.find_elements_by_class_name('searchresult_list')
    for hotel in hotels:
        hid = str(hotel.get_attribute('id'))
        if not re.match(r'^\d+$', hid):
            continue
        name = driver.find_element_by_xpath('//*[@id="%s"]/ul/li[2]/h2/a' % hid).get_attribute('title')
        try:
            points = hotel.find_element_by_class_name('hotel_value').text
        except Exception:
            continue
        start_price = hotel.find_element_by_class_name('J_price_lowList').text
        about_points = hotel.find_element_by_class_name('hotel_judgement').text
        points_count = RE_COMMENT.search(about_points).group()
        logging.info('%s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (city, hid, name, n, points, start_price, points_count))
        if Hotel.objects.filter(hid=hid).count() == 0:
            Hotel.objects.create(city=city, hid=hid, name=name, page=n, points=points, start_price=start_price,
                                 points_count=points_count)


def spider(city: str, start=1) -> None:
    driver = webdriver.PhantomJS()
    for n in range(start, 161):
        try:
            get_hotel(driver, city, n)
        except (ConnectionRefusedError, urllib.error.URLError, ConnectionResetError, TypeError, AttributeError):
            del driver
            time.sleep(30)
            spider(city, n)
            break


def spider_comments(hid: str, n: int) -> int:
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = AGENT_HEADER
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    del dcap

    try:
        driver.get('%s/dianping/%s_p%st0.html' % (ROOT_URL, hid, n))
        driver.implicitly_wait(0.5)
    except (ConnectionRefusedError, urllib.error.URLError, ConnectionResetError, TypeError, AttributeError):
        del driver
        time.sleep(10)
        return spider_comments(hid, n)

    comment_list = driver.find_elements_by_class_name('comment_detail_list')[1]
    comments = comment_list.find_elements_by_class_name('comment_block')

    for comment in comments:
        try:
            name = comment.find_element_by_class_name('name').find_element_by_tag_name('span').text
            cid = comment.get_attribute('data-cid')
            points = comment.find_element_by_class_name('n').text
            room_type = comment.find_element_by_class_name('room_link').text
            content = comment.find_element_by_class_name('J_commentDetail').text.strip()
        except Exception:
            continue
        logging.info('%s\n%s\n%s\n%s\n%s\n%s\n' % (hid, name, n, room_type, points, content))

        if Comment.objects.filter(cid=cid).count() == 0:
            Comment.objects.create(cid=cid, content=content, hotel=hid, page=n, points=points, room_type=room_type,
                                   name=name)

        elif not Comment.objects.filter(cid=cid).exclude(page=n).count() == 0:
            return 1

    del driver
    return 0


if __name__ == '__main__':
    spider('beijing1')
