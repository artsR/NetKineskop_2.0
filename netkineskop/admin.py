from django.contrib import admin

from .models import Tag, Channel, ChannelTag



admin.site.register(Tag)
admin.site.register(Channel)
admin.site.register(ChannelTag)
