from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invite, Friends


@receiver(instance=Invite)
def create_friend(sender, instance, **kwargs):
    if instance.accepted:
        friend = Friends.objects.create(inviter = instance.inviter, target = instance.target)
        friend.save()
    if instance.accepted == False:
        instance.delete()

