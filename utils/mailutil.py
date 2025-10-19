import logging

import django
import os
from minihelper_backend import settings
from email.mime.text import MIMEText
import smtplib


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minihelper_backend.settings')
django.setup()

logger = logging.getLogger('django')

def send_mail(content, subject):
    # 创建邮件内容
    msg = MIMEText(content, "plain", "utf-8")
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = settings.EMAIL_TO[0]
    msg['Subject'] = subject
    receivers = settings.EMAIL_TO

    try:
        # 连接到 SMTP 服务器
        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.set_debuglevel(1)  # 开启调试模式

        # 登录 SMTP 服务器
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # 发送邮件 - 使用认证的邮箱地址作为发送方
        server.sendmail(settings.EMAIL_HOST_USER, receivers, msg.as_string())

        # 关闭连接
        server.quit()
        logger.info("邮件发送成功")

    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"收件人被拒绝: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP 错误: {e}")
    except Exception as e:
        logger.error(f"其他错误: {e}")