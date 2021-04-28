from django.db import models


class NewsAgency(models.Model):
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)
    logo = models.ImageField()


class Tag(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    agency = models.ForeignKey(NewsAgency, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    published_at = models.DateField()
    url = models.URLField(max_length=500)
    news_id = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, null=True, blank=True)


class StartUrl(models.Model):
    agency = models.ForeignKey(NewsAgency, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)