from django.urls import path
from .views import UserViewSet, AuthView

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('auth', AuthView.as_view()),
]
