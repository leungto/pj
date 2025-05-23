from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Users(models.Model):
    username = models.CharField(verbose_name='姓名', max_length=50)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    hashed_password = models.CharField(blank=True, null=True)
    role = models.CharField(verbose_name='角色', max_length=20, default='user')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'users'
    def check_password(self, raw_password):
        print(f"raw_password: {raw_password}")
        print(f"hashed_password: {self.hashed_password}")
        return check_password(raw_password, self.hashed_password)