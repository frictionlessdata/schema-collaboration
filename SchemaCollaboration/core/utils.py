from crispy_forms.layout import HTML


def cancel_button(url):
    return HTML(f'<a class="btn btn-danger" href="{url}">Cancel</a>')
