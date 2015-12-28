from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /user/1
    url(r'^user/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
]
