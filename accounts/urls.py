from django.urls import path
from .views import LoginPageView, LoginFormView, LogoutView

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('login-form/', LoginFormView.as_view(), name='login_form'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
