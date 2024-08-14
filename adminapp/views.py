from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from user.models import Order, User, OrderItem
from .models import Food, Category
from .forms import FoodForm, CategoryForm



class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    form_class = FoodForm
    template_name = 'adminapp/food_form.html'
    permission_required = 'user.add_food'
    success_url = reverse_lazy('food_list')


class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    form_class = FoodForm
    template_name = 'adminapp/food_form.html'
    permission_required = 'user.change_food'
    success_url = reverse_lazy('food_list')

class FoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'adminapp/food_confirm_delete.html'
    permission_required = 'user.delete_food'
    success_url = reverse_lazy('food_list')

class FoodListView(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'adminapp/food_list.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class UserOrderHistoryView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'adminapp/user_order_history.html'
    context_object_name = 'orders'
    permission_required = 'user.view_order'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Order.objects.filter(user_id=user_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.kwargs['user_id'])
        user_orders = context['orders']
        order_items = OrderItem.objects.filter(order__in=user_orders).select_related('product')
        print(f"Order Items: {order_items}")
        context['order_items'] = order_items
        return context



class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'adminapp/category_form.html'
    permission_required = 'user.add_category'
    success_url = reverse_lazy('food_list')


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'adminapp/category_form.html'
    permission_required = 'user.change_category'
    success_url = reverse_lazy('food_list')
class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'adminapp/category_confirm_delete.html'
    permission_required = 'user.delete_category'
    success_url = reverse_lazy('food_list')




class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'adminapp/users_full_list.html'
    context_object_name = 'users'