from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True,
                                        is_used=False)
            request.session['coupon_id'] = coupon.id
            coupon.is_used = True
            coupon.save(force_update=True)
            response = {'status': 'success', 'message': 'Coupon applied successfully'}
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            response = {'status': 'fail', 'message': 'Invalid coupon code'}
    else:
        response = {'status': 'fail', 'message': 'Invalid form input'}
    return JsonResponse(response)