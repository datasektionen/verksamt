from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from verksamhetsplan import models


def edit_comment(request, pk):
    try:
        comment = models.Comment.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404("Kommentaren finns inte")

    if comment.author != request.user:
        return HttpResponseForbidden("Du får bara redigera dina egna kommentarer")

    comment_form = modelform_factory(models.Comment, fields=('content',))

    if request.method == 'GET':
        return render(request, "verksamhetsplan/edit_comment.html", {
            'form': comment_form(instance=comment)
        })
    elif request.method == 'POST':
        received_form = comment_form(request.POST, instance=comment)
        if received_form.is_valid():
            received_form.save()
        if comment.long_term_goal:
            return HttpResponseRedirect(reverse('vp-long_goal', args=[comment.long_term_goal_id]))
        if comment.goal:
            return HttpResponseRedirect(reverse('vp-goal', args=[comment.goal_id]))


def delete_comment(request, pk):
    try:
        comment = models.Comment.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404("Kommentaren finns inte")
    if comment.author != request.user:
        return HttpResponseForbidden("Du får bara ta bort dina egna kommentarer")

    if request.method == 'POST':
        comment.delete()
        if comment.long_term_goal:
            return HttpResponseRedirect(reverse('vp-long_goal', args=[comment.long_term_goal_id]))
        if comment.goal:
            return HttpResponseRedirect(reverse('vp-goal', args=[comment.goal_id]))
    elif request.method == 'GET':
        return render(request, 'verksamhetsplan/confirm_delete.html')
    else:
        raise Http404()
