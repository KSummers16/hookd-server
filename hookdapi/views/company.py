from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from hookdapi.models import Companys
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companys
        fields = ["id", "name"]


class CompanyView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        companys = Companys.objects.all()
        serializer = CompanySerializer(
            companys, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            companys = Companys.objects.get(pk=pk)
            serializer = CompanySerializer(companys, context={"request": request})
            return Response(serializer.data)
        except Companys.DoesNotExist:
            return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
