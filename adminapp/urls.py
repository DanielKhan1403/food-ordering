from django.urls import path
from .views import *

urlpatterns = [
    path('food/create/', FoodCreateView.as_view(), name='food_create'),
    path('food/<int:pk>/update/', FoodUpdateView.as_view(), name='food_update'),
    path('food/<int:pk>/delete/', FoodDeleteView.as_view(), name='food_delete'),
    path('food/', FoodListView.as_view(), name='food_list'),

    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:user_id>/orders/', UserOrderHistoryView.as_view(), name='user_order_history'),

]
