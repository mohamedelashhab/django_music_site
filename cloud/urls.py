from django.conf.urls import url
from . import views

app_name = 'cloud'
urlpatterns = [
    url('^$',views.register,name='register'),
    url('^login/',views.user_login,name='login'),
    url('^logout/$',views.user_logout,name='logout'),
    url('^add_album/$',views.create_album,name='create_album'),
    url('^(?P<pk>\d+)/detail/$',views.detail,name='detail'),
    url(r'^(?P<pk>\d+)/add_song/$',views.add_song,name='create_song'),
    url(r'^/profile/$',views.profile,name='profile'),
    url(r'^/(?P<pk>\d+)/delete/$',views.delete_album,name='delete_album')
]