from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
	path('', views.index, name='index'),
	path('buy/<int:item_id>', views.buy, name='buy'),
	path('item/<int:item_id>', views.item, name='item'),
]