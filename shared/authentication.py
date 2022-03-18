from rest_framework import authentication
from allauth.account.auth_backends import AuthenticationBackend

from apps.user.models import User


class BearerAuthentication(authentication.TokenAuthentication):
    """
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812

    source: https://stackoverflow.com/a/51335958/7986581
    """
    keyword = 'Bearer'


class AuthenticationByDocument(AuthenticationBackend):
    def authenticate(self, request, **credentials):
        document = credentials.get("document")
        password = credentials.get("password")

        if document is None or password is None:
            return None

        try:
            user = User.objects.get(document__iexact=document)
            if self._check_password(user, password):
                return user

        except User.DoesNotExist:
            return None
