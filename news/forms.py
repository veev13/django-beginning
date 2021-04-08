from django import forms


class NewsSearchForm(forms.Form):
    query = forms.CharField(label='검색어')