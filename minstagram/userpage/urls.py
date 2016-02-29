"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from . import views

app_name = 'minstagram'
urlpatterns = [
    url(r'about/$', views.see_about, name='about'),
    url(r'^home/(?P<id>\d+)/$', views.see_post, name='see_post'),
    url(r'^(?:edit-(?P<id>\d+)/)$', views.edit_post, name='edit_post'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_post, name='delete_post'),
    url(r'^new/$', views.create_post, name='create_post'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registered-ok/$', views.regok, name='regok'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^home/', views.go_home, name='home'),
    # url(r'^edit-info/', views.edit_info, name='edit_info'),
    url(r'^friends/$', views.see_friends, name='see_friends'),
    url(r'^search/$', views.find_friends, name='find_friends'),
    url(r'^search/follow/(?P<id>\d+)/$', views.follow, name='follow'),
    url(r'^search/unfollow/(?P<id>\d+)/$', views.unfollow, name='unfollow'),
    url(r'^search/(?P<id>\d+)/$', views.see_user, name='see_user'),
    url(r'^search/(?P<user_id>\d+)/(?P<post_id>\d+)/$', views.see_user_post, name='see_user_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
