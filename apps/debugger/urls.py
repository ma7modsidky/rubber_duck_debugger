from django.urls import path
from .views import debugger_home

urlpatterns = [
    path('', debugger_home, name='home'),
    path('<int:log_id>/', debugger_home, name='log_detail'), # New dynamic route
]