from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('social_django.urls', namespace='social')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('tasks/', include('task.urls')),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

admin.site.site_header = 'Mini To-Do App Admin'
admin.site.site_title = 'Mini To-Do App Administration'
admin.site.index_title = 'Mini To-Do App Administration'
