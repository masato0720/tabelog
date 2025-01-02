from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    user_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="ユーザー名前"
    )
    hurigana = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="フリガナ"
    )
    zip_code = models.CharField(
        max_length=16, null=True, blank=True, verbose_name="郵便番号"
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="住所"
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="電話番号"
    )
    birthday = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="誕生日"
    )
    job = models.CharField(max_length=255, null=True, blank=True, verbose_name="職業")

    
    # 有料会員情報
    subscription = models.BooleanField(null=True, default=False, verbose_name="有料会員")
    card_name = models.CharField(max_length=128, null=True, blank=True,verbose_name='カード名義')
    card_number = models.CharField(max_length=128, null=True, blank=True,verbose_name='カード番号')

    
    class Meta:
        verbose_name = '会員一覧'
        verbose_name_plural = "会員一覧"


    def __str__(self):
        return self.username
