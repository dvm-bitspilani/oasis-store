from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from allauth.socialaccount.models import *
from django.core.urlresolvers import reverse
from .models import *
from django.core.cache import cache
import time

@csrf_exempt
def index(request):
	return render(request, 'shop/index-2.html')


@csrf_exempt
def buy(request):
	# user = request.user
	# userp = UserProfile.objects.get(user = request.user)
	# if user is not None:
	# print request.session['uniqueID']
	if request.POST:
		request.session['uniqueID'] = str(time.time)
		uid = request.session['uniqueID']
		print(request.session['uniqueID'])
		itemID = request.POST['itemID']
		item = Item.objects.get(pk = itemID)
		quantity = request.POST['quantity']
		size = request.POST['size']
		price = item.price
		name = item.name
		# color = item.colour		
		# key = (str(user.id) + ',' + str(itemID)) since there isnt any user
		key = (str(itemID) + ',' + str(uid))
		if cache.has_key(key):
			tmpcache = cache.get(key)
			tmpcachequant = int(tmpcache['quantity']) + int(quantity)
			cache.set(key, {
				'itemID': itemID,
				'price': price,
				'quantity': tmpcachequant,
				'size': size,
				# 'color': color,
				'name': name,
				'executionType': 'buy'
				},
				timeout = None)
				# if len(request.session['item']) == 0:
				# 	request.session['item'] = [key]
				# else:
				# 	request.session.append(key)
		else:
			cache.set(key, {
				'itemID': itemID,
				'price': price,
				'quantity': quantity,
				'executionType': 'buy',
				'size': size,
				# 'color': color,
				'name': name
				},
				timeout = None)
			if len(request.session['uniqueID']) == 0:
				request.session['uniqueID'] = [key]
			else:
				request.session.append(key)
		# sending data back incase someone does any mischief in price in frontend
		data = {
			'itemID': itemID,
			'price': price,
			'quantity': quantity,
			'size': size,
			# 'color': color,
			'name': name
		}
		resp = {'status': True, 'message': item.name + ' added succesfully to the cart','data':data}
		return JsonResponse(resp)
	# else:
	# 	return HttpResponseRedirect('../login')

@login_required
def getcart(request):
	# user = request.user
	uid = request.session['uniqueID']
	keys = str(uid) + "*"
	cart = cache.keys(keys)
	resp = []
	totalprice = 0
	for item in cart:
		tmpitem = cache.get(item)
		t_price = int(tmpitem['price'])*int(tmpitem['quantity'])
		totalprice+=t_price

		resp.append({'itemID': tmpitem['itemID'], 'name': tmpitem['name'], 'price': tmpitem['price'], 'quantity': tmpitem['quantity'], 't_price': t_price, 'size': tmpitem['size'], 'color': tmpitem['color']})

	return JsonResponse({'items': resp})

@login_required
def checkoutcart(request):
	# user = request.user
	uid = request.session['uniqueID']
	keys = str(uid) + "*"
	cart = cache.keys(keys)
	resp = []
	tt_price = 0
	num = 1
	cartbody = []
	for item in cart:
		tmpitem = cache.get(item)
		t_price = int(tmpitem['price'])*int(tmpitem['quantity'])
		quantity = int(tmpitem['quantity'])
		tt_price+=t_price
		name = tmpitem['name']
		size = tmpitem['size']
		itemID = tmpitem['itemID']
		itemst = Item.objects.get(itemID = itemID)
		itemst.sales+=1

		cartbody.append('''
						%s  %s  %s  %s

						''' %(num, name, size, quantity, t_price))
		num+=1

	y = 0
	while y < len(cartbody):
		tcartbody = cartbody[y] + "\n"
		y+=1

	email = request.POST['email_id']
	body = '''

Thank you for placing the order.
You have ordered the following items

				''' + tcartbody


	email = EmailMultiAlternatives('Registration Confirmation', '---', 'register@bits-oasis.org', [send_to.strip()]) #connection=awsbackend)
	email.attach_alternative(body, "text/html");
	try:
		email.send()
	except SMTPException:
		try:
			bosm2016.settings.EMAIL_HOST_USER = bosm2016.email_config.config.email_host_user[1]
			bosm2016.settings.EMAIL_HOST_PASSWORD = bosm2016.email_config.config.email_host_pass[1]
			email.send()
		except SMTPException:

			bosm2016.settings.EMAIL_HOST_USER = bosm2016.email_config.config.email_host_user[2]
			bosm2016.settings.EMAIL_HOST_PASSWORD = bosm2016.email_config.config.email_host_pass[2]
			email.send()
	keys = str(user.id) + "*"
	cart = cache.delete_pattern(keys)

	resp = {'success': True, 'message': 'Thank you for placing the order. You have been sent a mail regarding your order details'}

def getitem(request, itemid):
	# if request.POST:
		# itemID = request.POST['itemID']
	item = Item.objects.get(pk = itemid)
	name = item.name
	price = item.price
	pic_f = str(item.pic_front.url)[4:]
	pic_b = str(item.pic_back.url)[4:]
	desc = item.description
	colours = ''
	for color in item.colour.all():
		colours += str(color)
	# colours = [x for x in item.colour]
	# send the user current cart as well..lets say he refreshes the page
	context = {'name': name, 'price': price, 'pic_f': pic_f, 'pic_b': pic_b, 'desc': desc, 'colours': colours}
	return JsonResponse(context) #render(request, 'shop/product.html', context)

def getall(request):
	items = Item.objects.all()
	resp = []
	for item in items:
		resp.append({'id': item.id, 'name': item.name, 'price': item.price, 'description': item.description, 'img': str(item.pic_front.url)[4:]})

	response = {'items': resp}

	return JsonResponse(response)
