from django.conf.urls import url

from . import views

print (' commom urls ')
urlpatterns = [
    url(r'^', views.head),
    url(r'hello$', views.index)
]
