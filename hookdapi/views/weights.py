from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from hookdapi.models import Weight
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)


class WeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ["id", "name", "ply"]


class WeightsView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        weights = Weight.objects.all()
        serializer = WeightsSerializer(weights, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            weights = Weight.objects.get(pk=pk)
            serializer = WeightsSerializer(weights, context={"request": request})
            return Response(serializer.data)
        except Weight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # def create(self, request):
    #     if not request.user.is_authenticated:
    #         return Response(
    #             {"error": "Authentication is required."},
    #             status=status.HTTP_401_UNAUTHORIZED,
    #         )
    #     elif not request.user.customer.is_admin:
    #         return Response(
    #             {"error": "You do not have permission to perform this action"},
    #             status=status.HTTP_403_FORBIDDEN,
    #         )
    #     serializer = WeightsSerializer(data=request.data, context={"request": request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
