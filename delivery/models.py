from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	first_name   = models.CharField(max_length=50)
	last_name 	 = models.CharField(max_length=50)
	username  	 = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=50, null=True, blank=True)

	email 	  		= models.EmailField(unique=True)
	profile_picture = models.ImageField(default="person.png", null=True, blank=True, upload_to="profile/%Y/%m/%d")
	created_at 		= models.DateTimeField(auto_now_add=True, null=True, blank=True)
	password 		= models.CharField(max_length=100, null=True, blank=True)
	# location 		= models.CharField(max_length=100)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone_number"]

	def __str__(self):
		return self.first_name+ " "+self.last_name

	class Meta:
		ordering = ['first_name', 'last_name', 'username']

class HotelType(models.Model):
	TYPES = [
		('restourant', 'Restourant'),
		('hotel', 'Hotel'),
	]
	hotel_type = models.CharField(max_length=100, choices=TYPES)

	def __str__(self):
		return self.hotel_type


class Hotel(models.Model):
	hotel_name 		= models.CharField(max_length=100)
	employee_no		= models.IntegerField(default=1)
	hotel_type 		= models.ForeignKey(HotelType, on_delete=models.SET_NULL, null=True, blank=True)
	hotel_location 	= models.CharField(max_length=100)
	stars 			= models.IntegerField(default=1)
	bio 			= models.CharField(max_length=400, null=True, blank=True)
	image 			= models.ImageField(default="hotel.jpg", upload_to="hotels", null=True, blank=True)

	def __str__(self):
		return self.hotel_name
    
	@property
	def products(self):
		return self.food_set.all()

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Food(models.Model):
    hotel 			= models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    name 			= models.CharField(max_length=200)
    descriptions 	= models.TextField(null=True, blank=True)
    price 			= models.IntegerField(default=0)
    digital 		= models.BooleanField(default=False, null=True, blank=True)
    image 			= models.ImageField(null=True, blank=True, upload_to="product/%Y/%m")
    locations 		= models.CharField(max_length=200)
    stars 			= models.IntegerField(default=1)
    type_id 		= models.IntegerField(default=1, null=True, blank=True)
    created_at 		= models.DateTimeField(auto_now_add=True)
    updated_at 		= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
	customer 		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered 	= models.DateTimeField(auto_now_add=True)
	complete 		= models.BooleanField(default=False)
	transaction_id 	= models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.customer)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	def __str__(self):
		return str(self.product)

	class Meta:
		ordering = ['-date_added']


class OrderSuccess(models.Model):
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	product 	= models.ForeignKey(Food, on_delete=models.CASCADE)
	items 		= models.ForeignKey(OrderItem, on_delete=models.CASCADE)
	ordered_at  = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.user+ " "+self.product+" "+self.items

	class Meta:
		ordering = ['-ordered_at']



