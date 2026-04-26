from typing import Optional

import stripe
from django.conf import settings

from apps.payments.models import Discount, Item, Order, Tax


def _get_stripe_client(currency: str) -> stripe.StripeClient:
    keys = settings.STRIPE_CURRENCY_KEYS.get(currency.lower())
    if not keys or not keys.get("secret"):
        raise ValueError(f"Stripe ключи для валюты '{currency}' не настроены")
    return stripe.StripeClient(keys["secret"])


def get_public_key(currency: str) -> str:
    keys = settings.STRIPE_CURRENCY_KEYS.get(currency.lower(), {})
    return keys.get("public", "")


def _ensure_coupon(client: stripe.StripeClient, discount: Discount) -> str:
    if discount.stripe_coupon_id:
        return discount.stripe_coupon_id

    params: dict = {"name": discount.name}
    if discount.discount_type == Discount.DiscountType.PERCENT:
        params["percent_off"] = float(discount.value)
        params["duration"] = "once"
    else:
        params["amount_off"] = int(discount.value * 100)
        params["duration"] = "once"

    coupon = client.coupons.create(params=params)
    discount.stripe_coupon_id = coupon.id
    discount.save(update_fields=["stripe_coupon_id"])
    return coupon.id


def _ensure_tax_rate(client: stripe.StripeClient, tax: Tax) -> str:
    if tax.stripe_tax_rate_id:
        return tax.stripe_tax_rate_id

    tax_rate = client.tax_rates.create(
        params={
            "display_name": tax.name,
            "percentage": float(tax.percentage),
            "inclusive": tax.inclusive,
        }
    )
    tax.stripe_tax_rate_id = tax_rate.id
    tax.save(update_fields=["stripe_tax_rate_id"])
    return tax_rate.id


def create_item_checkout_session(item: Item, success_url: str, cancel_url: str) -> str:
    client = _get_stripe_client(item.currency)

    session = client.checkout.sessions.create(
        params={
            "payment_method_types": ["card"],
            "line_items": [
                {
                    "price_data": {
                        "currency": item.currency,
                        "product_data": {"name": item.name},
                        "unit_amount": item.price_in_cents(),
                    },
                    "quantity": 1,
                }
            ],
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
    )
    return session.id


def create_order_checkout_session(order: Order, success_url: str, cancel_url: str) -> str:
    currency = order.currency()
    client = _get_stripe_client(currency)

    line_items = [
        {
            "price_data": {
                "currency": currency,
                "product_data": {"name": item.name},
                "unit_amount": item.price_in_cents(),
            },
            "quantity": 1,
        }
        for item in order.items.all()
    ]

    params: dict = {
        "payment_method_types": ["card"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
    }

    if order.discount:
        coupon_id = _ensure_coupon(client, order.discount)
        params["discounts"] = [{"coupon": coupon_id}]

    if order.tax:
        tax_rate_id = _ensure_tax_rate(client, order.tax)
        for line_item in params["line_items"]:
            line_item["tax_rates"] = [tax_rate_id]

    session = client.checkout.sessions.create(params=params)
    return session.id


def create_item_payment_intent(item: Item) -> dict:
    client = _get_stripe_client(item.currency)

    intent = client.payment_intents.create(
        params={
            "amount": item.price_in_cents(),
            "currency": item.currency,
            "automatic_payment_methods": {"enabled": True},
        }
    )
    return {
        "client_secret": intent.client_secret,
        "public_key": get_public_key(item.currency),
    }
