from shop import views
from django.conf.urls import url, include
urlpatterns = [
    url(r'^product/(?P<itemid>[0-9]+)/$', views.getitem, name='getitem'),
]