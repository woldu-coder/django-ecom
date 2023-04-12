from rest_framework import serializers
from .models import Food, Hotel, User


class FoodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Food
		fields = ["id", "hotel", "name", "descriptions", "image", "price", "locations", "stars", "type_id"]


class HotelSerializer(serializers.ModelSerializer):
	products = FoodSerializer(many=True, read_only=True)
	total_size = serializers.SerializerMethodField()
	class Meta:
		model = Hotel
		fields = ["id", "hotel_name", "hotel_type", "employee_no", "hotel_location", "bio", "image", "total_size", "products"]


	def get_total_size(self, obj):
		return obj.food_set.count()

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, write_only=True, required=True, style={'input_type': 'password'})
	profile_picture = serializers.ImageField(default=True)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'profile_picture']

	def create(self, validated_data):
		user = super().create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user


	def update(self, instance, validated_data):
		user = super().update(instance, validated_data)
		try:
			user.set_password(validated_data['password'])
			user.save()
		except KeyError:
			pass
		return user



    

class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, write_only=True, required=True, style={'input_type': 'password'})
	class Meta:
		model = User
		fields = ["email", "password"]
