from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import RTSProduct, Eyes, Category
import base64
from django.core.files.base import ContentFile
from ..permissions import IsAdminUser


class RTSProductSerializer(serializers.ModelSerializer):
    """JSON serializer for Ready to Sell products"""

    class Meta:
        model = RTSProduct
        fields = (
            "id",
            "name",
            "price",
            "description",
            "category",
            "image",
            "eyes",
            "pattern",
            "yarn",
        )
        depth = 1


class RTSProductsView(ViewSet):
    def list(self, request):
        rts_products = RTSProduct.objects.all()
        serializer = RTSProductSerializer(
            rts_products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            rts_product = RTSProduct.objects.get(pk=pk)
            serializer = RTSProductSerializer(rts_product, context={"request": request})
            return Response(serializer.data)
        except RTSProduct.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        permission_classes = [IsAdminUser]
        if not request.user.customer.is_admin:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            new_rtsproduct = RTSProduct()
            new_rtsproduct.name = request.data["name"]
            new_rtsproduct.price = request.data["price"]
            new_rtsproduct.description = request.data["description"]
            new_rtsproduct.category = Category.objects.get(
                pk=request.data["category_id"]
            )

            eyes_id = request.data.get("eyes_id")
            if eyes_id is not None:
                try:
                    new_rtsproduct.eyes = Eyes.objects.get(pk=eyes_id)
                except Eyes.DoesNotExist:
                    return Response(
                        {"error": "Invalid eyes_id"}, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                new_rtsproduct.eyes = None
            new_rtsproduct.pattern = request.data["pattern"]
            new_rtsproduct.yarn = request.data["yarn"]

            if "image_path" in request.data:
                format, imgstr = request.data["image_path"].split(";base64,")
                ext = format.split("/")[-1]
                data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'{new_rtsproduct.id}-{request.data["name"]}.{ext}',
                )
                new_rtsproduct.image_path = data

            new_rtsproduct.save()
            serializer = RTSProductSerializer(
                new_rtsproduct, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
