from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from final_project.web.models import Profile

UserModel = get_user_model()


# @receiver(signals.post_save, sender=UserModel)
# def create_profile_on_user_creation(instance, created, *args, **kwargs):
#     if not created:
#         return
#
#     Profile.objects.create(
#         first_name=instance.profile.first_name,
#         last_name=instance.profile.last_name,
#         age=instance.profile.age,
#         gender=instance.profile.gender,
#         user_id=instance.pk
#     )


@receiver(signals.post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(signals.post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()