from django.contrib import admin

from authorization.models import User

# Register your models here.

# admin.site.register(User)

@admin.register(User)
class AuthorizationUserAdmin(admin.ModelAdmin):
    # 设置需要被屏蔽的属性
    exclude = ['open_id']
    pass