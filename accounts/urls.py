from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', login, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile')
]
