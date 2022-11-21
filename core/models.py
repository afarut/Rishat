from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
	name = models.CharField(max_length=40)
	description = models.TextField()
	price = models.PositiveIntegerField(default=50, validators=[MinValueValidator(50)])

	def __str__(self):
		return self.name


class Discount(models.Model):
	currency = models.CharField(max_length=3) # required
	name = models.CharField(max_length=40, blank=True, null=True)
	# !!! Ограничения описаны в signals.py !!!
	amount_off = models.IntegerField(help_text="optional if percent_off is required", 
		validators=[MinValueValidator(1)], blank=True, null=True)
	percent_off = models.FloatField(help_text="optional if amount_off is required", 
		validators=[MinValueValidator(0.1), MaxValueValidator(100)], blank=True, null=True)

	def is_valid(self):
		in_none = bool(self.amount_off is None and self.percent_off is None)
		is_full =  bool((not self.amount_off is None) and (not self.percent_off is None))
		if in_none == False and is_full == False:
			return True
		return False

	def __str__(self):
		if self.name is None:
			return f"currency: {self.currency}"
		else:
			return self.name


class Order(models.Model):
	items = models.ManyToManyField(Item)
	discount = models.ForeignKey(Discount, on_delete = models.CASCADE, blank=True, null=True)