from django.contrib import admin
from .models import Channel, ChannelMembership, Group, GroupMembership, Message

admin.site.register(Channel)
admin.site.register(ChannelMembership)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Message)
