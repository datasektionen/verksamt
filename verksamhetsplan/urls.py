from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index),
    url('^long_term/(?P<pk>\d+)/$', views.long_term_goal_by_id),
    url('^goal/(?P<pk>\d+)/$', views.goal_by_id),
]
