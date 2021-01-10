from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, forms

from core.models import Datapackage, Person
from .models import Comment


class CommentForm(ModelForm):
    def __init__(self, *args, datapackage_id, logged_user, **kwargs):
        form_action_url = kwargs.pop('form_action_url', None)
        allow_private = kwargs.pop('allow_private', False)

        super().__init__(*args, **kwargs)

        self._logged_user = logged_user

        self.helper = FormHelper(self)

        self.fields['text'].widget.attrs = {'rows': 3}

        self.fields['private'].help_text = 'Enable if this comment should only be visible to data managers'

        fields_author = self.fields['author']

        if logged_user is None or logged_user.is_anonymous:
            logged_person = None
        else:
            try:
                logged_person = Person.objects.get(user=logged_user)
            except ObjectDoesNotExist:
                logged_person = None

        if logged_person:
            fields_author.initial = logged_person
            fields_author.disabled = True
        else:
            queryset = Datapackage.objects.get(id=datapackage_id). \
                collaborators. \
                filter(user__isnull=True). \
                order_by('full_name')
            fields_author.queryset = queryset

            if queryset.count() == 1:
                fields_author.initial = queryset[0]
                fields_author.disabled = True

            fields_author.help_text = 'Please select who you are'

        self.fields['private'].disabled = not allow_private

        self.fields['datapackage'].initial = Datapackage.objects.get(id=datapackage_id)
        self.fields['datapackage'].disabled = True

        self.helper.layout = Layout(
            Div(
                Div('text', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('private', css_class='col-6'),
                css_class='row',
                hidden=not allow_private
            ),
            Div(
                Div('author', css_class='col-6'),
                css_class='row',
                hidden=logged_person is not None
            ),
            Div(
                Div('datapackage', css_class='col-6'),
                css_class='row',
                hidden=True
            ),

            FormActions(
                Submit('save', 'Add Comment'),
            )
        )

        if form_action_url:
            self.helper.form_action = form_action_url

    def clean(self):
        super().clean()

        if self._logged_user is None and 'author' in self.cleaned_data and self.cleaned_data['author'].user_id:
            # User is not logged_in but tries to add a comment as a logged-in user. This is not allowed
            # (it should not appear in the form, might be trying to inject commments as a 'data-manager'?)
            raise forms.ValidationError({'author': 'Author not allowed'})

    class Meta:
        model = Comment
        fields = ['datapackage', 'author', 'text', 'private']
