from django.urls import path
from .views import MenuListView, BlogContantView, BlogListView

urlpatterns = [
    path('menu', MenuListView.as_view()),
    path('contant', BlogContantView.as_view()),
    path('list', BlogListView.as_view()),
]
