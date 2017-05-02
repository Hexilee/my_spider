from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from spider.settings import CITIES, ROOT_URL, RE_COMMENT
import re
import json
from typing import Iterable
import logging

from .models import Hotel

logging.basicConfig(level=logging.INFO)


def to_json(iterable: Iterable) -> str:
    return json.dumps(iterable, ensure_ascii=False)


def get_hotel(driver: WebDriver, city: str, n: int) -> None:
    driver.get('http://hotels.ctrip.com/hotel/%s/p%d' % (city, n))

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
        comment_about = hotel.find_element_by_class_name('hotel_judgement').text
        comment_count = RE_COMMENT.search(comment_about).group()
        logging.info('%s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (city, hid, name, n, points, start_price, comment_count))

        Hotel.objects.create(city=city, hid=hid, name=name, page=n, points=points, start_price=start_price,
                             comments_count=comment_count)


def spider(city: str) -> None:
    driver = webdriver.PhantomJS()
    for n in range(8, 161, 8):
        get_hotel(driver, city, n)




if __name__ == '__main__':
    spider('beijing1')
