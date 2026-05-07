from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:id>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('user/<str:user_id>/', views.OrdersByUserIdView.as_view(), name='orders-by-user'),
]
