from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from verksamhetsplan import models
from verksamt import dauth


def long_term_goal_by_id(request, pk):
    try:
        long_term_goal = models.LongTermGoal.objects.get(pk=int(pk))
        if request.method == 'GET':
            return render(request, "verksamhetsplan/long_term.html", {
                'long_term_goal': long_term_goal,
                'goals': long_term_goal.goal_set.order_by('year')
            })
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")


def edit_long_term_goal(request, pk):
    try:
        goal = models.LongTermGoal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")

    if not dauth.has_permission('drek', request.user):
        return HttpResponseForbidden("Du har inte rättigheter att redigera det här målet")

    goal_form = modelform_factory(models.LongTermGoal, fields=('goaltext', 'description'))

    if request.method == 'GET':
        return render(request, "verksamhetsplan/edit_long_term_goal.html", {
            'form': goal_form(instance=goal)
        })
    elif request.method == 'POST':
        received_form = goal_form(request.POST, instance=goal)
        if received_form.is_valid():
            received_form.save()
        return HttpResponseRedirect(reverse('vp-long_goal', args=[goal.id]))


def create_comment(request, pk):
    try:
        goal = models.LongTermGoal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")
    if request.method == 'POST':
        comment = models.Comment(long_term_goal=goal, author=request.user, content=request.POST['content'])
        comment.save()
        return HttpResponseRedirect(reverse('vp-long_goal', args=[goal.id]))
