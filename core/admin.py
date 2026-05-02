from django.contrib import admin
from .models import EnerjiHesaplayiciAyar, Kategori, Proje, ProjeGorseli, BlogYazisi

@admin.register(EnerjiHesaplayiciAyar)
class EnerjiHesaplayiciAyarAdmin(admin.ModelAdmin):
    list_display = ['guncel_kwh_fiyati', 'ortalama_tasarruf_orani']

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('ad',)} # Adı yazarken slug otomatik dolsun

class ProjeGorseliInline(admin.TabularInline):
    model = ProjeGorseli
    extra = 1 # Ekstradan 1 boş fotoğraf yükleme satırı gösterir

@admin.register(Proje)
class ProjeAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'kategori', 'musteri', 'ilerleme_yuzdesi', 'sira']
    list_filter = ['kategori', 'musteri']
    list_editable = ['ilerleme_yuzdesi', 'sira']
    inlines = [ProjeGorseliInline] # Galeriyi projenin içine gömdük!
@admin.register(BlogYazisi)
class BlogYazisiAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'olusturulma_tarihi', 'yayinda_mi']
    list_filter = ['yayinda_mi', 'olusturulma_tarihi']
    search_fields = ['baslik', 'icerik']


admin.site.site_header = "Zafer Tech Yönetim Paneli"
admin.site.site_title = "Zafer Tech Portal"
admin.site.index_title = "İçerik ve Sistem Yönetimine Hoş Geldiniz"