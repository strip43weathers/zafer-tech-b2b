from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, ProjeSitemap, BlogSitemap
# Medya dosyalarını göstermek için gerekli importlar
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

sitemaps = {
    'static': StaticViewSitemap,
    'projeler': ProjeSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ana_sayfa, name='ana_sayfa'),
    path('pdf-indir/', views.pdf_olustur, name='pdf_indir'),
    path('portal/', views.musteri_portali, name='musteri_portali'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('proje/<int:proje_id>/', views.proje_detay, name='proje_detay'),
    path('blog/', views.blog_liste, name='blog_liste'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('blog/<int:blog_id>/', views.blog_detay, name='blog_detay'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Eğer geliştirme modundaysak (DEBUG=True), yüklenen medyaları sunabilmek için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
