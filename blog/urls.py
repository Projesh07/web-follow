from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
import views

urlpatterns = [
    url(r'^$', views.globalStream, name='home'),
    url(r'^globalStream$', views.globalStream, name='globalStream'),
    url(r'^followerStream$', views.followerStream, name='followerStream'),
    url(r'^profile$', views.myProfile, name='profile'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    url(r'^getProfile/(\d+)$', views.getProfile, name='getProfile'),
    url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^postItem$', views.postItem, name='postItem'),
    url(r'^commentItem/(?P<pk>[-\w]+)$', views.commentItem, name='commentItem'),
    url(r'^register$', views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'blog/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]
