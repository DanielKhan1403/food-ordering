from django import forms
from .models import Food, Category

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'price', 'category', 'photo']  # Укажите поля модели, которые хотите использовать в форме

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Укажите поля модели, которые хотите использовать в форме
        # теперь надо сделать админку и все