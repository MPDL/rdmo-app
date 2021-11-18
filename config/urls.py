from django.contrib import admin
from django.urls import include, path

from rdmo.core.views import about, home

from rdmo_theme.views import impressum, privacy_policy, FAQs, quickstart, login_form_sso

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),

    path('', include('rdmo.core.urls')),
    path('api/v1/', include('rdmo.core.urls.v1')),
    path('api/v1/', include('rdmo.core.urls.swagger')),

    path('admin/', admin.site.urls),

    path('impressum/', impressum, name='impressum'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('FAQs/', FAQs, name='FAQs'),
    path('quickstart/', quickstart, name='quickstart'),
    path('shibboleth-ds/', login_form_sso, name='login_form_sso'),
]

handler400 = 'rdmo.core.views.bad_request'
handler403 = 'rdmo.core.views.forbidden'
handler404 = 'rdmo.core.views.not_found'
handler500 = 'rdmo.core.views.internal_server_error'
