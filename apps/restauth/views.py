from dj_rest_auth import views as dj_rest_auth_views
from rest_framework.generics import DestroyAPIView
from apps.user.serializers import BaseUserSerializer, ExecutiveUserSerializer, TechnicalUserSerializer

from shared.authentication import BearerAuthentication


class LoginView(dj_rest_auth_views.LoginView):
    # Prevents clash between session and token authentication
    authentication_classes = (BearerAuthentication,)


class PasswordResetView(dj_rest_auth_views.PasswordResetView):
    authentication_classes = (BearerAuthentication,)


class PasswordResetConfirmView(dj_rest_auth_views.PasswordResetConfirmView):
    authentication_classes = (BearerAuthentication,)


class LogoutView(dj_rest_auth_views.LogoutView):
    pass


class UserDetailsView(dj_rest_auth_views.UserDetailsView):
    def get_serializer_class(self):
        user = self.get_object()
        if user.is_civil:
            return ExecutiveUserSerializer
        elif user.is_technical:
            return TechnicalUserSerializer
        else:
            return BaseUserSerializer


class UserDestroyView(DestroyAPIView):
    """Destroy (delete) logged in user."""
    def get_object(self):
        return self.request.user


class PasswordChangeView(dj_rest_auth_views.PasswordChangeView):
    pass
