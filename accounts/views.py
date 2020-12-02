import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow


from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse



def register(request):
    """Register new User."""
    if request.user.is_authenticated:
        return redirect('netkineskop:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'New account added successfully. Now you can Sign In')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = dict(form=form, active='register')
    return render(request, 'accounts/auth.html', context)


def oauth_authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRET_FILE, scopes=settings.SCOPES
    )
    print('FLOW :', flow)
    # flow.redirect_uri = request.build_absolute_uri(reverse("oauth_callback"))
    flow.redirect_uri = 'http://127.0.0.1:8000/callback/'
    print('URI~~~1~~~', flow.redirect_uri)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true'
    )
    print('AUTHORIZATION ', authorization_url)
    print('STATE ', state)
    request.session['state'] = state

    return redirect(authorization_url)


def oauth_callback(request):
    state = request.session['state']
    print('STATE 2: ', state)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRET_FILE, scopes=settings.SCOPES, state=state
    )
    # flow.redirect_uri = request.build_absolute_uri(reverse("oauth_callback"))
    flow.redirect_uri = 'http://127.0.0.1:8000/callback/'
    print('URI~~~2~~~', flow.redirect_uri)
    authorization_response = request.build_absolute_uri()
    print('AUTHORIZATION RES: ', authorization_response)
    flow.fetch_token(authorization_response=authorization_response)
    print('CONTROL 1')
    credentials = flow.credentials
    print('CONTROL 2')
    request.session['credentials'] = credentials_to_dict(credentials)
    print('CREDENTIALS: ', request.session['credentials'])
    return redirect(reverse('netkineskop:home'))


def oauth_revoke(request):
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


def clear_credentials(request):
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
