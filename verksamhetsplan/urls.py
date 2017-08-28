from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index),
    url('^long_term/(?P<pk>\d+)/$', views.long_term_goal_by_id, name='vp-long_goal'),
    url('^goal/(?P<pk>\d+)/$', views.goal_by_id, name='vp-goal'),
    url('^(?P<year>[^/]+)/$', views.get_operational_plan, name='vp-operational_plan'),
    url('^(?P<year>[^/]+)/(?P<area_name>[^/]+)/$', views.get_operational_area, name='vp-operational_area'),
]
