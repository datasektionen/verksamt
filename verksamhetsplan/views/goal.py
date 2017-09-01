from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from verksamhetsplan import models
from verksamt import dauth


def goal_by_id(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
        if request.method == 'GET':
            return render(request, "verksamhetsplan/goal.html", {
                'goal': goal,
                'current_plan': goal.year,
                'comment_form': modelform_factory(models.Comment, fields=('content', 'suggested_status'))(),
                'may_edit': may_edit(request),
                'operational_areas': models.OperationalArea.objects.filter(subarea__longtermgoal__goal__year=goal.year)
                          .order_by('id').distinct(),
            })
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")


def edit_goal(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")

    if not may_edit(request):
        return HttpResponseForbidden("Du har inte rättigheter att redigera det här målet")

    goal_form = modelform_factory(models.Goal, fields=('goal', 'description', 'status', 'responsible_groups'))

    if request.method == 'GET':
        return render(request, "verksamhetsplan/edit_goal.html", {
            'form': goal_form(instance=goal)
        })
    elif request.method == 'POST':
        received_form = goal_form(request.POST, instance=goal)
        if received_form.is_valid():
            received_form.save()
        return HttpResponseRedirect(reverse('vp-goal', args=[goal.id]))


def create_comment(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")
    if request.method == 'POST':
        form_factory = modelform_factory(models.Comment, fields=('content', 'suggested_status'))
        comment = models.Comment(author=request.user, goal=goal,
                                 content=request.POST['comment_form.content'],
                                 suggested_status_id=int(request.POST['suggested_status']))

        comment.save()

        return HttpResponseRedirect(reverse('vp-goal', args=[goal.id]))


def may_edit(request):
    return dauth.has_permission('drek', request.user)
