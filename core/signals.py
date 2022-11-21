from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Discount
from django.core.exceptions import ValidationError
import stripe
from django.conf import settings 


@receiver(pre_save, sender=Discount)
def my_handler(sender, instance, **kwargs):
	if instance.amount_off is None and instance.percent_off is None:
		raise ValidationError('amount_off or percent_off must be require.')
	elif (not instance.amount_off is None) and (not instance.percent_off is None):
		raise ValidationError('amount_off or percent_off must be empty.')
	stripe.api_key = settings.STRIPE_SECRET_TOKEN
	a = stripe.Coupon.create(
	  percent_off=instance.percent_off,
	  amount_off=instance.amount_off,
	  currency=instance.currency,
	  name=instance.name,
	  duration="once"
	)
	instance.name = a['id']