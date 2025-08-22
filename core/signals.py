from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.usuario.user import User
from core.utils import sync_user_groups  # ou onde você colocou

@receiver(post_save, sender=User)
def update_user_groups(sender, instance, **kwargs):
    sync_user_groups(instance)
