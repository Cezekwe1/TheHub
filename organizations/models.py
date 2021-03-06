from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='Membership')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  related_name="creator")
    


class Membership(models.Model):
    administrator = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    organization = models.ForeignKey( Organization , on_delete = models.CASCADE)


    class Meta:
        unique_together = ['organization', 'user']

    def make_admin(self,admin):
        m = Membership.objects.filter(user=admin,organization=self.organization)
        if not not m:
            if m[0].administrator:
                if not self.administrator:
                    self.administrator = True
                    self.save()
                    return 
                else:
                    raise Exception("Already an Administrator")
            raise Exception("Person requesting change is not an Admistrator")
        raise Exception("Member does not exist")


class OrgInvite(models.Model):
    inviter = models.ForeignKey(User,on_delete = models.CASCADE, related_name='orginviteinviter')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    target = models.ForeignKey(User, on_delete= models.CASCADE, related_name='orginvitetarget')
    accepted = models.NullBooleanField(default = None)

    
    class Meta:
        unique_together = ['organization', 'target']

    def is_admin(self, person, organization):
        m = Membership.objects.filter(user=person, organization=organization)
        
        if not not m:
            if m[0].administrator:
                return True
        return False

    
    def save(self, *args, **kwargs):

        if self.is_admin(self.inviter, self.organization):
            super().save(*args, **kwargs)
        else:
            raise Exception("This person is not an administrator")
