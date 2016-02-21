from django.conf.urls import patterns, url, include
from polls import views

urlpatterns = patterns('',
	url(r'^$', views.Main.as_view(), name = 'main'),
	url(r'^pub_date$', views.FilmListByDate.as_view(), name = 'film_list_d'),
	url(r'^rating$', views.FilmListByRating.as_view(), name = 'film_list_r'),
	url(r'^login$', views.login, name = 'login'),
	url(r'^logout$', views.logout, name = 'logout'),
	url(r'^reg$', views.register, name = 'reg'),
	url(r'^new_film$', views.new_film, name = 'new_film'),
	url(r'^confirm/(?P<key>\w+)$', views.register_confirm, name = 'confirm'),
	url(r'^film/(?P<pk>\d+)$', views.FilmItem.as_view(), name = 'film'),
)

