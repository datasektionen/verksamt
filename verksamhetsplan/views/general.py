from django.shortcuts import render

from verksamhetsplan import models


def index(request):
    return render(request, "verksamhetsplan/main.html", {
        'operational_plans': models.OperationalPlan.objects.order_by('-id').all()
    })


def groups(request):
    return render(request, "verksamhetsplan/groups.html", {
        'groups': models.Group.objects.filter().order_by('name').all(),
        'operational_plans': models.OperationalPlan.objects.order_by('-id')[:5],
    })


def group(request, name):
    return render(request, "verksamhetsplan/group.html", {
        'group': models.Group.objects.get(name=name),
        'goals': models.Goal.objects.filter(responsible_groups__name=name).order_by('-year').distinct(),
        'operational_plans': models.OperationalPlan.objects.order_by('-id')[:5],
    })
