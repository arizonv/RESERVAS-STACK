from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)


if not get_user_model().objects.filter(username='alonso').exists():
    User = get_user_model()
    User.objects.create_superuser('alonso', 'alonso@example.com', 'alonso')
