from django.shortcuts import redirect


def authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func


def allowed_user(allowed_group=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				# print(request.user.groups.get(name='Customer'))
				if request.user.groups.count() > 1:			
					group = request.user.groups.all()[1].name
				else:
					group = request.user.groups.all()[0].name
				
			if group in allowed_group:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('error')
		return wrapper_func
	return decorator
	