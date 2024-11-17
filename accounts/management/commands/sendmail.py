from typing import Any
from django.core.management.base import BaseCommand
from django.core.mail import BadHeaderError, send_mail


""" メール================================== """
class Command(BaseCommand):
    help = "テストコマンド3"
    def handle(self, *args, **options):
        print('test3')
        """題名"""
        subject = "題名"
        """本文"""
        message = "本文です¥nこんにちは。メールを送信しました"
        """送信元メールアドレス"""
        from_email = "xxxxxx"
        """宛先メールアドレス"""
        recipient_list = [
            "xxxxxxx"
        ]
        send_mail(subject, message, from_email, recipient_list)