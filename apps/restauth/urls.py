from django.urls import include, path

from . import views

app_name = 'auth'

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='rest_login'),
    path('password/reset/', views.PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', views.LogoutView.as_view(), name='rest_logout'),
    path('user/', views.UserDetailsView.as_view(), name='rest_user_details'),
    path('user/delete/', views.UserDestroyView.as_view(), name='rest_user_destroy'),
    path('password/change/', views.PasswordChangeView.as_view(), name='rest_password_change'),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
