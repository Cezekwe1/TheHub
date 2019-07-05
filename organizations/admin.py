from django.contrib import admin
from .models import Organization, Membership, OrgInvite
# Register your models here.
admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(OrgInvite)