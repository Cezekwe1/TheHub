from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invite, Friends


@receiver(post_save, sender=Invite)
def create_friend(sender,instance, **kwargs):
    if instance.accepted:
        friend = Friends.objects.create(inviter = instance.inviter, target = instance.target)
        friend.save()
        instance.delete()
    if instance.accepted == False:
        instance.delete()

