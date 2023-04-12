from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *



class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']


class FoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ["hotel", "name", "descriptions", "image", "price", "locations", "type_id"]


class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = ["hotel_name", "hotel_type", "employee_no", "hotel_location", "bio", "image"]
