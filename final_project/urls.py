from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('final_project.web.urls')),
                  path('select2/', include("django_select2.urls")),
                  path('chaining/', include('smart_selects.urls')),
                  # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = NotFoundView.get_rendered_view()
