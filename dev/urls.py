from django.urls import path
from . import views


urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('request', views.Request.as_view(), name='request'),
    path('verify', views.Verify.as_view(), name='verify'),
]