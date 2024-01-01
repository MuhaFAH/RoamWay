from django.contrib.auth.base_user import BaseUserManager

__all__ = []


class UserManager(BaseUserManager):
    def active(self):
        return (
            self.get_queryset()
            .filter(
                is_active=True,
            )
            .select_related("profile")
            .only("username")
        )
