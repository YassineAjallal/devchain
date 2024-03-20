from django.urls import path
from . import views


urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='authenticate'),
    path('home', views.Home.as_view(), name='home'),
    path('request', views.Request.as_view(), name='request'),
    path('verify', views.Verify.as_view(), name='verify'),
]