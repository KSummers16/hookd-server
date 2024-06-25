from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .orders import OrderSerializer
from .lineitem import CartItemSerializer
from .rtsproduct import RTSProductSerializer
from .cusrequest import CusRequestSerializer
from hookdapi.models import (
    Customer,
    OrderProduct,
    Order,
    RTSProduct,
    CusRequest,
    CusProduct,
    RTSSold,
    Eyes,
    Color,
    Cart,
)
import datetime
from django.core.mail import send_mail


class CartView(viewsets.ViewSet):
    shipping_cost = 10  # $10 in shipping

    def calculate_total_price(self, open_order):
        order_products = OrderProduct.objects.filter(order=open_order)
        subtotal = sum(
            (op.rtsproduct.price if op.rtsproduct else op.cusrequest.cus_product.price)
            for op in order_products
        )
        return subtotal + self.shipping_cost

    def create(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(customer=current_user, emailed=False)
        except Order.DoesNotExist:
            open_order = Order.objects.create(
                customer=current_user, created_date=datetime.datetime.now()
            )

        # Handle adding an RTSProduct to the cart
        rtsproduct_id = request.data.get("rtsproduct_id")
        if rtsproduct_id:
            try:
                rtsproduct = RTSProduct.objects.get(pk=rtsproduct_id)
            except RTSProduct.DoesNotExist:
                return Response(
                    {"message": "RTS Product not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            OrderProduct.objects.create(order=open_order, rtsproduct=rtsproduct)

            open_order.total_price = self.calculate_total_price(open_order)
            open_order.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        # Handle creating a CusRequest and adding it to the cart
        cusproduct_id = request.data.get("cusproduct_id")
        if cusproduct_id:
            try:
                cusproduct = CusProduct.objects.get(pk=cusproduct_id)
            except CusProduct.DoesNotExist:
                return Response(
                    {"message": "Custom Product not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            eyes_id = request.data.get("eyes_id")
            color1_id = request.data.get("color1_id")
            color2_id = request.data.get("color2_id")

            try:
                eyes = Eyes.objects.get(pk=eyes_id) if eyes_id else None
                color1 = Color.objects.get(pk=color1_id)
                color2 = Color.objects.get(pk=color2_id) if color2_id else None
            except (Eyes.DoesNotExist, Color.DoesNotExist):
                return Response(
                    {"message": "Invalid eyes or color data."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cusrequest = CusRequest.objects.create(
                cus_product=cusproduct,
                eyes=eyes,
                customer=current_user,
                color1=color1,
                color2=color2,
            )

            OrderProduct.objects.create(order=open_order, cusrequest=cusrequest)

            open_order.total_price = self.calculate_total_price(open_order)
            open_order.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"message": "No product data provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(customer=current_user, emailed=False)
        except Order.DoesNotExist:
            return Response(
                {"message": "No open order found."}, status=status.HTTP_404_NOT_FOUND
            )

        order_products = OrderProduct.objects.filter(order=open_order)
        order_product_serializer = CartItemSerializer(order_products, many=True)

        subtotal = sum(
            (op.rtsproduct.price if op.rtsproduct else op.cusrequest.cus_product.price)
            for op in order_products
        )

        cart_data = {
            "order_id": open_order.id,
            "subtotal": subtotal,
            "shipping_cost": self.shipping_cost,
            "total_price": subtotal + self.shipping_cost,
            "order_products": order_product_serializer.data,
        }

        return Response(cart_data)

    @action(methods=["post"], detail=False)
    def complete(self, request):
        current_user = Customer.objects.get(user=request.auth.user)
        try:
            order_to_complete = Order.objects.get(
                customer=current_user, payment__isnull=True
            )
            order_products = OrderProduct.objects.filter(order=order_to_complete)

            subject = "New Order Received"
            message = f"A new order has been placed by {current_user.user.first_name} {current_user.user.last_name}.\n email: {current_user.user.email}\n shipping address: {current_user.address}\nOrder Details:\n"
            subtotal = 0
            for order_product in order_products:
                if order_product.rtsproduct:
                    rts_product = order_product.rtsproduct

                    RTSSold.objects.create(
                        name=rts_product.name,
                        price=rts_product.price,
                        order=order_to_complete,
                    )

                    product_name = order_product.rtsproduct.name
                    product_price = order_product.rtsproduct.price

                    rts_product.delete()
                else:
                    product_name = order_product.cusrequest.cus_product.name
                    product_price = order_product.cusrequest.cus_product.price
                message += f"{product_name}\nQuantity: 1\nPrice: ${product_price}\n\n"
                subtotal += product_price

            message += f"Subtotal: ${subtotal}\n"
            message += f"Shipping: ${self.shipping_cost}\n"
            message += f"Total Price: ${subtotal + self.shipping_cost}"

            send_mail(
                subject,
                message,
                "hookdbykim@gmail.com",
                ["hookdbykim@gmail.com", current_user.user.email],
                fail_silently=False,
            )

            order_to_complete.emailed = True
            order_to_complete.save()

            return Response(
                {"message": "Order placed successfully."}, status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=["delete"], url_path="clear-cart", detail=False)
    def delete(self, request):
        current_user = Customer.objects.get(user=request.auth.user)
        open_order = Order.objects.get(customer=current_user, payment=None)

        OrderProduct.objects.filter(order=open_order).delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
