from rest_framework import serializers

from news.models import News
from stock.models import Stock
from weather.models import Weather, NowWeather

# https://www.django-rest-framework.org/api-guide/relations/
class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['url',
                  'sid',
                  'title',
                  'author',
                  'create_time', ]


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ['title',
                  'value',
                  'difference', ]


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ['main', 'description', 'icon']


class NowWeatherSerializer(serializers.HyperlinkedModelSerializer):
    weather_list = WeatherSerializer(many=True, read_only=True)

    class Meta:
        model = NowWeather
        fields = ['id', 'name', 'dt', 'timezone', 'weather_list']
