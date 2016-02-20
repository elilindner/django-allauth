from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
import requests

from .provider import StravaProvider


class StravaAdapter(OAuth2Adapter):
    provider_id = StravaProvider.id
    access_token_url = 'https://www.strava.com/oauth/token'
    authorize_url = 'https://www.strava.com/oauth/authorize'
    profile_url = 'https://www.strava.com/api/v3/athlete'
    redirect_uri_protocol = 'https'

    def complete_login(self, request, app, token, **kwargs):
        extra_data = requests.get(self.profile_url, params={
            'access_token': token.token
        })

        # This only here because of weird response from the test suite
        if isinstance(extra_data, list):
            extra_data = extra_data[0]

        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )


oauth2_login = OAuth2LoginView.adapter_view(StravaAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(StravaAdapter)
