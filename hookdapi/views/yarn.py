from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from hookdapi.models import Company, Weight, Color
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated,
)
from hookdapi.models import MasterYarn, CustomerYarn, Customer


class MasterYarnSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    weight = serializers.PrimaryKeyRelatedField(queryset=Weight.objects.all())
    base_color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())

    class Meta:
        model = MasterYarn
        fields = (
            "id",
            "name",
            "company",
            "weight",
            "base_color",
            "color_name",
        )
        depth = 1


class MasterYarnView(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        master_yarn = MasterYarn.objects.all()
        serializer = MasterYarnSerializer(
            master_yarn, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            master_yarn = MasterYarn.objects.get(pk=pk)
            serializer = MasterYarnSerializer(master_yarn, context={"request": request})
            return Response(serializer.data)
        except MasterYarn.DoesNotExist:
            return Response(
                {"error": "Master Yarn does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request):
        permission_classes = [IsAdminUser]
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif not request.user.customer.is_admin:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MasterYarnSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        permission_classes = [IsAdminUser]
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif not request.user.customer.is_admin:
            return Response(
                {"error": "You  do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            try:
                master_yarn = MasterYarn.objects.get(pk=pk)
            except MasterYarn.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            master_yarn.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerYarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerYarn
        fields = [
            "id",
            "master_yarn",
            "name",
            "company",
            "weight",
            "base_color",
            "color_name",
            "amount",
            "is_custom",
        ]
        read_only_fields = ["customer", "is_custom"]


class CustomerYarnView(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer = Customer.objects.get(user=request.user)
        customer_yarn = CustomerYarn.objects.filter(customer=customer)
        serializer = CustomerYarnSerializer(
            customer_yarn, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            customer_yarn = CustomerYarn.objects.get(pk=pk, customer__user=request.user)
            serializer = CustomerYarnSerializer(
                customer_yarn, context={"request": request}
            )
            return Response(serializer.data)
        except CustomerYarn.DoesNotExist:
            return Response(
                {"error": "Yarn not found in your stash"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authenticated is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CustomerYarnSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(
                customer=Customer.objects.get(user=request.user), is_custom=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            customer = Customer.objects.get(user=request.user)
            customer_yarn = CustomerYarn.objects.get(pk=pk, customer=customer)
        except CustomerYarn.DoesNotExist:
            return Response(
                {"error": "Yarn not found in your stash"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CustomerYarnSerializer(
            customer_yarn, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            customer = Customer.objects.get(user=request.user)
            customer_yarn = CustomerYarn.objects.get(pk=pk, customer=customer)
            customer_yarn.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomerYarn.DoesNotExist:
            return Response(
                {"error": "Yarn not found in your stash"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def add_from_master(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        master_yarn_id = request.data.get("master_yarn_id")
        amount = request.data.get("amount", 0)

        try:
            master_yarn = MasterYarn.objects.get(id=master_yarn_id)
        except MasterYarn.DoesNotExist:
            return Response(
                {"error": "Master yarn not found"}, status=status.HTTP_404_NOT_FOUND
            )

        customer_yarn, created = CustomerYarn.objects.get_or_create(
            customer=customer,
            master_yarn=master_yarn,
            defaults={
                "name": master_yarn.name,
                "company": master_yarn.company,
                "weight": master_yarn.weight,
                "base_color": master_yarn.base_color,
                "color_name": master_yarn.color_name,
                "amount": amount,
                "is_custom": False,
            },
        )

        if not created:
            customer_yarn.amount += amount
            customer_yarn.save()

        serializer = CustomerYarnSerializer(customer_yarn)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
