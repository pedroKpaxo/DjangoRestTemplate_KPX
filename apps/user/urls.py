from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('technical', views.TechnicalUserViewSet, basename='technical-user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
