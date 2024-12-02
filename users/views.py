from users.models import User
from users.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="엔드포인트 설명",
        request_body=UserRegistrationSerializer,
        responses={
            200: "ggooooood",
            400: '잘못된 요청'
        }
    )
    def post(self, req):
        serializer = UserRegistrationSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="엔드포인트 설명",
        request_body=UserLoginSerializer,
        responses={
            200: "good",
            400: '잘못된 요청'
        }
    )
    def post(self,req):
        email = req.data['email']
        password = req.data['password']

        user = User.objects.filter(email=email).first()

        if not user.check_password(password):
            print("ㄹㅇ 잘못됨")
            # raise AuthenticationFailed('Incorrect password')
            return Response({"messege": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(req.data)