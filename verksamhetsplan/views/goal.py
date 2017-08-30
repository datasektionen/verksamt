from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from verksamhetsplan import models


def goal_by_id(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
        if request.method == 'GET':
            return render(request, "verksamhetsplan/goal.html", {'goal': goal})
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")


def create_comment(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")
    if request.method == 'POST':
        comment = models.Comment(goal=goal, author=request.user, content=request.POST['content'])
        comment.save()
        return HttpResponseRedirect(reverse('vp-goal', args=[goal.id]))
