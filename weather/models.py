import datetime

from django.db import models


class NowWeather(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    dt = models.BigIntegerField()
    timezone = models.IntegerField()
    weather_list = models.ManyToManyField('Weather', related_name='now_weather_list')

    def __str__(self):
        return f'{self.name}: {self.get_local_time()}'

    def get_local_time(self):
        local_timezone = self.dt + self.timezone
        return datetime.datetime.utcfromtimestamp(local_timezone)

    class Meta:
        ordering = ['name', 'dt']


class PredictWeather(models.Model):
    update_day = models.CharField(max_length=8)
    lat = models.FloatField()
    lon = models.FloatField()
    timezone_offset = models.IntegerField()

    def __str__(self):
        return f'위도: {self.lat}, 경도: {self.lon}, timezon_offset: {self.timezone_offset}'

    @staticmethod
    def timestamp_to_day_str(timestamp, offset=0):
        timestamp += offset
        time = datetime.datetime.utcfromtimestamp(timestamp)
        return f'{time.year}{time.month}{time.day}'

    class Meta:
        unique_together = (('update_day', 'lat', 'lon'),)


class PredictDayWeather(models.Model):
    predict_weather = models.ForeignKey(PredictWeather, related_name='daily', on_delete=models.CASCADE)
    dt = models.BigIntegerField()
    weather_list = models.ManyToManyField('Weather', related_name='predict_day_weather_list')

    def get_local_time(self):
        return datetime.datetime.utcfromtimestamp(self.dt + self.predict_weather.timezone_offset)

    class Meta:
        ordering = ['dt']


class Coord(models.Model):
    now_weather = models.OneToOneField(NowWeather, on_delete=models.CASCADE)
    lat = models.FloatField()  # 위도
    lon = models.FloatField()  # 경도

    def __str__(self):
        return f'위도: {self.lat}, 경도: {self.lon}'


class Weather(models.Model):
    id = models.IntegerField(primary_key=True)
    main = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    icon = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.main} - {self.description}'



class Main(models.Model):
    now_weather = models.OneToOneField(NowWeather, on_delete=models.CASCADE)
    temp = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return \
            f'온도: {self.temp}\n' \
            f'체감온도: {self.feels_like}\n' \
            f'최저온도: {self.temp_min}\n' \
            f'최고온도: {self.temp_max}\n' \
            f'기압: {self.pressure}\n' \
            f'humidity: {self.humidity}'
