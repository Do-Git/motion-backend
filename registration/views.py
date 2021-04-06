
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from rest_framework.generics import GenericAPIView

from registration.models import Registration
from user_profile.models import UserProfile
from rest_framework.response import Response

User = get_user_model()


class RegistrationView(GenericAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_user = User(username=email, email=email, is_active=False)
        new_user.save()
        new_user_profile = UserProfile(user=new_user)
        new_user_profile.save()
        registration = Registration(user=new_user_profile)
        registration.save()
        send_mail(
            'Verification code',
            f'Please confirm the verification code {registration.code}',
            'backpacker.propulsion@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response(status=200)

class ValidationView(GenericAPIView):
    serializer_class = UserProfile
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            check_registration = Registration.objects.get(code=code, user__user__email=email)
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            password = request.data.get('password')
            username = request.data.get('username')
            check_registration.user.user.username = username
            check_registration.user.user.set_password(password)
            check_registration.user.user.email = email
            check_registration.user.user.is_active = True
            check_registration.user.user.save()
            check_registration.user.first_name = first_name
            check_registration.user.last_name = last_name
            check_registration.user.save()
            check_registration.code_used = True
            check_registration.save()
            return Response(self.get_serializer(check_registration.user).data)
        except ObjectDoesNotExist:
            return Response(data='email or code are wrong', status=400)
        return Response(status=200)