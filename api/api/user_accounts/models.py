from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from api.common.models import SoftDeleteModel, TimestampedModel


class UserProfile(SoftDeleteModel, TimestampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", primary_key=True
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name or self.user.username}'s Profile"

    def soft_delete(self):
        self.user.is_active = False
        self.user.save()
        super().soft_delete()

    def restore(self):
        self.user.is_active = True
        self.user.save()
        super().restore()

    class Meta:
        db_table = "user_profiles"
        verbose_name = "User Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
