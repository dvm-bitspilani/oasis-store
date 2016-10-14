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
		if request.session['uniqueID'] == None:
			request.session['uniqueID'] = str(time.time())
			request.session.modified = True
			uid = request.session['uniqueID']
			print(request.session['uniqueID'])
		else: 
			pass

		itemID = request.POST['itemID']
		item = Item.objects.get(pk = itemID)
		if item.category != 'ticket':
			quantity = request.POST['quantity']
			size = request.POST['size']
			color = request.POST['color']
			price = item.price
			name = item.name
			# color = item.colour
			# key = (str(user.id) + ',' + str(itemID)) since there isnt any user
			key = (str(uid) + ',' + str(itemID) + ',' + str(size) + str(color))
			print(uid,key)

			if cache.has_key(key):
				tmpcache = cache.get(key)
				tmpcachequant = int(tmpcache['quantity']) + int(quantity)
				cache.set(key, {
					'itemID': itemID,
					'price': price,
					'quantity': tmpcachequant,
					'size': size,
					'color': color,
					'name': name,
					'executionType': 'buy'
					},
					timeout = None)
					# if len(request.session['item']) == 0:
					# 	request.session['item'] = [key]
					# else:
					# 	request.session.append(key)
				data = {
					'itemID': itemID,
					'price': price,
					'quantity': quantity,
					'size': size,
					'color': color,
					'name': name
				}
				resp = {'status': True, 'message': item.name + ' added succesfully to the cart', 'data':data}
			else:
				cache.set(key, {
					'itemID': itemID,
					'price': price,
					'quantity': quantity,
					'executionType': 'buy',
					'size': size,
					'color': color,
					'name': name
					},
					timeout = None)
				# if len(request.session['uniqueID']) == 0:
				# 	request.session['uniqueID'] = [key]
				# else:
				# 	request.session['uniqueID'].append(key)
			# sending data back incase someone does any mischief in price in frontend
			data = {
				'itemID': itemID,
				'price': price,
				'quantity': quantity,
				'size': size,
				'color': color,
				'name': name
			}
			resp = {'status': True, 'message': item.name + ' added succesfully to the cart', 'data':data}

		else: 
			quantity = request.POST['quantity']
			price = item.price
			name = item.name
			# color = item.colour
			# key = (str(user.id) + ',' + str(itemID)) since there isnt any user
			key = (str(uid) + ',' + str(itemID))
			print(uid,key)

			if cache.has_key(key):
				tmpcache = cache.get(key)
				tmpcachequant = int(tmpcache['quantity']) + int(quantity)
				cache.set(key, {
					'itemID': itemID,
					'price': price,
					'quantity': tmpcachequant,
					'name': name,
					'executionType': 'buy'
					},
					timeout = None)
					# if len(request.session['item']) == 0:
					# 	request.session['item'] = [key]
					# else:
					# 	request.session.append(key)
				data = {
					'itemID': itemID,
					'price': price,
					'quantity': quantity,
					'name': name
				}
				resp = {'status': True, 'message': item.name + ' added succesfully to the cart', 'data':data}
			else:
				cache.set(key, {
					'itemID': itemID,
					'price': price,
					'quantity': quantity,
					'executionType': 'buy',
					'name': name
					},
					timeout = None)
				# if len(request.session['uniqueID']) == 0:
				# 	request.session['uniqueID'] = [key]
				# else:
				# 	request.session['uniqueID'].append(key)
			# sending data back incase someone does any mischief in price in frontend
			data = {
				'itemID': itemID,
				'price': price,
				'quantity': quantity,
				'name': name
			}
			resp = {'status': True, 'message': item.name + ' added succesfully to the cart', 'data':data}			

	return JsonResponse(resp)
	# else:
	# 	return HttpResponseRedirect('../login')

def getcart(request):
	# user = request.user
	uid = request.session['uniqueID']
	keys = str(uid) + "*"
	print cache.keys(keys)
# <<<<<<< HEAD
# 	cart = cache.get(str(keys))
# 	resp = []
# 	totalprice = 0
# 	print(cart)
# 	for item in cart:
# 		tmpitem = cache.get(item)
# =======
	# cart = cache.get(keys)
	keyss = cache.keys(keys)
	resp = []
	totalprice = 0

	# try:
		# while next(cache.iter_keys(keys)) != None:
	x = 0
	for x in range(0,len(keyss)):
		tmpitem = cache.get(keyss[x])
		t_price = int(tmpitem['price'])*int(tmpitem['quantity'])
		getitem = Item.objects.get(pk = tmpitem['itemID'])
		if getitem.category != 'ticket':
			itemimg = getitem.pic_front.url
			print itemimg
			totalprice+=t_price
			x+=1

			resp.append({'itemID': tmpitem['itemID'], 'name': tmpitem['name'], 'price': tmpitem['price'], 'quantity': tmpitem['quantity'], 't_price': t_price,'img': str(getitem.pic_front.url)[4:]})
		else:

			itemimg = getitem.pic_front.url
			print itemimg
			totalprice+=t_price
			x+=1

			resp.append({'itemID': tmpitem['itemID'], 'name': tmpitem['name'], 'price': tmpitem['price'], 'quantity': tmpitem['quantity'], 't_price': t_price, 'size': tmpitem['size'], 'color': tmpitem['color'], 'img': str(getitem.pic_front.url)[4:]})			
	# except next(cache.iter_keys(keys) == None):
	# 	pass

	return JsonResponse({'items': resp, 'cartid': uid})

import hmac
import hashlib
@csrf_exempt
def checkoutcart(request):
	# user = request.user
	uid = request.session['uniqueID']
	keys = str(uid) + "*"
	cart = cache.get(keys)
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
		color = tmpitem['color']
		itemst = Item.objects.get(itemID = itemID)

		itemst.sales+=quantity

		cartbody.append('''
						%s  %s  %s  %s %s

						''' %(num, name, size, quantity, color, t_price))
		num+=1

	y = 0
	while y < len(cartbody):
		tcartbody = cartbody[y] + "\n"
		y+=1
	if request.method == 'POST':

		email = request.POST['email']
		showlist = request.POST['items']
		tt_price = request.POST['TotalPrice']
		quantity = request.POST['quantity']

	# email = request.POST['email_id']
	body = '''

Thank you for placing the order.
You have ordered the following items. Kindly follow the link %s to make the payment. Ignore if already paid.

				''' + tcartbody


	email = EmailMultiAlternatives('Registration Confirmation', '---', 'register@bits-oasis.org', [send_to.strip()]) #connection=awsbackend)
	email.attach_alternative(body, "text/html");

	a = 0
	for x in showlist:
		
		shows = ( str( ','.join( shows ) ) )
		a+=1

	salt = 'ecbc4820f1c248eb88cdcff26325d00b'
	message = str(shows)+'|'+str(tt_price)+'|'+str(email)+'|'+str(quantity)
	mac_calculated = hmac.new(
     	str(salt),
    	message,
    	hashlib.sha1,
    	).hexdigest()

	b = 'https://www.instamojo.com/bitsoasis16/oasis-professional-shows/'+'?intent=buy&data_Field_5581='+shows+'&data_amount='+str(tt_price)+'&data_email='+str(email)+'&data_quantity='+quantity+'&data_readonly=data_amount&data_readonly=data_Field_5581&data_readonly=data_email&data_readonly=data_quantity&data_sign='+mac_calculated

	email.send()

	keys = str(uid) + "*"
	cart = cache.delete_pattern(keys)

	# resp = {'success': True, 'message': 'Thank you for placing the order. You have been sent a mail regarding your order details'}
	return HttpResponseRedirect(b)


def getitem(request, itemid):
	# if request.POST:
		# itemID = request.POST['itemID']
	item = Item.objects.get(pk = itemid)
	if item.category != 'ticket':
		name = item.name
		price = item.price
		pic_f = str(item.pic_front.url)[4:]
		pic_b = str(item.pic_back.url)[4:]
		desc = item.description

		# send the user current cart as well..lets say he refreshes the page
		context = {'id':itemid,'name': name, 'price': price, 'pic_f': pic_f, 'pic_b': pic_b, 'desc': desc, 'colours': item.colour.all(),'sizes':item.size.all()}
	else:
		price = item.price
		pic_f = str(item.pic_front.url)[4:]
		pic_b = str(item.pic_back.url)[4:]
		desc = item.description

		# send the user current cart as well..lets say he refreshes the page
		context = {'id':itemid,'name': name, 'price': price, 'pic_f': pic_f, 'pic_b': pic_b, 'desc': desc }
	return render(request, 'shop/product.html', context)

def getall(request):
	items = Item.objects.all()
	resp = []
	for item in items:
		resp.append({'id': item.id, 'name': item.name, 'price': item.price, 'description': item.description, 'img': str(item.pic_front.url)[4:]})

	response = {'items': resp}

	return JsonResponse(response)

@csrf_exempt
def removeItem(request):
	cartuid = request.POST['cartid']
	cache.delete(cartuid)

	return JsonResponse({'message': 'The following item has been removed from the cart'})

################################Instamojo Payment Portal###########################################
# import hmac
# import hashlib
# def final_pay(request):
# 	if request.method == 'POST':

# 		email = request.POST['email']
# 		showlist = request.POST['items']
# 		tt_price = request.POST['TotalPrice']

# 		a = 0
# 		for x in shows:
			
# 			shows = ( str( ','.join( shows ) ) )
# 			a+=1

# 		salt = 'ecbc4820f1c248eb88cdcff26325d00b'
# 		message = str(shows)+'|'+str(tt_price)+'|'+str(email)	
# 		mac_calculated = hmac.new(
# 	     	str(salt),
#         	message,
#         	hashlib.sha1,
#         	).hexdigest()

# 		b = 'https://www.instamojo.com/bitsoasis16/oasis-professional-shows/'+'?intent=buy&data_Field_5581='+shows+'&data_amount='+str(tt_price)+'&data_email='+str(email)+'&data_readonly=data_amount&data_readonly=data_Field_5581&data_readonly=data_email&data_sign='+mac_calculated

# 		return HttpResponseRedirect(b)

# 	# return render('middlepage.html', context={'email_id':request.GET['email']})
# 	return JsonResponse({'message': 'You have successfully made the payment'})

def apirequest(request):
	import requests
	payid=str(request.GET['payment_id'])
	headers = {'X-Api-Key': '9efcf3131144007821bcbc905dabebc7',
    	       'X-Auth-Token': '03c40f518819e3e9d84d31156fee5681'}
	r = requests.get('https://www.instamojo.com/api/1.1/payments/',
                	 headers=headers)
	json_ob = r.json()
	payments = json_ob['payments'][0]
	amount = payments['amount']
	email = payments['email']
	itemfield = custom_fields_['Field_5581']
	itemslist = str(itemfield['value']).split(',')

	# try:
	# 	email = payments['custom_fields']['Field_5581']['value']
	# 	user=Participant.objects.filter(email_id = email)[0]
	# 	if int(float(amount)) == 300:
	# 		user.reg_paid=True
	# 	user.save()
	# except:
	# 	ids = payments['custom_fields']['Field_5581']['value'].split('.')
	# 	no_paid = int(float(amount))/300
	# 	for i in ids[:no_paid]:
	# 		user = Participant.objects.get(id = int(i))
	# 		user.reg_paid=True
	# 		user.save()

	order = Order()
	# order.item = request.POST['itemID']
	order.email = email
	for item in itemlist:
		order.item = item
	# order.size = size
	# order.color = color
	order.save()
	context = {
		'status' : 1,
		'message' : 'Payment Successful.'
	}
	return JsonResponse(context)
