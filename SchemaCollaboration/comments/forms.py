from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.forms import ModelForm

from core.models import Datapackage
from .models import Comment


class CommentForm(ModelForm):
    def __init__(self, *args, datapackage_id, person, **kwargs):
        form_action_url = kwargs.pop('form_action_url', None)
        allow_private = kwargs.pop('allow_private', False)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['text'].widget.attrs = {'rows': 3}

        self.fields['private'].help_text = 'Enable if this comment is going to be visible only by you'

        if person:
            self.fields['author'].initial = person
            self.fields['author'].disabled = True
        else:
            self.fields['author'].queryset = Datapackage.objects.get(id=datapackage_id). \
                collaborators.order_by('full_name')
            self.fields['author'].help_text = 'Please select who you are'

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
                hidden=person is not None
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

    class Meta:
        model = Comment
        fields = ['datapackage', 'author', 'text', 'private']
