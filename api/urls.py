from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from api.views.accounts_api_views import *

app_name = 'api'
urlpatterns = []

accounts_urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/advisor/', CreateAdvisorView.as_view(), name='advisor'),
    path('register/student/', CreateStudentView.as_view(), name='student'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]

urlpatterns += accounts_urlpatterns
