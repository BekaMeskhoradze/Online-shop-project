from django.urls import path
from .views import LoginRegisterView
from django.contrib.auth.views import LogoutView

app_name= 'accounts'

urlpatterns = [
    path('accounts/', LoginRegisterView.as_view(), name='login_register'),
    path('accounts/logout/', LogoutView.as_view(next_page='core:index'), name='logout'),
]