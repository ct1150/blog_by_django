#! -*- coding:utf8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
import datetime

class CrawlerHouse():
    def __init__(self,url='http://esf.fz.fang.com/'):
        self.url = url
        self.page_url = "/house/i3"

    def get_urllist(self,pagecount=3):
        """获取房价详情页面url并存入列表"""
        url_list = []
        for page in range(1,pagecount+1):
            response = requests.get(self.url+self.page_url+str(page)).text
            print("正在分析第"+str(page)+"页")
            time.sleep(0.3)
            soup = BeautifulSoup(response,"lxml")
            for a in soup.select(".houseList .title a"):
                href = self.url + a["href"]
                url_list.append(href)
        return url_list

    def get_house_detail(self,url):
        """根据传入url获取住房详情"""
        detail = {}
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response,"lxml")

            detail['estate'] = soup.find('div',text=re.compile(r'小\s+区')).next_sibling.next_sibling.find('a').get_text().strip()
            detail['area1'] = soup.find('div',text=re.compile(r'区\s+域')).next_sibling.next_sibling.find_all('a')[0].get_text().strip()
            detail['area2'] = soup.find('div',text=re.compile(r'区\s+域')).next_sibling.next_sibling.find_all('a')[1].get_text().strip()
            detail['totalprice'] = int(soup.select(".price_esf i")[0].get_text())
            detail['unitprice'] = re.sub("\D","",soup.find('div',text="单价").previous_sibling.previous_sibling.get_text().strip())
            detail['housetype'] = soup.find('div',text="户型").previous_sibling.previous_sibling.get_text().strip()
            detail['size'] = re.sub("\D","",soup.find('div',text="建筑面积").previous_sibling.previous_sibling.get_text().strip())
            detail['towards'] = soup.find('div',text="朝向").previous_sibling.previous_sibling.get_text().strip()
            detail['floor'] = soup.find('div',text=re.compile(r'^楼层')).previous_sibling.previous_sibling.get_text().strip()
            detail['fitment'] = soup.find('div',text="装修").previous_sibling.previous_sibling.get_text().strip()
            detail['contacts'] = soup.select('.zf_jjname')[0].get_text()
            detail['tel'] = soup.find('span',text=re.compile(r'[0-9]{11}')).get_text()
            detail['houseyear'] = datetime.datetime.strptime(re.sub("\D","",soup.find('span',text='建筑年代').next_sibling.next_sibling.get_text().strip()),'%Y')
            detail['elevator'] = soup.find('span',text='有无电梯').next_sibling.next_sibling.get_text().strip()
            detail['property'] = soup.find('span',text='产权性质').next_sibling.next_sibling.get_text().strip()
            detail['houseform'] = soup.find('span',text='住宅类别').next_sibling.next_sibling.get_text().strip()
            detail['structure'] = soup.find('span',text='建筑结构').next_sibling.next_sibling.get_text().strip()
            detail['buildcategory'] = soup.find('span',text='建筑类别').next_sibling.next_sibling.get_text().strip()
            detail['publictime'] = datetime.datetime.strptime(soup.find('span',text='挂牌时间').next_sibling.next_sibling.get_text().strip(),'%Y-%m-%d')
            detail['url'] = url

        except AttributeError as e:
            print(e)

        return detail

    def main(self):
        url_list = self.get_urllist()
        house_list = []
        for url in url_list:
            house_list.append(self.get_house_detail(url))
        return house_list

if __name__ == "__main__":
    fzhouse = CrawlerHouse()
    print(fzhouse.main())
