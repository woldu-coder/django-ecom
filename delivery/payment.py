

def user_payment_info(request, *args, **kwargs):
	user_id = request.user.id
	name = request.user
	item_name = kwargs['items']
	no_item  = kwargs['no_item']
	price    = kwargs['price']
	payment_method = kwargs['payment_method']


	return 
