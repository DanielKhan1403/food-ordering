
from django.views import View
from django.views.generic import ListView
from .models import *
from django.contrib.auth.views import  LogoutView


from django.views.generic import TemplateView, CreateView

from user.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


from .forms import UserEditForm

# Create your views here.

class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'auth/edit_profile.html', {'form': form})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


# user interface Daniel not chatgpt
class IndexView(ListView):
    model = Food
    context_object_name = 'foods'

    def get_template_names(self):
        if self.request.user.groups.filter(name='managers').exists():
            return ['adminapp/food_list.html']  # Шаблон для администраторов
        return ['user/index.html']  # Шаблон для обычных пользователей

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            return Food.objects.filter(category__slug=category_slug)
        return Food.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# cart function

class AddToCartView(View):
    def get(self, request, food_id):
        food = Food.objects.get(id=food_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=food)

        if created:
            cart_item.price = food.price
        else:
            cart_item.quantity += 1
            cart_item.price = cart_item.quantity * food.price

        cart_item.save()


        cart_items = CartItem.objects.filter(user=request.user)
        request.session['cart_items'] = sum(item.quantity for item in cart_items)
        request.session['cart_total'] = float(sum(item.price for item in cart_items))  # Преобразование в float

        return redirect('index')

class CartView(TemplateView):
    template_name = 'user/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItem.objects.filter(user=self.request.user)
        context['total_price'] = sum(item.price for item in context['cart_items'])
        return context


class CartItemUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.price = cart_item.quantity * cart_item.product.price
            cart_item.save()
        else:
            cart_item.delete()


        cart_items = CartItem.objects.filter(user=request.user)
        request.session['cart_items'] = sum(item.quantity for item in cart_items)
        request.session['cart_total'] = float(sum(item.price for item in cart_items))

        return redirect('cart')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):

        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.price for item in cart_items)
        return render(request, 'user/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

    def post(self, request, *args, **kwargs):

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            return redirect('cart')

        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)
        cart_items.delete()

        return redirect('order_confirmation', order_id=order.id)


class OrderConfirmationView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)
        return render(request, 'user/order_confirmation.html', {'order': order})

class OrderHistoryView(ListView):
    model = Order
    template_name = 'user/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')