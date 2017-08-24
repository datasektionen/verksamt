from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index),
    url('^goal/(?P<pk>\d+)$', views.goal_by_id),
]
