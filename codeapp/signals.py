from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserStats

# Create stats when a user is first created
@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)

# Ensure stats always exist
@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    UserStats.objects.get_or_create(user=instance)
