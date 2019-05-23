from .models import Organization, Membership, OrgInvite
from messages.models import Channel
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Organization)
def create_org_admin(sender, instance, created, **kwargs):
    if created:
        m = Membership.objects.create(user=instance.creator, organization=instance, administrator=True)
        m.save()

@receiver(post_save, sender=OrgInvite)
def create_org_member(sender, instance, **kwargs):
        if instance.accepted:
                m = Membership.objects.create(user=instance.target, organization= instance.organization)

@receiver(post_save, sender=Organization)
def create_default_channels(sender, instance, created, **kwargs):
        if created:
                c1 = Channel(name= "general", organization = instance, description="general work related topics")
                c2 = Channel(name= "water-cooler", organization = instance, description="discuss how good game of thrones is")
                c1.save()
                c2.save()
                for member in instance.members.all():
                        c1.members.add(member)
                        c2.members.add(member)

@receiver(post_save, sender=Membership)
def add_member_to_default_channels(sender, instance, created, **kwargs):
        if created:
                c1 = Channel.objects.filter(name="general",organization=instance.organization) 
                c2 = Channel.objects.filter(name="water-cooler",organization=instance.organization)
                if c1:
                        c1[0].members.add(instance.user)
                if c2:
                        c2[0].members.add(instance.user) 