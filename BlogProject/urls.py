
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'
handler403 = 'accounts.views.custom_403'
handler400 = 'accounts.views.custom_400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('home.urls', namespace='home')),
    path('comments/', include('comments.urls', namespace='comments')),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)