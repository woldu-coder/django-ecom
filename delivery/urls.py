from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path('', views.home_page, name='home'),
	path('home/', views.home_page, name='home'),
	path('about/', views.about_page, name='about'),
	path('location/', views.location_handler, name='location'),
	
	path('store/', views.stores, name='store'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),

	path('sign_up/', views.signup_page, name='sign_up'),
	path('add_product/', views.add_product, name='add_product'),
	path('error/', views.access_denied, name='error'),

	path('checkout/', views.checkout, name='checkout'),
	path('cart_list/', views.cart_list, name='cart_list'),
	path('update_item/', views.updateItem, name='update_item'),

	path('message/', views.message, name='message'),
	path('payment/', views.payment, name='payment'),
	path('payment_method/<str:args>/', views.payment_method, name='payment-method'),

		# Password Reset
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='reset_password'),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_sent.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),



	# REST API INTEGRATIONS
	path("hotels/", views.get_products_list),
	path("hotels/<int:pk>/", views.get_products_list),
	path("products/", views.get_product_list),
	path("products/<int:pk>/", views.get_product_list),
	path("users/", views.user_create_view),
	path("login_client/", views.login_client),


	# Tokens 
	
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]


