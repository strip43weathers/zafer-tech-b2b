from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Proje, BlogYazisi

class StaticViewSitemap(Sitemap):
    priority = 1.0 # Ana sayfanın önemi en yüksek
    changefreq = 'weekly'

    def items(self):
        # Sadece arama motorlarının görmesini istediğimiz ana sayfaları yazıyoruz
        return ['ana_sayfa', 'blog_liste']

    def location(self, item):
        return reverse(item)

class ProjeSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Proje.objects.all()

class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Sadece yayında olan blog yazılarını haritaya ekle
        return BlogYazisi.objects.filter(yayinda_mi=True)

    def lastmod(self, obj):
        return obj.olusturulma_tarihi
