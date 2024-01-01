from django.contrib.auth.backends import ModelBackend

import users.models

__all__ = []


class UsernameAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            get_user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None
        else:
            if get_user.check_password(password) and get_user.is_active:
                if not hasattr(get_user, "profile"):
                    users.models.Profile.objects.create(
                        user=get_user,
                    )
                get_user.profile.save()
                return get_user
