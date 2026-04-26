from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.payments.models import Item, Order
from apps.payments.services import stripe_service


def index_view(request):
    return render(request, "payments/index.html", {
        "items": Item.objects.all(),
        "orders": Order.objects.prefetch_related("items").all(),
    })


class ItemDetailView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(
            request,
            "payments/item_detail.html",
            {
                "item": item,
                "stripe_public_key": stripe_service.get_public_key(item.currency),
            },
        )


class BuyItemView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        base_url = request.build_absolute_uri("/")
        session_id = stripe_service.create_item_checkout_session(
            item=item,
            success_url=f"{base_url}success/",
            cancel_url=request.build_absolute_uri(f"/item/{pk}/"),
        )
        return JsonResponse({"id": session_id})


class PayItemView(View):
    """Альтернативный эндпоинт через Payment Intent."""

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        data = stripe_service.create_item_payment_intent(item)
        return JsonResponse(data)


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk)
        return render(
            request,
            "payments/order_detail.html",
            {
                "order": order,
                "stripe_public_key": stripe_service.get_public_key(order.currency()),
            },
        )


class BuyOrderView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk)
        base_url = request.build_absolute_uri("/")
        session_id = stripe_service.create_order_checkout_session(
            order=order,
            success_url=f"{base_url}success/",
            cancel_url=request.build_absolute_uri(f"/order/{pk}/"),
        )
        return JsonResponse({"id": session_id})


def success_view(request):
    return render(request, "payments/success.html")
