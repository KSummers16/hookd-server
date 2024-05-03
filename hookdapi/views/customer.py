from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import Customer
from django.contrib.auth.decorators import login_required


class CustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = Customer
        fields = ("id", "user", "email_address", "address", "is_admin")
        depth = 1


class CustomersView(ViewSet):

    @login_required
    def update(self, request, pk=None):

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return HttpResponseServerError(
                "Customer not found", status=status.HTTP_404_NOT_FOUND
            )

        customer.user.name = request.data["name"]
        customer.user.email = request.data["email"]
        customer.address = request.data["address"]
        customer.user.save()
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(user=request.user)
            serializer = CustomerSerializer(customer, context={"request": request})
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return HttpResponseServerError(
                "Customer not found", status=status.HTTP_404_NOT_FOUND
            )
