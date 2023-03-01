from rest_framework.routers import SimpleRouter
from django.urls import path,include
from src.users.views import UserViewSet,MeView,SkillViewset

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)
users_router.register(r'skills', SkillViewset)


urlpatterns = [
    path("me/", MeView.as_view()),
]