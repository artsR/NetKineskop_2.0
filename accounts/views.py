import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from django.shortcuts import render, redirect
from django.urls import reverse



def oauth_authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    print('FLOW :', flow)
    flow.redirect_uri = reverse('oauth_callback')
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true'
    )
    print('AUTHORIZATION ', authorization_url)
    print('STATE ', state)
    request.session['state'] = state

    return redirect(authorization_url)


def oauth_callback():
    state = request.session['state']
    print('STATE 2: ', state)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = reverse('oauth_callback')

    authorization_response = request.url
    print('AUTHORIZATION RES: ', authorization_response)
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    request.session['credentials'] = credentials_to_dict(credentials)
    print('CREDENTIALS: ', request.session['credentials'])
    return redirect(reverse('netkineskop:home'))


def oauth_revoke():
    if 'credentials' not in request.session:
        return (
            f'You need to <a href="/authorize">authorize</a> '
            f'before testing the code to revoke credentials.'
        )

    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

    revoke = requests.post(
        'https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return 'Credentials successfully revoked.'
    else:
        return 'An error occured.'


def clear_credentials():
    if 'credentials' in request.session:
        del request.session['credentials']
    return 'Credentials have been cleared.<br><br>'


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
