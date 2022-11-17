from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Item, Order
import stripe
from django.conf import settings
from .forms import MultipleChoiceForm


def index(request):
	return render(request, "core/index.html")


def item(request, item_id):
	item = Item.objects.get(id=item_id)
	return render(request, "core/item.html", {"item": item, "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY})


def buy(request, item_id):
	item = Item.objects.get(id=item_id)
	stripe.api_key = settings.STRIPE_SECRET_TOKEN

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
	  success_url="https://example.com/success",
	  cancel_url="https://example.com/cancel",
	  line_items=[
	    {
	      "price": starter_subscription_price['id'],
	      "quantity": 1,
	    },
	  ],
	  mode="payment",
	)
	return JsonResponse({"id": payment_link['id']})


def order(request):
	stripe.api_key = settings.STRIPE_SECRET_TOKEN
	items = Item.objects.all()
	form = MultipleChoiceForm(request.POST or None)
	choices = tuple([(item.id, item.name) for item in items])
	form.fields["order"].choices = choices
	if form.is_valid():
		items_id = form.cleaned_data.get("order")
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
			  #recurring={"interval": "month"},
			  product=product['id'],
			)
			catalog.append({"price": price['id'], "quantity": 1})

		session = stripe.checkout.Session.create(
		  success_url="https://example.com/success",
		  cancel_url="https://example.com/cancel",
		  line_items=catalog,
		  mode="payment",
		)
		order.save()
		return redirect(session['url'])
	return render(request, "core/order.html", {"items": items, "form": form})