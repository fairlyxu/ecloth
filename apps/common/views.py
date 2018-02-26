
from django.shortcuts import render, render_to_response
def head(request):
    return render(request, 'common/head.html')


def index(request):
    return render(request, 'topic.html')