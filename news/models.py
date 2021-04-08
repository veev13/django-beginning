from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    url = models.URLField(primary_key=True)
    # sid: 분야
    sid = models.IntegerField(db_index=True, default=101)
    SIDS = ((101, '경제'), (105, 'IT/과학'), (1000, 'e스포츠'))

    class Meta:
        ordering = ['-create_time']
