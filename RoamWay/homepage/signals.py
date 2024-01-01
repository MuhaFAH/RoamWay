from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import UserUploadedFiles

__all__ = ["delete_related_files"]


@receiver(post_delete, sender=UserUploadedFiles)
def delete_related_files(sender, instance, **kwargs):
    if sender.__name__ == UserUploadedFiles.__name__:
        file_path = Path(settings.MEDIA_ROOT) / str(instance.file)

        if file_path.exists():
            file_path.unlink()
