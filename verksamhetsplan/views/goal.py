from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from verksamhetsplan import models
from verksamt import dauth


def goal_create(request, year, long_term_goal_id):
    if not may_edit(request):
        return HttpResponseForbidden("Du har inte rättigheter att skapa mål")

    if request.method == 'POST':
        goal_form = modelform_factory(models.Goal, fields=('goal', 'description', 'status', 'responsible_groups'))
        received_form = goal_form(request.POST,
                                  instance=models.Goal(
                                      year=models.OperationalPlan.objects.get(year=year),
                                      long_term_goal_id=int(long_term_goal_id)
                                  ))
        if received_form.is_valid():
            goal = received_form.save()
        else:
            return HttpResponseBadRequest("Något gick fel när du försökte skapa målet.")
        return HttpResponseRedirect(reverse('vp-operational_area-edit',
                                            args=[year, goal.long_term_goal.sub_area.operational_area]))


def goal_by_id(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
        if request.method == 'GET':
            return render(request, "verksamhetsplan/goal.html", {
                'goal': goal,
                'current_plan': goal.year,
                'operational_plans': models.OperationalPlan.objects.order_by('-id')[:5],
                'comment_form': modelform_factory(models.Comment, fields=('content', 'suggested_status'))(),
                'may_edit': may_edit(request),
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
            'form': goal_form(instance=goal),
            'operational_plans': models.OperationalPlan.objects.order_by('-id')[:5],
        })
    elif request.method == 'POST':
        received_form = goal_form(request.POST, instance=goal)
        if received_form.is_valid():
            received_form.save()
        return HttpResponseRedirect(reverse('vp-goal', args=[goal.id]))


def delete_goal(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")

    if not may_edit(request):
        return HttpResponseForbidden("Du har inte rättigheter att ta bort det här målet")

    if request.method == 'GET':
        return render(request, "verksamhetsplan/confirm_delete.html", {
            'operational_plans': models.OperationalPlan.objects.order_by('-id')[:5],
        })
    elif request.method == 'POST':
        goal.delete()
        return HttpResponseRedirect(
            reverse('vp-operational_area-edit', args=[goal.year, goal.long_term_goal.sub_area.operational_area]))


def create_comment(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")
    if request.method == 'POST':
        comment = models.Comment(author=request.user, goal=goal,
                                 content=request.POST['comment_form.content'],
                                 suggested_status_id=int(request.POST['suggested_status']))

        comment.save()

        return HttpResponseRedirect(reverse('vp-goal', args=[goal.id]))


def may_edit(request):
    return dauth.has_permission('drek', request.user)
