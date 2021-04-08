from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.views.generic.edit import FormMixin

from crawling import crawl
from news.forms import NewsSearchForm

from news.models import News


def crawl_news(request):
    crawl.NewsCrawl.news_crawl()
    crawl.NewsCrawl.sport_news_crawl() # 못가져옴
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))


class NewsListView(FormMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    paginate_by = 20  # 한 페이지에 n개씩

    form_class = NewsSearchForm

    def get_queryset(self, *args, **kwargs):
        q = News.objects.all()
        sid = self.request.GET.get("sid", '')
        query = self.request.GET.get("query", '')
        if sid != '':
            q = q.filter(Q(sid=sid))
        q = q.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).distinct()
        return q

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context.update({'sids': News.SIDS})
        if self.request.GET.get("query", None):
            # query가 없을 경우 의도치 않은 문구(에러문구)도 추가됨
            context.update({'form': self.get_form_class()(self.request.GET)})
        return context
