from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
import django.forms

import users.models

__all__ = []


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields[User.email.field.name].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        ]


class ProfileChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["visited_countries_count"].required = False
        self.fields["homeland_country"].required = False
        self.fields["roamway_link"].required = False
        self.fields["twitter_link"].required = False
        self.fields["instagram_link"].required = False
        self.fields["facebook_link"].required = False
        self.fields["image"].widget.attrs["type"] = "file"
        self.fields["visited_countries_count"].widget.attrs["disabled"] = True

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.image.field.name,
            users.models.Profile.visited_countries_count.field.name,
            users.models.Profile.homeland_country.field.name,
            users.models.Profile.roamway_link.field.name,
            users.models.Profile.twitter_link.field.name,
            users.models.Profile.instagram_link.field.name,
            users.models.Profile.facebook_link.field.name,
        )


class UserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        model = User
        fields = [
            User.username.field.name,
            User.email.field.name,
        ]


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        return (
            [single_file_clean(d, initial) for d in data]
            if isinstance(data, (list, tuple))
            else single_file_clean(data, initial)
        )


class PhotosFileForm(django.forms.Form):
    files = MultipleFileField(label="Файлы", required=True)
