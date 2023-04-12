from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import permission_required, login_required
import json, geocoder, folium
import datetime
from django.http import JsonResponse
from rest_framework import generics, mixins, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .forms import *
from .decorators import *
from .serializers import *
from .utils import *
from .locations import *
from .models import Food, User, Order, OrderItem, Hotel

# @login_required(login_url='login')
def home_page(request, *args, **kwargs):  #  {'lat': 9.6213626, 'lng': 41.8409431}  -> Main Library
	products = Food.objects.all()[:3]
	map = userlocation([9.6213626, 41.8409431])

	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"products":products,
		"groups":group,
		"cartItems": cartItems,
		"map": map
	}
	return render(request, "app/home.html", context)

# GET Started
@login_required(login_url='login')
def stores(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	products = Food.objects.filter(
		Q(price__icontains=q)|
		Q(name__icontains=q) |
		Q(hotel__hotel_name__icontains=q)
		)
	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"products":products,
		"groups":group,
		"cartItems": cartItems,
		"map": map
	} 
	return render(request, "app/store.html", context)


def about_page(request):
	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"groups":group,
		"cartItems": cartItems,
		"map": map
	} 
	return render(request, "app/about.html", context)


def location_handler(request):
	location = json.loads(request.body)
	latitude = location['lat']
	longitude = location['lng']
	return redirect('home')

@authenticated_user
def login_page(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')

		else:
			messages.info(request, "Please enter your password or email address correctly!")
			return HttpResponseRedirect('/home')

	return render(request, "register/login.html", {})

def logout_page(request):
	logout(request)
	return redirect('home')


def signup_page(request):
	page = "signup"
	if request.method == "POST":
		fname = request.POST.get('firstname')
		lname = request.POST.get('lastname')
		uname = request.POST.get('username')
		phone = request.POST.get('phonenumber')
		email = request.POST.get('email')
		pass1 = request.POST.get('password')
		pass2 = request.POST.get('password2')
		if pass1 == pass2:
			user = User.objects.get_or_create(first_name=fname, last_name=lname,
					username=uname,
					phone_number = phone,
					email=email,
					password= make_password(pass1)
				)
			if user is not None:
				print("user created successfully")
				return redirect('home')

	context = {
		"page":page
	}
	return render(request, "register/sign-up.html", context)


@login_required(login_url="login")
@allowed_user(allowed_group=["Admin", "Manager"])
def add_product(request):
	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	if request.method == "POST":
		form = FoodForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save()
			return redirect('add_product')
	else:
		form = FoodForm()

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"groups":group,
		"form":form,
		"cartItems":cartItems,
	} 
	return render(request, "app/product.html", context)


def access_denied(request):
	return render(request, "error/error.html", {})

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user
	product = Food.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def cart_list(request):
	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"groups":group,
		"items":items,
		"order":order,
		"cartItems":cartItems
	}
	return render(request, "app/cart-list.html", context)


def checkout(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('checkout')
		else:
			messages.error(request, "Email or password wrong. Please enter correctly!")
			# print("Error Password!")
			return HttpResponseRedirect('/checkout')

	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {
		"groups":group,
		"items":items,
		"order":order,
		"cartItems":cartItems
	}
	return render(request, "app/checkout.html", context)



# SENDING EMAIL FOR THE CLIENT
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def message(request):
	
	template = render_to_string('app/email_send.html', {"name":request.user})

	if request.method == 'POST':
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		idea  = request.POST.get('message')

		mail = EmailMessage(
				f"Hello {email} !!",
				template,
				settings.EMAIL_HOST_USER,
				[email],
			)
		mail.fail_silently = False
		mail.send()
		return render(request, 'success/contact.html', {})
	else:
		return render(request, 'app/home.html', {})


def payment(request):
	group = []
	for i in request.user.groups.all():
		group.append(i.name)

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		"groups":group,
		"items":items,
		"order":order,
		"cartItems":cartItems
	}
	return render(request, "app/home.html", context)


def payment_method(request, args):
	method = ''
	if args == '1':
		method = 'Cash'
	elif args == '2':
		method = 'Telebirr'
	elif args == '3':
		method = 'CBE'
	# print("You are going to pay with = ",method)
	group = []
	for i in request.user.groups.all():
		group.append(i.name)
	data = cartData(request)
	response = render(request, "success/payment-succeed.html")
	response.delete_cookie('cart')
	data['cartItems'] = 0
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	ordered = []
	for item in items:
		ordered.append(f"{request.user} ordered: {item.product} = {str(item.quantity)} with {str(item.get_total)} birr")
	
	# print(ordered)

	context = {
		"order": ordered,
		"items":items,
		"group": group,
		"order":order,
		"method":method,
		"cartItems":cartItems
	}
	return render(request, "success/payment-succeed.html", context)


def error_404(request, exception):
    data = {}
    return render(request,'error/404.html', data)



# REST API INTEGRATIONS

class AddProducts(mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Food.objects.all()
	serializer_class = FoodSerializer
	
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

add_products = AddProducts.as_view()


class GetProductsList(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
	queryset = Hotel.objects.all()
	serializer_class = HotelSerializer
	lookup_field = 'pk'

	def get(self, request, *args, **kwargs):
		print(args, kwargs)
		pk = kwargs.get("pk")
		if pk is not None:
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)
get_products_list = GetProductsList.as_view()

class GetProductList(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
	mixins.UpdateModelMixin, generics.GenericAPIView):
	queryset = Food.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def get(self, request, *args, **kwargs):
		pk = kwargs.get("pk")
		if pk is not None:
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		pk = kwargs.get('pk')
		if pk is not None:
			return self.retrieve(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

get_product_list = GetProductList.as_view()


class UpdateProducts(mixins.UpdateModelMixin, generics.GenericAPIView):
	queryset = Food.objects.all()
	serializer_class = FoodSerializer
	lookup_field = "pk"



class UserCreateAPIView(mixins.ListModelMixin,
	mixins.CreateModelMixin,
 	generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	# authentication_classes = [authentication.TokenAuthentication]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


user_create_view = UserCreateAPIView.as_view()



class UserLoginView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		email = request.data.get('email')
		password = request.data.get('password')
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
			# return HttpResponse("Logged in successfully")
		return HttpResponse("Password or email is not correct")


login_client = UserLoginView.as_view()

