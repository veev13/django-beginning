import json
import urllib
from datetime import datetime

import bs4
import requests
from django.db import IntegrityError

from news.models import News
from stock.models import Stock
from weather.models import NowWeather, Coord, Weather, Main, PredictWeather, PredictDayWeather


class NewsCrawl:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

    @staticmethod
    def news_crawl():
        target_url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1={}&listType=title&page={}'
        for sid in News.SIDS:
            news_sid = sid[0]
            for page in range(1, 2):
                html = requests.get(target_url.format(news_sid, page), headers=NewsCrawl.headers).text
                soup = bs4.BeautifulSoup(html, 'html.parser')
                news_tags = soup.select('#main_content ul.type02 li')
                for tags in news_tags:
                    title = tags.find('a').text
                    author = tags.select('.writing')[0].text
                    news_url = tags.find('a')['href']
                    # date_is_new = tags.select('.is_new')[0].text
                    if not News.objects.filter(url=news_url).exists():
                        News.objects.create(
                            title=title,
                            author=author,
                            url=news_url,
                            sid=news_sid,
                        )

    @staticmethod
    def sport_news_crawl():
        target_url = 'https://sports.daum.net/news/ranking'
        sid = News.SIDS[2][0]
        page = 1
        html = requests.get(target_url.format(page), headers=NewsCrawl.headers).text
        # requests.get('https://sports.news.naver.com/index.nhn',headers=NewsCrawl.headers).text
        # requests.get('https://sports.news.naver.com/general/news/index.nhn?isphoto=N&page=1&view=text',headers=NewsCrawl.headers).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        news_tags = soup.select('.list_news li .wrap_cont')
        for tags in news_tags:
            title = tags.select('.tit_news')[0].text
            news_url = tags.find('a')['href']
            author = tags.select('.txt_info')[0].text
            if not News.objects.filter(url=news_url).exists():
                News.objects.create(
                    title=title,
                    author=author,
                    url=news_url,
                    sid=sid,
                )


class StockCrawl:
    @staticmethod
    def stock_crawl(query):
        base_url = 'https://finance.yahoo.com'
        html = requests.get(f'{base_url}/lookup?s={query}').text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tds = soup.select('#lookup-page table td')
        if len(tds) == 0:
            return None
        a_tag = tds[0].find('a')
        path = a_tag['href']
        target_url = f'{base_url}{path}'

        return StockCrawl.stock_update(target_url)

    @staticmethod
    def stock_update(url):
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')

        header = soup.select('#quote-header-info')[0]
        title = header.select(
            'div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1') \
            [0].text
        value = header.select(
            'div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)') \
            [0].text
        difference = header.select(
            'div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\)') \
            [0].text
        obj, created = Stock.objects.update_or_create(defaults={
            'title': title,
            'value': value,
            'difference': difference,
            'url': url,
        }, title=title)
        return obj


class CrawlWeather:
    # https://openweathermap.org/api/one-call-api
    api_key = '50b33116f4bc6463a5c716bd1fc69b34'

    def crawl_weather(self, city_name):
        obj, created = self.get_now_weather(city_name)
        if type(obj) != str:
            self.get_predict_weather(obj.coord.lat, obj.coord.lon)
        return obj  # error message

    def get_predict_weather(self, lat, lon):
        daily_weather_url = f'https://api.openweathermap.org/data/2.5/onecall?exclude=current,minutely,hourly,alerts' \
                            f'&lat={lat}&lon={lon}&appid={CrawlWeather.api_key}&lang=kr'
        response = requests.get(daily_weather_url).text
        res_dict = json.loads(response)
        predict_weather, created = PredictWeather.objects.get_or_create(
            update_day=PredictWeather.timestamp_to_day_str(datetime.utcnow().timestamp(), res_dict['timezone_offset']),
            lat=res_dict['lat'],
            lon=res_dict['lon'],
            defaults={
                'timezone_offset': res_dict['timezone_offset'],
            }
        )
        if not created:
            predict_weather.daily.all().delete()
        daily = res_dict['daily']
        for day in daily:
            predict_day_weather = PredictDayWeather.objects.create(
                predict_weather=predict_weather,
                dt=day['dt'],
            )
            for w in day['weather']:
                weather, _ = Weather.objects.get_or_create(
                    id=w['id'],
                    defaults={
                        'main': w['main'],
                        'description': w['description'],
                        'icon': w['icon'], }
                )
                predict_day_weather.weather_list.add(weather)

    def get_now_weather(self, city_name: str):
        now_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={CrawlWeather.api_key}'
        print(f'NOW_WEATHER_URL:\n{now_weather_url}')
        response = requests.get(now_weather_url).text
        res_dict = json.loads(response)
        if res_dict['cod'] != 200:
            return res_dict['message'], False
        now_weather, created = NowWeather.objects.get_or_create(
            id=res_dict['id'],
            defaults={
                'name': res_dict['name'],
                'dt': res_dict['dt'],
                'timezone': res_dict['timezone'], }
        )
        if not created:
            return now_weather, created
        res_dict_coord = res_dict['coord']
        Coord.objects.create(
            now_weather=now_weather,
            lat=res_dict_coord['lat'],
            lon=res_dict_coord['lon'],
        )

        res_dict_weathers = res_dict['weather']
        for w in res_dict_weathers:
            weather, _ = Weather.objects.get_or_create(
                id=w['id'],
                defaults={
                    'main': w['main'],
                    'description': w['description'],
                    'icon': w['icon'], }
            )
            now_weather.weather_list.add(weather)

        res_dict_main = res_dict['main']
        Main.objects.create(
            now_weather=now_weather,
            temp=res_dict_main['temp'],
            feels_like=res_dict_main['feels_like'],
            temp_min=res_dict_main['temp_min'],
            temp_max=res_dict_main['temp_max'],
            pressure=res_dict_main['pressure'],
            humidity=res_dict_main['humidity'],
        )
        return now_weather, created
