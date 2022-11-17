from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
import stripe
from django.conf import settings


def index(request):
	return render(request, "core/index.html")


def item(request, item_id):
	item = Item.objects.get(id=item_id)
	return render(request, "core/item.html", {"item": item})


def buy(request, item_id):
	item = Item.objects.get(id=item_id)
	stripe.api_key = settings.STRIPE_SECRET_TOKEN

	product = stripe.Product.create(
	  name=item.name,
	  description=item.description,
	)

	price = stripe.Price.create(
	  unit_amount=item.price,
	  currency="usd",
	  product=product['id'],
	)
	data = stripe.checkout.Session.create(
	  success_url="https://example.com/success",
	  cancel_url="https://example.com/cancel",
	  line_items=[
	    {
	      "price": price['id'],
	      "quantity": 1,
	    },
	  ],
	  mode="payment",
	)
	return JsonResponse({"id": data['id']})