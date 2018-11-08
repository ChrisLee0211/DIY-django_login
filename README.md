# DIY-django_login
通过重载django自带的ModelBackend来自定义django登录逻辑，适用于session、cookie、JWT方式

## 使用方法：

- 在settings.py中：
```
AUTHENTICATION_BACKENDS = ('users.views.CustomBackend',)
AUTH_USER_MODEL = 'users.UserProfile'
```
加入以上配置，在setting中指定重载的模块

- models.py中：
```
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

#继承AbstractUser来重写或增加自己需要的字段
class UserProfile(AbstractUser):
    """
    用户
    """

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.username
```
当然，你可以增加任何你需要的字段去作为账号登录验证

- views.py中:
```
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

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
```
别忘了自己配置url去指定View了
