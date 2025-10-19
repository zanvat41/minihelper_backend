import django
import os
from minihelper_backend import settings
from email.mime.text import MIMEText
import smtplib

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minihelper_backend.settings')
django.setup()

def send_mail_test():
    # 创建邮件内容
    msg = MIMEText("邮件通道测试", "plain", "utf-8")
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = settings.EMAIL_TO[0]
    msg['Subject'] = "***Mail Test From Python SMTP***"
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
        print("邮件发送成功")

    except smtplib.SMTPRecipientsRefused as e:
        print(f"收件人被拒绝: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP 错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

if __name__ == '__main__':
    send_mail_test()