from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from verksamhetsplan import models


def get_operational_plan(request, year):
    try:
        year = models.OperationalPlan.objects.get(year=year)
    except ObjectDoesNotExist:
        raise Http404("Verksamhetsåret finns inte.")

    return render(request, "verksamhetsplan/operational_plan.html", {
        'current_plan': year,
        'operational_plan': year,
        'operational_areas': models.OperationalArea.objects.filter(subarea__longtermgoal__goal__year=year)
                  .order_by('id').distinct()
    })


def get_operational_area(request, year, area_name):
    try:
        year = models.OperationalPlan.objects.get(year=year)
    except ObjectDoesNotExist:
        raise Http404("Verksamhetsåret finns inte.")

    try:
        operational_area = models.OperationalArea.objects.get(name__iexact=area_name)
    except ObjectDoesNotExist:
        raise Http404("Verksamhetsplansområdet finns inte.")

    return render(request, "verksamhetsplan/operational_area.html", {
        'current_plan': year,
        'operational_areas': models.OperationalArea.objects.filter(subarea__longtermgoal__goal__year=year)
                  .order_by('id').distinct(),
        'operational_area': operational_area,
        'goals': models.Goal.objects
                  .order_by('long_term_goal', 'long_term_goal__sub_area', 'id')
                  .filter(year=year, long_term_goal__sub_area__operational_area=operational_area)
    })
