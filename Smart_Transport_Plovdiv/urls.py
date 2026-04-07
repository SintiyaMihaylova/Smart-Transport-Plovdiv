from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    path('', TemplateView.as_view(template_name='common/home.html'), name='home'),

    path('transport/', include('transport.urls')),
    path('stations/', include('stations.urls')),

    path('reports/', include('reports.urls')),
    path('subscriptions/', include('subscriptions.urls')),
]
handler404 = 'Smart_Transport_Plovdiv.views.error_404'
handler500 = 'Smart_Transport_Plovdiv.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)