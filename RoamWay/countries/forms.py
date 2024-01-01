import django.forms

import users.models

__all__ = ["TaskCreateForm", "TextForm"]


class TaskCreateForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["homeland_country"].required = True

    class Meta:
        model = users.models.Profile
        fields = (users.models.Profile.homeland_country.field.name,)


class TextForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["text"].required = True

    text = django.forms.CharField()
