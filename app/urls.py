from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('tasks/', include('task.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

admin.site.site_header = 'Mini To-Do App Admin'
admin.site.site_title = 'Mini To-Do App Administration'
admin.site.index_title = 'Mini To-Do App Administration'
