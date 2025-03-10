from django.contrib import admin
from.models import *

admin.site.register([Admin, Cliente, Categoria, Produto, Cart, CartItem, Pedido_order])
