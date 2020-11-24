from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from comments.forms import CommentForm
from core.models import Person


def process_post_add_comment(request, context,
                             datapackage, force_anonymous_user,
                             success_view_name,
                             failure_template_name):
    if force_anonymous_user:
        person = None
    else:
        person = Person.objects.get(user=request.user)

    comment_form = CommentForm(request.POST, datapackage_id=datapackage.id, person=person, allow_private=True)

    if comment_form.is_valid():
        comment_form.save()
        messages.success(request, 'Comment saved')
        return redirect(reverse(success_view_name, kwargs={'uuid': datapackage.uuid}))

    else:
        messages.error(request, 'Error saving the comment. Check below for the error messages')
        context['comment_form'] = comment_form

        return render(request, failure_template_name, context)
