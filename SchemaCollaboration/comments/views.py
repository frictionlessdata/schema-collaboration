from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from comments.forms import CommentForm
from core.models import Person, Datapackage


def process_post_add_comment(request, context,
                             datapackage, force_anonymous_user,
                             success_view_name,
                             failure_template_name):
    if force_anonymous_user:
        person = None
    else:
        person = Person.objects.get(user=request.user)

    comment_form = CommentForm(request.POST, datapackage_id=datapackage.id, person=person)

    if comment_form.is_valid():
        comment_form.save()
        messages.success(request, 'Comment saved')
        return redirect(reverse(success_view_name, kwargs={'uuid': datapackage.uuid}))

    else:
        messages.error(request, 'Error saving the comment. Check below for the error messages')
        context['comment_form'] = comment_form

        return render(request, failure_template_name, context)


class AbstractAddCommentView(TemplateView):
    def __init__(self, force_anonymous_user, success_view_name, failure_url, *args, **kwargs):
        self._force_anonymous_user = force_anonymous_user
        self._success_view_name = success_view_name
        self._failure_url = failure_url

        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        datapackage = Datapackage.objects.get(uuid=kwargs['uuid'])

        if self._force_anonymous_user:
            person = None
        else:
            person = Person.objects.get(user=self.request.user)

        comment_form = CommentForm(request.POST, datapackage_id=datapackage.id, person=person)

        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, 'Comment saved')
            return redirect(reverse(self._success_view_name, kwargs={'uuid': datapackage.uuid}))

        else:
            messages.error(request, 'Error saving the comment. Check below for the error messages')
            return redirect()
            # TODO handle this
            assert False
