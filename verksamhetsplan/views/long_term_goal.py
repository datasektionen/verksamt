from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from verksamhetsplan import models


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
