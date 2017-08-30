from django.shortcuts import render

from verksamhetsplan import models


def index(request):
    return render(request, "verksamhetsplan/main.html", {
        'operational_plans': models.OperationalPlan.objects.order_by('-id').all()
    })
