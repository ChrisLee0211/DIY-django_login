from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username)|Q(mobile=username)#你可以自定义已经在model中设置好的字段作为登录验证逻辑，这里是username和mobile
            )
            if user.check_password(password):
                return  user
        except Exception as e:
            return None