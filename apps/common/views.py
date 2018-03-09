
from django.shortcuts import render, render_to_response
def head(request):
    return render(request, 'common/head.html')
def index(request):
    return render(request, 'topic.html')
def welcome(request):
    return render(request, 'oscar/promotions/welcome.html')
def regist_success(request):
    return render(request, 'oscar/customer/regist_success.html')