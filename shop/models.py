from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length = 100, default = '')
	price = models.IntegerField(default = 0)
	description = models.CharField(max_length = 1000)
	designer = models.CharField(max_length = 100, default = '')
	sales = models.IntegerField(default = 0)
	pic_front = models.ImageField(upload_to = './shop/static/shop/itemspic', null = True)
	pic_back = models.ImageField(upload_to = './shop/static/shop/itemspic', null = True)
	colour = models.ManyToManyField('Colours', null = True, blank = True)
	size = models.ManyToManyField('Size', null = True, blank = True)
	limit = models.IntegerField(default = 0)
	category = models.CharField(max_length = 30, null = True)

	def __unicode__(self):
		return self.name

class Colours(models.Model):
	name = models.CharField(max_length = 20, default = '')

	def __unicode__(self):
		return self.name

class Size(models.Model):
	size = models.CharField(max_length = 5, default = '')

	def __unicode__(self):
		return self.size
		
class Order(models.Model):
	email = models.CharField(max_length = 60)
	item = models.ForeignKey('Item', null = True)
	color = models.ForeignKey('Colours', null = True)
	size = models.ForeignKey('Size', null = True)
	uniqueid = models.CharField(max_length = 20, null = True)
	quantity = models.CharField(max_length = 10, default = '0')

	def __unicode__(self):
		return self.email
