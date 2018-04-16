#! -*- coding:utf8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
import datetime
import random
from fake_useragent import UserAgent


class CrawlerHouse():
    def __init__(self, url='http://esf.fz.fang.com'):
        self.url = url
        self.page_url = "/house/i3"
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random
        }
        self.randtime = random.uniform(1, 3)

    def get_urllist(self, pagecount=3):
        """获取房价详情页面url并存入列表"""
        url_list = []
        for page in range(1, pagecount + 1):
            try:
                response = requests.get(self.url + self.page_url + str(page), headers=self.headers).text
                print("正在分析第" + str(page) + "页")
            except Exception as e:
                print(e)
            time.sleep(self.randtime)
            soup = BeautifulSoup(response, "lxml")
            for a in soup.select(".houseList .title a"):
                href = self.url + a["href"]
                url_list.append(href)
        return url_list

    def get_house_detail(self, url):
        """根据传入url获取住房详情"""
        detail = {}
        response = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(response, "lxml")
        detail['estate'] = soup.find('div', text=re.compile(r'小\s+区')).next_sibling.next_sibling.find(
            'a').get_text().strip()
        detail['area1'] = soup.find('div', text=re.compile(r'区\s+域')).next_sibling.next_sibling.find_all('a')[
            0].get_text().strip()
        detail['area2'] = soup.find('div', text=re.compile(r'区\s+域')).next_sibling.next_sibling.find_all('a')[
            1].get_text().strip()
        detail['totalprice'] = float(soup.select(".price_esf i")[0].get_text())
        detail['unitprice'] = float(
            re.sub("\D", "", soup.find('div', text="单价").previous_sibling.previous_sibling.get_text().strip()))
        detail['housetype'] = soup.find('div', text="户型").previous_sibling.previous_sibling.get_text().strip()
        detail['size'] = float(
            re.sub("\D", "", soup.find('div', text="建筑面积").previous_sibling.previous_sibling.get_text().strip()))

        try:
            detail['towords'] = soup.find('div', text="朝向").previous_sibling.previous_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['floor'] = soup.find('div',
                                        text=re.compile(r'^楼层')).previous_sibling.previous_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['fitment'] = soup.find('div', text="装修").previous_sibling.previous_sibling.get_text().strip()
        except Exception as e:
            print(e)

        detail['contacts'] = soup.select('.zf_jjname')[0].get_text()

        try:
            detail['tel'] = soup.find('span', text=re.compile(r'[0-9]{11}')).get_text()
        except Exception as e:
            print(e)

        try:
            detail['houseyear'] = datetime.datetime.strptime(
                re.sub("\D", "", soup.find('span', text='建筑年代').next_sibling.next_sibling.get_text().strip()), '%Y')
        except Exception as e:
            print(e)

        try:
            detail['elevator'] = soup.find('span', text='有无电梯').next_sibling.next_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['property'] = soup.find('span', text='产权性质').next_sibling.next_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['houseform'] = soup.find('span', text='住宅类别').next_sibling.next_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['structure'] = soup.find('span', text='建筑结构').next_sibling.next_sibling.get_text().strip()
        except Exception as e:
            print(e)

        try:
            detail['buildcategory'] = soup.find('span', text='建筑类别').next_sibling.next_sibling.get_text().strip()
        except Exception as e:
            print(e)

        detail['publictime'] = datetime.datetime.strptime(
            soup.find('span', text='挂牌时间').next_sibling.next_sibling.get_text().strip(), '%Y-%m-%d')
        detail['url'] = url

        return detail

    def main(self, pagecount=3):
        url_list = self.get_urllist(pagecount)
        house_list = []
        for url in url_list:
            try:
                house_list.append(self.get_house_detail(url))
            except Exception as e:
                print(e)
            time.sleep(self.randtime)
        return house_list


if __name__ == "__main__":
    fzhouse = CrawlerHouse()
    print(fzhouse.main())
