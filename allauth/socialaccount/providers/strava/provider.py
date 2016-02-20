from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class StravaAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get('profile')

    def get_profile_url(self):
        return 'https://www.strava.com/athletes/' + self.account.uid;

class StravaProvider(OAuth2Provider):
    id = 'strava'
    name = 'Strava'
    package = 'allauth.socialaccount.providers.strava'
    account_class = StravaAccount

    def extract_uid(self, data):
        return data['id']

    def get_user_names(self, fullname='', first_name='', last_name=''):
        # Avoid None values
        fullname = fullname or ''
        first_name = first_name or ''
        last_name = last_name or ''
        if fullname and not (first_name or last_name):
            try:
                first_name, last_name = fullname.split(' ', 1)
            except ValueError:
                first_name = first_name or fullname or ''
                last_name = last_name or ''
        fullname = fullname or ' '.join((first_name, last_name))
        return fullname.strip(), first_name.strip(), last_name.strip()

    def extract_common_fields(self, data):
       # username = data['athlete'].get('id')

        email = data.get('email', '')
        fullname, first_name, last_name = self.get_user_names(
            first_name=data.get('firstname', ''),
            last_name=data.get('lastname', '')
        )

        return dict(name=fullname,
                    first_name=first_name,
                    last_name=last_name,
                    email=email)

providers.registry.register(StravaProvider)
