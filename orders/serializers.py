
from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from products.models import Product


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "shipping_address",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    items = OrderItemInputSerializer(many=True, allow_empty=False)

    def validate_items(self, items):
        product_ids = [item["product_id"] for item in items]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Bir mahsulotni bir buyurtmada takrorlamang."
            )

        products = Product.objects.filter(
            id__in=product_ids,
            is_active=True
        )

        product_map = {product.id: product for product in products}

        for item in items:
            product = product_map.get(item["product_id"])

            if product is None:
                raise serializers.ValidationError(
                    f"Product ID {item['product_id']} topilmadi."
                )

            if product.stock < item["quantity"]:
                raise serializers.ValidationError(
                    f"{product.name} mahsuloti uchun zaxira yetarli emas."
                )

        return items

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        with transaction.atomic():
            # Mahsulotlarni qayta tekshiramiz va satrlarni bloklaymiz.
            product_ids = [item["product_id"] for item in items_data]

            products = Product.objects.select_for_update().filter(
                id__in=product_ids,
                is_active=True
            )
            product_map = {product.id: product for product in products}

            total = Decimal("0.00")

            for item in items_data:
                product = product_map.get(item["product_id"])

                if product is None:
                    raise serializers.ValidationError({
                        "items": "Mahsulot topilmadi yoki faol emas."
                    })

                if product.stock < item["quantity"]:
                    raise serializers.ValidationError({
                        "items": f"{product.name}: zaxira yetarli emas."
                    })

                total += product.price * item["quantity"]

            order = Order.objects.create(
                user=user,
                shipping_address=validated_data["shipping_address"],
                total_amount=total,
            )

            for item in items_data:
                product = product_map[item["product_id"]]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                )

                product.stock -= quantity
                product.save(update_fields=["stock"])

        return order
