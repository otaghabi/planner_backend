from django.urls import path

from api.views.accounts_api_views import *

app_name = 'api'
urlpatterns = []

accounts_urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]

urlpatterns += accounts_urlpatterns
