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


# class CusRequestView(ViewSet):
#     # def create(self, request):
#     #     cus_product_id = request.data["cus_product_id"]
#     #     eyes_id = request.data["eyes_id"]
#     #     color1_id = request.data["color1_id"]

#     #     customer = Customer.objects.get(user=request.auth.user)

#     #     # Check if color2_id is provided in the request
#     #     if "color2_id" in request.data:
#     #         color2_id = request.data["color2_id"]
#     #     else:
#     #         color2_id = None

#     #     new_request = CusRequest(
#     #         cus_product_id=cus_product_id,
#     #         eyes_id=eyes_id,
#     #         color1_id=color1_id,
#     #         color2_id=color2_id,
#     #         customer=customer,
#     #     )
#     #     new_request.save()
#     #     serializer = CusRequestSerializer(new_request)

#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
