from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product category"""

    class Meta:
        model = Category
        fields = ("id", "name")


class CategoriesView(ViewSet):
    """Categories for products"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_product_category = Category()
        new_product_category.name = request.data["name"]
        new_product_category.save()

        serializer = CategorySerializer(
            new_product_category, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category"""
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to ProductCategory resource"""
        category = Category.objects.all()

        serializer = CategorySerializer(
            category, many=True, context={"request": request}
        )
        return Response(serializer.data)
