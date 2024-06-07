from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from cart.cart import Cart
from coupons.forms import CouponApplyForm
from coupons.models import Coupon, CouponUsage


# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    cart = Cart(request)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            # Check if the coupon has already been used by this user
            if CouponUsage.objects.filter(coupon=coupon, user=request.user).exists():
                messages.error(request, 'Vous avez déjà utilisé ce coupon.')
            else:
                # Mark the coupon as used for this user
                CouponUsage.objects.create(coupon=coupon, user=request.user)
                request.session['coupon_id'] = coupon.id
                messages.success(request, 'Coupon appliqué avec succès.')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Code coupon invalide')
    else:
        messages.error(request, 'Invalid form input.')
    return redirect('cart:cart_detail')
