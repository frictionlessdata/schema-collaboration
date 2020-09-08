from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from comments.forms import CommentForm
from core.models import Person


class AddComment(TemplateView):
    template_name = 'comments/comment-added.html'

    def get(self, request, *args, **kwargs):
        print('here GET')

    def post(self, request, *args, **kwargs):
        datapackage_id = self.kwargs['datapackage_id']
        person = Person.objects.get(user=self.request.user)
        comment_form = CommentForm(request.POST, person=person, datapackage_id=datapackage_id)

        if comment_form.is_valid():
            comment_form.save()

            return redirect(reverse('management:datapackage-detail', kwargs={'pk': datapackage_id}))
        else:
            # TODO handle this
            assert False