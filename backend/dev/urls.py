from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('authenticate', views.Authenticate.as_view(), name='authenticate'),
    path('set_name', views.SetName.as_view(), name='set name'),
    path('create', views.CreateArticle.as_view(), name='create'),
    path('request', views.Request.as_view(), name='request'),
    path('verify', views.Verify.as_view(), name='verify'),
]