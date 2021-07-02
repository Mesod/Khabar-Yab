from django.contrib import admin
from .models import NewsAgency, News, StartUrl, SearchLog

@admin.register(NewsAgency)
class NewsAgencyAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    pass

@admin.register(StartUrl)
class StartUrlAdmin(admin.ModelAdmin):
    pass