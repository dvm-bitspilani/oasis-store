from shop import views
from django.conf.urls import url, include
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^buy/', views.buy, name = 'buy'),
	url(r'^getcart/', views.getcart, name = 'getcart'),
    url(r'^product/(?P<itemid>[0-9]+)/$', views.getitem, name='getitem'),
    url(r'^items/getall/$', views.getall, name='getall'),
]
