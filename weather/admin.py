from django.contrib import admin

from weather.models import NowWeather, Weather, PredictWeather, Coord

admin.site.register(NowWeather)
admin.site.register(PredictWeather)
admin.site.register(Weather)
admin.site.register(Coord)
