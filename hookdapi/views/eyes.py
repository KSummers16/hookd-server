from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from hookdapi.models import Eyes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class EyesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eyes
        fields = ["id", "name"]


class EyesView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        eyes = Eyes.objects.all()
        serializer = EyesSerializer(eyes, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            eyes = Eyes.objects.get(pk=pk)
            serializer = EyesSerializer(eyes, context={"request": request})
            return Response(serializer.data)
        except Eyes.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
