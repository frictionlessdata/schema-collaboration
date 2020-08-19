from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms

from core.models import Person


class PersonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-6'),
                css_class='row'
            ),
            FormActions(
                Submit('save', 'Save'),

            )
        )

    class Meta:
        model = Person
        fields = ['name']
