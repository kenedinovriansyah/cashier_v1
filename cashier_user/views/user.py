from django.conf import settings
from rest_framework import serializers, status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from cashier_user.serializer.user import UserSerializers, UserModelSerializer
from django.utils.translation import gettext as _


class UserModelViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    fields_serializer = UserSerializers

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                permissions.AllowAny,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.fields_serializer(data=request.data)
        serializer.context["types"] = "create"
        message = _("Accounts has been created")
        _s = status.HTTP_201_CREATED
        if request.data.get("types") == "reset":
            serializer.context["types"] = "reset"
            message = _(
                "Account has been reset, please check your email inbox for a new password sandi"
            )
            _s = status.HTTP_200_OK
        if serializer.is_valid():
            serializer.save()
            return Response({"message": message}, status=_s)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        check = request.user.accounts_set.first().employe.filter(accounts__public_id=pk)
        if not check.exists():
            return Response(
                {"message": _("Accounts not found")}, status=status.HTTP_404_NOT_FOUND
            )
        if not settings.TEST:
            check.first().delete()
        return Response(
            {"message": _("Employe has been deleted")}, status=status.HTTP_200_OK
        )


class DestroyEmployeManyToMany(APIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    fields_serializer = UserSerializers

    def delete(self, request, objects):
        for i in str(objects).split(","):
            check = self.queryset.filter(id=i).first()
            check.delete()
        return Response(
            {"message": _("Employe has been deletede")}, status=status.HTTP_200_OK
        )


class UpdateEmployeAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    fields_serializer = UserSerializers

    def post(self, request, pk):
        filter = self.queryset.filter(accounts__public_id=pk).first()
        check = request.user.accounts_set.first().employe.filter(
            accounts__public_id=filter.accounts_set.first().public_id
        )
        if not check.exists():
            return Response(
                {"message": _("Accounts not found")}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.fields_serializer(check.first(), data=request.data)
        serializer.context["types"] = "updated"
        if serializer.is_valid():
            serializer.save()
            retrieve = User.objects.filter(accounts__public_id=pk).first()
            return Response(
                {
                    "message": _("Accounts has been updated"),
                    "data": self.serializer_class(retrieve).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountsMeAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    fields_serializer = UserSerializers

    def post(self, request):
        serializer = self.fields_serializer(request.user, data=request.data)
        serializer.context["types"] = "updated"
        message = _("Profile has been updated")
        if request.data.get("types") == "email":
            serializer.context["types"] = "email"
            message = _("Email has been updated")
        elif request.data.get("types") == "password":
            serializer.context["types"] = "password"
            message = _("Password has been updated")
        elif request.data.get("types") == "employe":
            serializer.context["types"] = "employe"
            message = _("Employe has been add")
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": message, "data": self.serializer_class(request.user).data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
