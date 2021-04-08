from django.db import models


class Stock(models.Model):
    title = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=30)
    difference = models.CharField(max_length=30)
    url = models.URLField()

    def __str__(self):
        return f'{self.title} | {self.value} | {self.difference}'
