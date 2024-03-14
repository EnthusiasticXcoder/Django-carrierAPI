from django.urls import path
from .views import MenuListView, BlogContantView, BlogListView
from temp.AppConstants import AppConstants

urlpatterns = [
    path(AppConstants.Path.MENU, MenuListView.as_view()),
    path(AppConstants.Path.CONTENT, BlogContantView.as_view()),
    path(AppConstants.Path.LIST, BlogListView.as_view()),
]
