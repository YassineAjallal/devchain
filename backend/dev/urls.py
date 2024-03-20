from django.urls import path
from . import views


urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='authenticate'),
    path('create_form', views.CreateArticle.as_view(), name='create form'),
    path('home', views.Home.as_view(), name='home'),
    path('request', views.Request.as_view(), name='request'),
    path('verify', views.Verify.as_view(), name='verify'),
]