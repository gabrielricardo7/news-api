from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from user.models import User
from user.permissions import UserPermission
from user.serializers import UserSerializer, LoginSerializer


class SignUpView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def post(self, request: Request):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, _: Request):
        users = User.objects.all()
        serialized = UserSerializer(instance=users, many=True)

        return Response({"users": serialized.data}, status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)

        if not user:
            return Response(
                {"detail": "invalid cpf or password"},
                status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        name = user.__dict__["first_name"]

        return Response(
            {"token": token.key, "user": name},
            status.HTTP_200_OK,
        )


def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def show_ip_address(request):
    user_ip = get_ip_address(request)
    return render(request, "output.html", {"user_ip": user_ip})
