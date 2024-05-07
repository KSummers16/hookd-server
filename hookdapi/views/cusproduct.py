from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import CusProduct, Category
import base64
from django.core.files.base import ContentFile
from ..permissions import IsAdminUser


class CusProductSerializer(serializers.ModelSerializer):
    """JSON serializer for Ready to Sell products"""

    class Meta:
        model = CusProduct
        fields = (
            "id",
            "name",
            "price",
            "image",
            "eyes",
            "category",
            "pattern",
            "yarn",
        )
        depth = 1


class CusProductView(ViewSet):

    def list(self, request):
        cus_products = CusProduct.objects.all()
        serializer = CusProductSerializer(
            cus_products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            cus_product = CusProduct.objects.get(pk=pk)
            serializer = CusProductSerializer(cus_product, context={"request": request})
            return Response(serializer.data)
        except CusProduct.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        permission_classes = [IsAdminUser]
        if not request.user.customer.is_admin:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            new_cusproduct = CusProduct()
            new_cusproduct.name = request.data["name"]
            new_cusproduct.price = request.data["price"]
            new_cusproduct.category = Category.objects.get(
                pk=request.data["category_id"]
            )
            new_cusproduct.pattern = request.data["pattern"]
            new_cusproduct.yarn = request.data["yarn"]

            if "image_path" in request.data:
                format, imgstr = request.data["image_path"].split(";base64,")
                ext = format.split("/")[-1]
                data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'{new_cusproduct.id}-{request.data["name"]}.{ext}',
                )
                new_cusproduct.image_path = data

            new_cusproduct.save()
            serializer = CusProductSerializer(
                new_cusproduct, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
