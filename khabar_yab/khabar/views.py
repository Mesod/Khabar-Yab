from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from .models import News


def index(request):
    return render(request, 'index2.html')


def search_listing(request):
    query = request.GET.get('query', '')
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')
    page_number = int(request.GET.get('page', '1'))
    page_size = int(request.GET.get('page_size', '12'))

    # TODO: search within date range
    news_list = News.objects.annotate(
        search=SearchVector('title', 'text'),
    ).filter(search=query)
    paginator = Paginator(news_list, page_size)
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {
        'page_obj': page_obj,
        'query': query,
        'from': from_date,
        'to': to_date,
        'page_size': page_size,
    })
