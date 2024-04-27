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
    Cart,
    Eyes,
    Color,
)
from .rtsproduct import RTSProductSerializer
import datetime


class CartView(viewsets.ViewSet):
    def create(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(customer=current_user, payment__isnull=True)
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
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"message": "No product data provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(customer=current_user, payment__isnull=True)
        except Order.DoesNotExist:
            return Response(
                {"message": "No open order found."}, status=status.HTTP_404_NOT_FOUND
            )

        order_products = OrderProduct.objects.filter(order=open_order)
        order_product_serializer = CartItemSerializer(order_products, many=True)

        cart_data = {
            "order_id": open_order.id,
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
            payment_id = request.data.get("payment_id")

            order_to_complete.payment_id = payment_id
            order_to_complete.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
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
