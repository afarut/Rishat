from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Item, Order, Discount
import stripe
from django.conf import settings
from .forms import MultipleChoiceForm
from .signals import *


def index(request):
	return render(request, "core/index.html")


def item(request, item_id):
	item = Item.objects.get(id=item_id)
	return render(request, "core/item.html", {"item": item, "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY})


def buy(request, item_id):
	item = Item.objects.get(id=item_id)
	stripe.api_key = settings.STRIPE_SECRET_TOKEN

	if request.is_secure():
	    protocol = 'https://'
	else:
	    protocol = 'http://'
	hosname = protocol + request.get_host()

	starter_subscription = stripe.Product.create(
	  name=item.name,
	  description=item.description,
	)

	starter_subscription_price = stripe.Price.create(
	  unit_amount=item.price,
	  currency="usd",
	  product=starter_subscription['id'],
	)
	payment_link = stripe.checkout.Session.create(
	  success_url=hosname+"/success",
	  cancel_url=hosname+"/cancel",
	  line_items=[
	    {
	      "price": starter_subscription_price['id'],
	      "quantity": 1,
	    },
	  ],
	  mode="payment",
	  #automatic_tax={     Без
	  #  'enabled': True,  Активации
	  #},				   Не работает
	)
	return JsonResponse({"id": payment_link['id']})


def order(request):
	stripe.api_key = settings.STRIPE_SECRET_TOKEN
	items = Item.objects.all()
	form = MultipleChoiceForm(request.POST or None)
	choices = tuple([(item.id, item.name) for item in items])
	form.fields["order"].choices = choices
	if request.is_secure():
	    protocol = 'https://'
	else:
	    protocol = 'http://'
	hosname = protocol + request.get_host()


	if form.is_valid():
		cd = form.cleaned_data
		items_id = cd.get("order")
		try:
			discount = Discount.objects.get(name=cd["discount"])
		except Discount.DoesNotExist:
			discount = None
		order = Order.objects.create()
		catalog = list()
		for item_id in items_id:
			item = Item.objects.get(id=item_id)
			order.items.add(item)

			product = stripe.Product.create(
			  name=item.name,
			  description=item.description,
			)

			price = stripe.Price.create(
			  unit_amount=item.price,
			  currency="usd",
			  product=product['id'],
			)
			catalog.append({"price": price['id'], "quantity": 1})
		if discount is None:
			success_url = hosname + "/success/"
			session = stripe.checkout.Session.create(
			  success_url=success_url,
			  cancel_url=hosname+"/cancel",
			  line_items=catalog,
			  mode="payment"
			)
		else:
			success_url = hosname + f"/success/{cd['discount']}"
			session = stripe.checkout.Session.create(
			  success_url=success_url,
			  cancel_url=hosname+"/cancel",
			  line_items=catalog,
			  mode="payment",
			  discounts=[{
			  	"coupon": cd["discount"]
			  }]
			)
		order.save()
		return redirect(session['url'])
	return render(request, "core/order.html", {"items": items, "form": form})


def discount(request, tocheck):
	try:
		discount = Discount.objects.get(name=tocheck)
	except Discount.DoesNotExist:
		discount = None
		return JsonResponse({"is_exist": False})
	if discount.amount_off is None:
		text = f"Скидка в {discount.percent_off}%"
	else:
		text = f"Скидка в {discount.amount_off} {discount.currency}"
	return JsonResponse({"is_exist": True, "bonus": text, "currency": discount.currency.upper()})


def success(request, discount="main"):
	try:
		discount = Discount.objects.get(name=discount)
		discount.delete()
	except Discount.DoesNotExist:
		discount = None

	return HttpResponse("Оплата прошла")


def cancel(request):
	return HttpResponse("Оплата не прошла")