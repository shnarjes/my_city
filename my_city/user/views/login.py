from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token
from django.utils import timezone
from user.serializers import UserSerializer
from user.models import User
from user.models import OTP
from user.utils import create_end_time, randN, end_time, send_sms_otp



class LoginpassAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        user = User.objects.filter(phone=request.data['phone'])
        if user.exists():
            user = User.objects.get(phone=request.data['phone'])
            serializer = self.get_serializer(user)
            token, created = Token.objects.get_or_create(user=user)
            if request.data['password'] == user.password :
                user.is_active = True
                user.save()
                context = (token.key, serializer.data)
                return(Response(context, status=status.HTTP_200_OK))
            else:
                return (Response("The password is wrong.", status=status.HTTP_400_BAD_REQUEST))
                
        else:
            return (Response("user with this Phone not exists.", status=status.HTTP_400_BAD_REQUEST))


class LogincodeAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        user = User.objects.filter(phone=request.data['phone'])
        if user.exists():
            user = User.objects.get(phone=request.data['phone'])
            obj = OTP.objects.filter(user=user, type=2)
            if obj.exists():
                obj = OTP.objects.get(user=user, type=2)
                count_otp = obj.number_error_5time
                if count_otp < 5:
                    obj.code = randN(6)
                    obj.exp_time = create_end_time()
                    obj.exp_time_error_send = end_time()
                    obj.number_error_5time = count_otp + 1
                    obj.save()
                    send_sms_otp(mobile=user.phone, token=obj.code)
                    return (Response(obj.code, status=status.HTTP_200_OK))
                else:
                    if obj.exp_time_error_send < timezone.now():
                        obj.code = randN(6)
                        obj.exp_time = create_end_time()
                        obj.exp_time_error_send = end_time()
                        obj.number_error_5time = 0
                        obj.save()
                        send_sms_otp(mobile=user.phone, token=obj.code)
                        return (Response(obj.code, status=status.HTTP_200_OK))
                    else:
                        return(Response('Try again an hour', status=status.HTTP_429_TOO_MANY_REQUESTS))
            else:
                obj = OTP.objects.create(
                    code=randN(6),
                    exp_time=create_end_time(),
                    exp_time_error_send=end_time(),
                    user=user,
                    type=2,
                    number_error_3time=0,
                    number_error_5time=1
                )
                send_sms_otp(mobile=user.phone, token=obj.code)
                return (Response(obj.code, status=status.HTTP_200_OK))
        else:
            return (Response("user with this Phone not exists.", status=status.HTTP_400_BAD_REQUEST))