

def get_subscriptions(youtube):
    subscribed_channels = dict(channels=list())
    next_page = ''

    while next_page is not None:
            response = youtube.subscriptions().list(
                part='snippet', mine='true', maxResults=50, pageToken=next_page
            )
            subscriptions_response = response.execute()

            subscribed_channels['channels'].extend({
                'title': item['snippet']['title'].strip(),
                'channel_id': item['snippet']['resourceId']['channelId'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'tags': [],
                }
                for item in subscriptions_response['items']
            )
            next_page = subscriptions_response.get('nextPageToken')

    subscribed_channels['total'] = subscriptions_response['pageInfo']['totalResults']

    return subscribed_channels
    


