from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
	path('', views.index, name='index'),
	path('buy/<int:item_id>', views.buy, name='buy'),
	path('item/<int:item_id>', views.item, name='item'),
	path('order', views.order, name='order'),
	path('discount/<str:tocheck>', views.discount, name='discount'),
	path('success/', views.success, name='success'),
	path('success/<str:discount>', views.success, name='success'),
	path('cancel', views.cancel, name='cancel'),
]