from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

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
                response = {'status': 'fail', 'message': 'You have already used this coupon.'}
            else:
                # Mark the coupon as used for this user
                CouponUsage.objects.create(coupon=coupon, user=request.user)
                request.session['coupon_id'] = coupon.id
                response = {'status': 'success', 'message': 'Coupon applied successfully'}
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            response = {'status': 'fail', 'message': 'Invalid coupon code'}
    else:
        response = {'status': 'fail', 'message': 'Invalid form input'}
    return redirect('cart:cart_detail')
