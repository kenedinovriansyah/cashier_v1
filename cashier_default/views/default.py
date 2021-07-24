import json
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class DefaultAPIView(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        with open("cashier_default/prefix/employe.json", "r") as r:
            e = json.loads(r.read())
        with open("cashier_default/prefix/gender.json", "r") as r:
            g = json.loads(r.read())
        data = {}
        data['gender'] = g
        data['employe'] = e
        return Response(data, status=status.HTTP_200_OK)