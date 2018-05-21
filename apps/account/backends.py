from social.backends.google import BaseGoogleOAuth2API
from social.backends.oauth import BaseOAuth2

__author__ = 'richard'


class GoogleOAuth2(BaseGoogleOAuth2API, BaseOAuth2):
    """Google OAuth2 authentication backend"""
    name = 'google-oauth2'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    # The order of the default scope is important
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
    DEPRECATED_DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/plus.me'
    ]
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        # if self.setting('USE_DEPRECATED_API', False):
        #     url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        # else:
        #     url = 'https://www.googleapis.com/plus/v1/people/me'
        url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        return self.get_json(url, params={
            'id_token': access_token,
            'alt': 'json'
        })
