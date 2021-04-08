from rest_framework import viewsets

from news.models import News
from restapi.serializers import NewsSerializer, StockSerializer, NowWeatherSerializer
from stock.models import Stock
from weather.models import NowWeather


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class NowWeatherViewSet(viewsets.ModelViewSet):
    queryset = NowWeather.objects.all()
    serializer_class = NowWeatherSerializer
