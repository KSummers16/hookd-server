from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import OrderProduct, Order, Customer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ["id", "rts_product", "cus_request", "quantity"]


class CartItem(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            # line_item = OrderProduct.objects.get(pk=pk)
            current_user = Customer.objects.get(user=request.auth.user)
            # line_item = OrderProduct.objects.get(pk=pk, order__customer=customer)
            line_items = OrderProduct.objects.filter(cart__customer=current_user)

            serializer = CartItemSerializer(line_items, context={"request": request})

            return Response(serializer.data)

        except OrderProduct.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
