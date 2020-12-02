import google.oauth2.credentials
import googleapiclient.discovery

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import yt_services
from .models import Tag, Channel, ChannelTag
from .forms import TagForm
from .permissions import TagUserPermission
from accounts.views import credentials_to_dict



def home(request):
    return render(request, 'netkineskop/home.html')


class TagView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'netkineskop/user_tags.html'
    context_object_name = 'user_tags'
    paginate_by = 15

    def get_queryset(self):
        current_user = self.request.user
        return current_user.tags.all()


class AddTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'netkineskop/add_tag.html'
    success_url = '/tags/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class DeleteTagView(TagUserPermission, DeleteView):
    model = Tag
    success_url = '/tags/'


class UpdateTagView(TagUserPermission, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'netkineskop/edit_tag.html'
    success_url = '/tags/'


class DetailTagView(TagUserPermission, DetailView):
    model = Tag
    template_name ='netkineskop/detail_tag.html'


def subscriptions(request):
    if 'credentials' not in request.session:
        return redirect('oauth_authorize')

    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])
    youtube = googleapiclient.discovery.build(
        settings.API_SERVICE_NAME, settings.API_VERSION, credentials=credentials
    )
    request.session['credentials'] = credentials_to_dict(credentials)

    subscribed_channels = yt_services.get_subscriptions(youtube)

    context = dict(subscriptions=subscribed_channels)
    return render(request, 'netkineskop/subscriptions.html', context)


def videos(request):
    if 'credentials' not in request.session:
        return redirect('oauth_authorize')

    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])
    youtube = googleapiclient.discovery.build(
        settings.API_SERVICE_NAME, settings.API_VERSION, credentials=credentials
    )
    response = youtube.subscriptions().list(part='snippet', mine='true')
    request.session['credentials'] = credentials_to_dict(credentials)
    subscribed_videos = response.execute()
    imgs = [
        v for k, v in subscribed_videos.items()
    ]
    channel_ids = [
        img['snippet']['resourceId']['channelId']
        for img in imgs[4]
    ]

    response_videos = youtube.channels().list(
        part='contentDetails',
        id=','.join(id for id in channel_ids)
    )
    videos = response_videos.execute()
    channels = [{
        'id': video['id'],
        'uploads': video['contentDetails']['relatedPlaylists']['uploads']
        }
        for video in videos['items']
    ]
    from pprint import pprint
    # print(f'Channels ######## : {channels}')
    uploads = list()
    for channel in channels:
        response_vids = youtube.playlistItems().list(
            part='snippet, contentDetails',
            playlistId=channel['uploads'],
            maxResults=50,
            pageToken=None
        )
        uploads.append(response_vids.execute())

    videos_all = list()
    for vids in uploads:
        for vid in vids['items']:
            videos_all.append({
                'channel_id': vid['snippet']['channelId'],
                'channel_title': vid['snippet']['channelTitle'],
                'published_at': vid['snippet']['publishedAt'],
                'thumbnail_url': vid['snippet']['thumbnails']['medium']['url'],
                'video_title': vid['snippet']['title'],
                'video_url': vid['snippet']['resourceId']['videoId']
        })
    # pprint(videos_all)
    context = dict(imgs=imgs, videos=videos_all)
    return render(request, 'netkineskop/videos.html', context)

