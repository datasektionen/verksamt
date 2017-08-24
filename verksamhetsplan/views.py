from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from . import models


def index(request):
    return render(request, "verksamhetsplan/main.html")


def goal_by_id(request, pk):
    try:
        goal = models.Goal.objects.get(pk=int(pk))
        if request.method == 'GET':
            return render(request, "verksamhetsplan/goal.html", {'goal': goal})
    except ObjectDoesNotExist:
        raise Http404("Målet finns inte")
