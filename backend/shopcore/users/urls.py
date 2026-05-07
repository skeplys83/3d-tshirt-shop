from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.InfoView.as_view(), name='info'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.UserListCreateView.as_view(), name='user-list'),
    path('<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
]
