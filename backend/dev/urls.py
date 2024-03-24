from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('authenticate', views.Authenticate.as_view(), name='authenticate'),
    path('set_name', views.SetName.as_view(), name='set name'),
    path('create', views.CreateArticle.as_view(), name='create'),
    path('update/<int:id>', views.UpdateArticle.as_view(), name='update'),
    path('delete', views.DeleteArticle.as_view(), name='delete'),
    path('article', views.ListUserArticles.as_view(), name='user articles'),
    path('article/<int:id>', views.ArticleDetails.as_view(), name='article details'),
    path('request', views.Request.as_view(), name='request'),
    path('verify', views.Verify.as_view(), name='verify'),
]