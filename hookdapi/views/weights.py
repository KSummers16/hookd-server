from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from hookdapi.models import Weights
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class WeightsSerializer(serializers.ModelField):
    class Meta:
        model = Weights
        fields = ["id", "name"]


class WeightsView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        weights = Weights.objects.all()
        serializer = WeightsSerializer(weights, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            weights = Weights.objects.get(pk=pk)
            serializer = WeightsSerializer(weights, context={"request": request})
            return Response(serializer.data)
        except Weights.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
