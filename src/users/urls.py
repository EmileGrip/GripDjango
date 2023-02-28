from rest_framework.routers import SimpleRouter
from django.urls import path,include
from src.users.views import UserViewSet,MeView

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)

urlpatterns = [
    path("me/", MeView.as_view()),
]