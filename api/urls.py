from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from api.views.accounts_api_views import *

app_name = 'api'
urlpatterns = []

accounts_urlpatterns = [
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/register/advisor/', CreateAdvisorView.as_view(), name='advisor'),
    path('auth/register/student/', CreateStudentView.as_view(), name='student'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/login/refresh/', RefreshView.as_view(), name='refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='logout'),
    # student urls
    path('student/advisors/', AdvisorsListView.as_view(), name='advisors_list'),

    # advisor urls
    path('advisor/students/', StudentListView.as_view(), name='student_list')
]

urlpatterns += accounts_urlpatterns
