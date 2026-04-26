from django.urls import path

from . import views

urlpatterns = [
    path("item/<int:pk>/", views.ItemDetailView.as_view(), name="item-detail"),
    path("buy/<int:pk>/", views.BuyItemView.as_view(), name="buy-item"),
    path("pay/<int:pk>/", views.PayItemView.as_view(), name="pay-item"),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("buy-order/<int:pk>/", views.BuyOrderView.as_view(), name="buy-order"),
    path("success/", views.success_view, name="success"),
]
