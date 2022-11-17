from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
	name = models.CharField(max_length=40)
	description = models.TextField()
	price = models.PositiveIntegerField(default=50, validators=[MinValueValidator(50)])

	def __str__(self):
		return self.name


class Order(models.Model):
	items = models.ManyToManyField(Item)