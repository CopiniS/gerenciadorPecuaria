from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('singup', RegisterView.as_view()),
    path('login', LoginView.as_view()),
]