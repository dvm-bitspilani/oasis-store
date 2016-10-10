from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length = 100, default = '')
	price = models.IntegerField(default = 0)
	description = models.CharField(max_length = 1000)
	designer = models.CharField(max_length = 100, default = '')
	sales = models.IntegerField(default = 0)
	pic_front = models.ImageField(upload_to = 'itemspic', null = True)
	pic_back = models.ImageField(upload_to = 'itemspic', null = True)
	colour = models.ManyToManyField('Colours')

	def __unicode__(self):
		return self.name

class Colours(models.Model):
	name = models.CharField(max_length = 20, default = '')

	def __unicode__(self):
		return self.name

