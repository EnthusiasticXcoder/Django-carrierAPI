from django.urls import path
from .views import UserViewSet, RegesterView, LoginView

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('register', RegesterView.as_view()),
    path('login', LoginView.as_view()),
]
