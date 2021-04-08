from django import forms


class WeatherSearchForm(forms.Form):
    query = forms.CharField(max_length=20, label='도시 이름')