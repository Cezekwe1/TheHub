from .models import Organization, Membership
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Organization)
def create_org_admin(sender, instance, created, **kwargs):
    if created:
        m = Membership.objects.create(user=instance.creator, organization=instance, administrator=True)
        m.save()


