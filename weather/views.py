from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView

from crawling import crawl
from weather.forms import WeatherSearchForm
from weather.models import NowWeather, PredictDayWeather, PredictWeather


class WeatherListView(FormView, ListView):
    template_name = 'weather/weather_list.html'
    model = NowWeather
    paginate_by = 10

    form_class = WeatherSearchForm

    def get(self, request, *args, **kwargs):
        template_response = super(WeatherListView, self).get(request, *args, **kwargs)
        return template_response

    def post(self, request, *args, **kwargs):
        message = weather_update(request)
        kwargs['message'] = message
        template_response = super(WeatherListView, self).get(request, *args, **kwargs)
        template_response.context_data.update({'message': kwargs['message']})
        return template_response


class WeatherDetailView(DetailView):
    template_name = 'weather/weather_detail.html'
    context_object_name = 'now_weather'
    model = NowWeather

    def get(self, request, **kwargs):
        template_response = super(WeatherDetailView, self).get(request, **kwargs)
        return template_response

    def get_context_data(self, **kwargs):
        context = super(WeatherDetailView, self).get_context_data(**kwargs)
        predict = \
            PredictWeather.objects.get(
                update_day=PredictWeather.timestamp_to_day_str(datetime.utcnow().timestamp(),
                                                               context['now_weather'].timezone),
                lat=context['now_weather'].coord.lat,
                lon=context['now_weather'].coord.lon,
            )
        context.update({'predict_weather': predict})
        return context


def weather_update(request):
    q = request.POST.get('query', )
    ret = crawl.CrawlWeather().crawl_weather(q)
    if type(ret) == str:
        return ret
    else:
        return 'search success'
