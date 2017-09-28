from django.conf.urls import url

from verksamhetsplan.views import comment as comment_views
from verksamhetsplan.views import general as general_views
from verksamhetsplan.views import goal as goal_views
from verksamhetsplan.views import long_term_goal as long_term_goal_views
from verksamhetsplan.views import operational_plan as operational_plan_views

urlpatterns = [
    url('^$', general_views.index),
    url('^long_term/(?P<pk>\d+)/$',
        long_term_goal_views.long_term_goal_by_id, name='vp-long_goal'),
    url('^long_term/(?P<pk>\d+)/edit/$',
        long_term_goal_views.edit_long_term_goal, name='vp-long_goal-edit'),
    url('^long_term/(?P<pk>\d+)/comment/$',
        long_term_goal_views.create_comment, name='vp-long_goal-comment'),

    url('^goal/create/year/(?P<year>[^/]+)/long_term/(?P<long_term_goal_id>\d+)/$',
        goal_views.goal_create, name='vp-goal-create'),
    url('^goal/(?P<pk>\d+)/$',
        goal_views.goal_by_id, name='vp-goal'),
    url('^goal/(?P<pk>\d+)/edit/$',
        goal_views.edit_goal, name='vp-goal-edit'),
    url('^goal/(?P<pk>\d+)/delete/$',
        goal_views.delete_goal, name='vp-goal-delete'),
    url('^goal/(?P<pk>\d+)/comment/$',
        goal_views.create_comment, name='vp-goal-comment'),

    url('^comment/(?P<pk>\d+)/edit/$',
        comment_views.edit_comment, name='vp-comment-edit'),
    url('^comment/(?P<pk>\d+)/delete/$',
        comment_views.delete_comment, name='vp-comment-delete'),

    url('^groups/$',
        general_views.groups, name='vp-groups'),
    url('^group/(?P<name>[^/]+)/$',
        general_views.group, name='vp-group'),

    url('^(?P<year>[^/]+)/$',
        operational_plan_views.get_operational_plan, name='vp-operational_plan'),

    url('^(?P<year>[^/]+)/(?P<area_name>[^/]+)/$',
        operational_plan_views.get_operational_area, name='vp-operational_area'),
    url('^(?P<year>[^/]+)/(?P<area_name>[^/]+)/edit/$',
        operational_plan_views.edit_operational_area, name='vp-operational_area-edit'),
]
