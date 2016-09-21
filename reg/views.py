from django.shortcuts import render

@csrf_exempt
def reg(request):
	if request.POST:
		email = request.POST['email']
		password = request.POST['password']
		c_password = request.POST['confirm_password']
		if password == c_password:
			user = User.objects.create_user(
			username=email,
			password=password)		
			return render(request, 'reg/success.html')		
		else:
			return JsonResponse({'message': 'The passwords did not match'})	

@csrf_exempt
def user_login(request):

	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:	
			login(request, user)
		else: 
			return JsonResponse({'message': 'Invalid Credentials'})			
