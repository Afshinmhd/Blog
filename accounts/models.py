from django.db import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError, NotAcceptable
from django.core.cache import cache
from .messages import Messages
from .utils import otp_generate
from rest_framework import status


class Profile(User):

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
            }

    @staticmethod
    def sub_login(username, email, *args, **kwargs):
        if cache.get(f'code_{email}'):
            ttl = cache.ttl(f'code_{email}')
            raise ValidationError({'Error': Messages.TTL_ERROR.value.format(ttl)})
        elif not cache.get(f'username_{email}'):
            cache.set_many(
                {f'username_{email}' : username,
                f'email_{email}': email}, 360)
        code = otp_generate()
        cache.set(f'code_{email}', code, 60)
        return 200, Messages.SEND_CODE.value
        

    @staticmethod
    def confirm(username, email, code, *args, **kwargs):
        if not cache.get(f'username_{email}') == username:
            raise NotAcceptable({'Error': Messages.EDIT_INFORMATION.value})
        elif not cache.get(f'code_{email}') == code:
            raise ValidationError({'Error': Messages.INCORRECT_CODE.value})
        user = User.objects.get_or_create(
            username=username, email=email)
        cache.delete_many([user[0].pk, f'code_{email}'])
        return (status.HTTP_200_OK,
                {'refresh': user[0].tokens()['refresh'],
                'access': user[0].tokens()['access']})

    def login(self, password):
        validate_password = self.check_password(password)
        if not validate_password:
            raise ValidationError({'Error': Messages.INCORRECT_PASSWORD.value})
        else:
            cache.delete(self.pk)
            return (status.HTTP_200_OK,
                {'refresh': self.tokens()['refresh'],
                'access': self.tokens()['access']})

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()
        return 200, Messages.CHANGE_PASSWORD.value

    def logout(self, refresh):
        RefreshToken(refresh).blacklist()
        cached = cache.set(self.pk, 'blocked', 180)
        return 200, Messages.LOGOUT.value