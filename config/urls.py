import debug_toolbar
from django.contrib import admin
from django.urls import include, path

from rdmo.core.views import about, home

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),

    path('', include('rdmo.core.urls')),
    path('api/v1/', include('rdmo.core.urls.v1')),
    path('api/v1/', include('rdmo.core.urls.swagger')),

    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]

handler400 = 'rdmo.core.views.bad_request'
handler403 = 'rdmo.core.views.forbidden'
handler404 = 'rdmo.core.views.not_found'
handler500 = 'rdmo.core.views.internal_server_error'
