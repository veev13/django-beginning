from django import forms


class StockSearchForm(forms.Form):
    query = forms.CharField(label='검색어')