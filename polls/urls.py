from django.conf.urls import patterns, url
from polls import views

urlpatterns = patterns('',
                       url(r'^$', views.Main.as_view(), name='main'),
                       url(r'^pub_date$', views.FilmListByDate.as_view(), name='film_list_d'),
                       url(r'^rating$', views.FilmListByRating.as_view(), name='film_list_r'),
                       url(r'^popularity$', views.FilmListByScores.as_view(), name='film_list_p'),
                       url(r'^login$', views.login, name='login'),
                       url(r'^logout$', views.logout, name='logout'),
                       url(r'^reg$', views.register, name='reg'),
                       url(r'^new_film$', views.new_film, name='new_film'),
                       url(r'^confirm/(?P<key>\w+)$', views.register_confirm, name='confirm'),
                       url(r'^film/(?P<pk>\d+)$', views.FilmItem.as_view(), name='film'),
                       url(r'^comment$', views.add_comment, name='add comment'),
                       url(r'^hide_comment$', views.hide_comment, name='hide comment'),
                       url(r'^delete$', views.delete_restore, name='delete-restore film'),
                       url(r'^update$', views.update, name='update film'),
                       url(r'^score$', views.add_score, name='add score'),
                       #url(r'^statistic/(?P<film_id>\d+)$', views.statistic, name='statistic')
                       )
