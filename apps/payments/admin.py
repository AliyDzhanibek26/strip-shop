from django.contrib import admin
from django.utils.html import format_html

from .models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "currency")
    list_filter = ("currency",)
    search_fields = ("name",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discount_type", "value", "stripe_coupon_id")
    list_filter = ("discount_type",)
    search_fields = ("name",)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "percentage", "inclusive", "stripe_tax_rate_id")
    list_filter = ("inclusive",)
    search_fields = ("name",)


class OrderItemsInline(admin.TabularInline):
    model = Order.items.through
    extra = 1
    verbose_name = "Товар"
    verbose_name_plural = "Товары в заказе"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_display", "discount", "tax", "created_at")
    list_filter = ("discount", "tax")
    readonly_fields = ("created_at", "total_display")
    inlines = [OrderItemsInline]
    exclude = ("items",)

    @admin.display(description="Сумма")
    def total_display(self, obj):
        try:
            return format_html(
                "<strong>{} {}</strong>",
                obj.total_amount(),
                obj.currency().upper(),
            )
        except Exception:
            return "—"
