from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    if sender.name == 'accounts':
        User = get_user_model()
        if not User.objects.filter(username='alonso').exists():
            User.objects.create_superuser('alonso', 'alonso@example.com', 'alonso')
