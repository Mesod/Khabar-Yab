from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'latest_question_list': '1'}
    return render(request, 'index.html', context)