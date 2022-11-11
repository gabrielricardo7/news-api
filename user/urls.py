from django.urls import path
from .views import LoginView, SignUpView, UserView
from user.views import show_ip_address

urlpatterns = [
    path('users/', UserView.as_view()),
    path('user/signup/', SignUpView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('user/ip/', show_ip_address),
]
