from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def create(self,validated_data):
#         password = validated_data.pop('password',None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None :
#             instance.set_password(password)
#         instance.save()
#         return instance

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    회원가입을 위한 시리얼라이저
    - 사용자 정보 입력 및 초기 계정 생성
    - 입력 데이터 검증
    """
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'phone_num', 'password', 'password_confirm']

    def validate(self, data):
        # 비밀번호 일치 검증
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # 사용자 생성 및 비밀번호 해시
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    로그인을 위한 시리얼라이저
    - 이메일과 비밀번호로 인증
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # 로그인 자격 검증
        user = User.objects.filter(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid login credentials")
        return data


class EmailVerificationSerializer(serializers.Serializer):
    """
    이메일 인증을 위한 시리얼라이저
    - 인증 코드 생성 및 검증
    """
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        # 인증 코드 검증 로직
        verification = Verification.objects.filter(
            email=data['email'],
            code=data['verification_code']
        ).first()

        if not verification:
            raise serializers.ValidationError("Invalid verification code")

        # 인증 완료 후 처리
        user = User.objects.get(email=data['email'])
        user.is_active = True
        user.save()

        # 인증 코드 삭제
        verification.delete()

        return data


class PasswordResetSerializer(serializers.Serializer):
    """
    비밀번호 재설정을 위한 시리얼라이저
    - 비밀번호 변경 및 재설정 로직
    """
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # 비밀번호 일치 검증
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        # 사용자 존재 확인
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError("User not found")

        return data

    def update(self, instance, validated_data):
        # 비밀번호 변경
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance