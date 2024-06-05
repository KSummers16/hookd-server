import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .lineitem import CartItemSerializer
from hookdapi.models import Order, Customer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    lineitems = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name="lineitem", lookup_field="id"
        )
        fields = ("id", "lineitems", "customer_id", "payment_id", "total_price")


class OrdersView(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, customer=customer)
            serializer = OrderSerializer(order, context={"request": request})
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"message": "the requested order does not exist"},
                stats=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)

        payment = self.request.query_params.get("payment", None)
        if payment is not None:
            orders = orders.filter(payment=payment)

        json_orders = OrderSerializer(orders, many=True, context={"request": request})

        return Response(json_orders.data)
