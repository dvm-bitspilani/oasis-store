from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length = 100, default = '')
	price = models.IntegerField(default = 0)
	description = models.CharField(max_length = 1000)
	designer = models.CharField(max_length = 100, default = '')
	sales = models.IntegerField(default = 0)

