from django.contrib import admin
from django.urls import path,include
from django.urls import *
from . import guard

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('accounts.urls')),
    path('servicios/', include('services.urls')),
    path('clientes/', include('client.urls')),
    path('auth/', include('login.urls')),
    
    ######## LOGIN API REST ########
    path('api/', include('api.urls')),
    ######### PAGES #################
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
]

handler404 = guard.handler404
handler505 = guard.handler505
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


