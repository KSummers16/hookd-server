from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import OrderProduct, Order, Customer


class CartItemSerializer(serializers.ModelSerializer):
    rtsproduct_id = serializers.PrimaryKeyRelatedField(
        source="rtsproduct", read_only=True
    )
    cusrequest_id = serializers.PrimaryKeyRelatedField(
        source="cusrequest", read_only=True
    )

    class Meta:
        model = OrderProduct
        fields = ["id", "rtsproduct_id", "cusrequest_id"]


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

    def delete(self, request, pk=None):
        try:
            customer = Customer.objects.get(user=request.auth.user)
            order_product = OrderProduct.objects.get(pk=pk, order__customer=customer)
            order_product.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except OrderProduct.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
