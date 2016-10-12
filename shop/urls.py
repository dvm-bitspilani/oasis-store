from shop import views
from django.conf.urls import url, include
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^buy', views.buy, name = 'buy'),
    url(r'^product/(?P<itemid>[0-9]+)/$', views.getitem, name='getitem'),
]
