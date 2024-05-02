from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hookdapi.models import CusProduct, CusRequest, Eyes, Color, Customer


class CusRequestSerializer(serializers.ModelSerializer):
    """JSON serializer for Ready to Sell products"""

    class Meta:
        model = CusRequest
        fields = (
            "id",
            "cus_product",
            "customer",
            "eyes",
            "color1",
            "color2",
        )
        depth = 1


class CusRequestView(ViewSet):
    def list(self, request):
        cus_request = CusRequest.objects.all()
        serializer = CusRequestSerializer(
            cus_request, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            cus_request = CusRequest.objects.get(pk=pk)
            serializer = CusRequestSerializer(cus_request, context={"request": request})
            return Response(serializer.data)
        except CusRequest.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
