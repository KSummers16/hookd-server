from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from hookdapi.models import Color
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ["id", "name"]


class ColorView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        colors = Color.objects.all()
        serializer = ColorSerializer(colors, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            color = Color.objects.get(pk=pk)
            serializer = ColorSerializer(color, context={"request": request})
            return Response(serializer.data)
        except Color.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
