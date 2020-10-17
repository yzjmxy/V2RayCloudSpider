# test model

import sys
sys.path.append('/qinse/V2RaycSpider0925')

from lxml import etree
from spiderNest.preIntro import *

home = 'https://www.youtube.com/watch?v=9Ubx9KsGR6g&t=86s'


def handle_html(url):
    headers = {
        'username-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'}
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    if res.status_code == 200:
        return res.text


def parse_html(res):
    tree = etree.HTML(res)
    title = tree.xpath("//h1//span/@class")
    return title


def do_driver(url):
    from datetime import datetime
    start = datetime.now()
    api = set_spiderOption(False, True)
    api.get(url)

    target_xpath = "//yt-formatted-string[contains(@class,'content style-scope ytd-video-secondary-info-renderer')]//a/@href"
    WebDriverWait(api, 30).until(EC.presence_of_element_located((
        By.XPATH, "//span[@dir='auto']"
    )))
    # api.find_element_by_xpath("//yt-formatted-string[@role='button']").click()
    data = api.find_element_by_xpath(target_xpath)

    api.quit()
    print(data)
    print('耗时 :{}'.format(datetime.now() - start))


def run():
    response = handle_html(home)
    data = parse_html(response)
    print(data)


if __name__ == '__main__':
    do_driver(home)
