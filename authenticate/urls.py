from django.urls import path
from .views import UserViewSet, RegesterView, LoginView
from scrapper.AppConstants import AppConstants

urlpatterns = [
    path(AppConstants.Path.BLANK, UserViewSet.as_view()),
    path(AppConstants.Path.REGISTER, RegesterView.as_view()),
    path(AppConstants.Path.LOGIN, LoginView.as_view()),
]
