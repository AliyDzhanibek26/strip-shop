from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Currency(models.TextChoices):
    USD = "usd", "USD"
    EUR = "eur", "EUR"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency.upper()})"

    def price_in_cents(self) -> int:
        return int(self.price * 100)


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Процент"
        AMOUNT = "amount", "Фиксированная сумма"

    name = models.CharField(max_length=255)
    stripe_coupon_id = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Процент (0–100) или сумма в валюте",
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        if self.discount_type == self.DiscountType.PERCENT:
            return f"{self.name} ({self.value}%)"
        return f"{self.name} (-{self.value})"


class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_tax_rate_id = models.CharField(max_length=255, blank=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    inclusive = models.BooleanField(
        default=False,
        help_text="Включён в цену или добавляется сверху",
    )

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        kind = "вкл." if self.inclusive else "доп."
        return f"{self.name} ({self.percentage}% {kind})"


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders", verbose_name="Товары")
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk}"

    def total_amount(self) -> Decimal:
        return sum(item.price for item in self.items.all())

    def currency(self) -> str:
        first = self.items.first()
        return first.currency if first else Currency.USD

    def total_in_cents(self) -> int:
        return int(self.total_amount() * 100)
