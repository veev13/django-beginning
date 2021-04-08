from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView

from crawling.crawl import StockCrawl
from stock.forms import StockSearchForm
from stock.models import Stock


class StockListView(FormView, ListView):
    model = Stock
    paginate_by = 20

    form_class = StockSearchForm
    template_name = 'stock/stock_list.html'

    def get(self, request, *args, **kwargs):
        template_response = super(StockListView, self).get(request, *args, **kwargs)
        context_data = template_response.context_data
        context_data.update(*args)
        return template_response

    def post(self, request, *args, **kwargs):
        query = request.POST.get('query', )
        form = StockSearchForm(request.POST)
        context = {'form': form,
                   'searched': True,
                   'searched_stock': StockCrawl.stock_crawl(query)}
        return self.get(request, context)

    def get_context_data(self, *args, **kwargs):
        context = super(StockListView, self).get_context_data(*args, **kwargs)
        return context


def stock_update(request):
    url = request.GET.get('url', )
    form = StockSearchForm()
    context = {'form': form,
               'searched': True,
               'searched_stock': StockCrawl.stock_update(url)}
    return StockListView.as_view()(request, context)
