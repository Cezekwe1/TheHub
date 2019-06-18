from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invite, Friends, Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=Invite)
def create_friend(sender,instance, **kwargs):
    if instance.accepted:
        friend = Friends.objects.create(inviter = instance.inviter, target = instance.target)
        friend.save()
        instance.delete()
    if instance.accepted == False:
        instance.delete()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()

