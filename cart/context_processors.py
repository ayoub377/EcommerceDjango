from .cart import Cart
from .forms import CartAddProductForm


def cart(request):
    return {'cart': Cart(request)}


def AddformCart(request):
    formCart = CartAddProductForm()
    return {'formCart': formCart}
