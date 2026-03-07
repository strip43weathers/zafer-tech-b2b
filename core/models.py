from django.db import models
from django.contrib.auth.models import User

class EnerjiHesaplayiciAyar(models.Model):
    guncel_kwh_fiyati = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=2.50, # Varsayılan elektrik birim fiyatı (TL)
        verbose_name="Güncel Elektrik Birim Fiyatı (TL/kWh)",
        help_text="Hesaplama aracında kullanılacak güncel 1 kWh elektrik fiyatını girin."
    )
    ortalama_tasarruf_orani = models.IntegerField(
        default=60, # Klasik aydınlatmaya göre LED'in sağladığı ortalama tasarruf %
        verbose_name="Ortalama LED Tasarruf Oranı (%)",
        help_text="Zafer Tech sistemlerinin eski sistemlere göre sağladığı ortalama % tasarruf."
    )

    class Meta:
        verbose_name = "Hesaplayıcı Ayarı"
        verbose_name_plural = "Hesaplayıcı Ayarları"

    def __str__(self):
        return f"Güncel Fiyat: {self.guncel_kwh_fiyati} TL | Tasarruf: %{self.ortalama_tasarruf_orani}"

    # Sistemin sadece 1 adet ayar kaydı tutmasını sağlamak için ufak bir hile (Singleton mantığı)
    def save(self, *args, **kwargs):
        self.pk = 1
        super(EnerjiHesaplayiciAyar, self).save(*args, **kwargs)

class Kategori(models.Model):
    ad = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, help_text="URL ve filtreleme için benzersiz isim (Örn: endustriyel)")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.ad


class Proje(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Proje Adı (Örn: Doğuş Oto Kartal)")
    aciklama = models.TextField(blank=True, verbose_name="Kısa Açıklama")
    kategori = models.ForeignKey('Kategori', on_delete=models.CASCADE, related_name='projeler')
    gorsel_url = models.URLField(blank=True, help_text="Geçici test için görsel linki")

    # --- YENİ EKLENEN B2B PORTAL ALANLARI ---
    musteri = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Atanan Müşteri",
                                help_text="Bu projeyi hangi müşteri kendi panelinde görecek?")
    ilerleme_yuzdesi = models.IntegerField(default=0, verbose_name="İlerleme Durumu (%)",
                                           help_text="0 ile 100 arası bir değer girin.")
    son_durum_notu = models.CharField(max_length=255, blank=True, verbose_name="Son Durum Notu",
                                      help_text="Örn: Kablo altyapısı tamamlandı, pano montajına geçiliyor.")
    santiye_fotografi = models.ImageField(
        upload_to='santiye_fotograflari/',
        blank=True,
        null=True,
        verbose_name="Son Durum Fotoğrafı",
        help_text="Müşterinin portalda göreceği güncel şantiye/proje fotoğrafı."
    )

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"

    def __str__(self):
        return self.baslik

class ProjeGorseli(models.Model):
    proje = models.ForeignKey(Proje, on_delete=models.CASCADE, related_name='fotograflar', verbose_name="Ait Olduğu Proje")
    gorsel = models.ImageField(upload_to='proje_galerisi/', verbose_name="Fotoğraf")
    sira = models.IntegerField(default=0, verbose_name="Gösterim Sırası", help_text="Küçük sayı önce gösterilir.")

    class Meta:
        verbose_name = "Proje Görseli"
        verbose_name_plural = "Proje Görselleri"
        ordering = ['sira']

    def __str__(self):
        return f"{self.proje.baslik} - Görsel"


class BlogYazisi(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    ozet = models.TextField(verbose_name="Kısa Özet", help_text="Blog listesinde görünecek kısa açıklama.")
    icerik = models.TextField(verbose_name="İçerik")
    gorsel = models.ImageField(upload_to='blog_gorselleri/', blank=True, null=True, verbose_name="Kapak Görseli")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Yayın Tarihi")
    yayinda_mi = models.BooleanField(default=True, verbose_name="Yayında mı?", help_text="Taslak olarak kaydetmek isterseniz işareti kaldırın.")

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-olusturulma_tarihi'] # En yeni yazılar en üstte görünsün

    def __str__(self):
        return self.baslik

