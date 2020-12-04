from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models



class Tag(models.Model):
    user = models.ForeignKey(
        User, related_name='tags', blank=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=32)
    color = models.CharField(
        max_length=7,
        blank=True,
        default='#cccccc',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$')]
    )

    def __str__(self):
        return f'{self.name}'


class Channel(models.Model):
    user = models.ForeignKey(
        User, related_name='channels', blank=False, on_delete=models.CASCADE
    )
    yt_channel_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128, blank=True, default='<name placeholder>')

    tags = models.ManyToManyField(Tag, related_name='channels', through='ChannelTag')

    def __str__(self):
        return f'{self.name}'


class ChannelTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tag} : {self.channel}'

    class Meta:
        unique_together = ('tag', 'channel')
