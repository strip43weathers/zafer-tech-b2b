import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import EnerjiHesaplayiciAyar, Kategori, Proje, BlogYazisi
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required


# YENİ: Otomatik Türkçe Karakter Temizleyici Motor
def clear_turkish_chars(text):
    if not text:
        return text
    replacements = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S',
        'ğ': 'g', 'Ğ': 'G', 'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }
    for tr, eng in replacements.items():
        text = text.replace(tr, eng)
    return text


def ana_sayfa(request):
    hesaplayici_ayar = EnerjiHesaplayiciAyar.objects.first()
    if not hesaplayici_ayar:
        hesaplayici_ayar = EnerjiHesaplayiciAyar.objects.create(guncel_kwh_fiyati=2.50, ortalama_tasarruf_orani=60)

    kategoriler = Kategori.objects.all()
    projeler = Proje.objects.all()

    context = {
        'hesaplayici_ayar': hesaplayici_ayar,
        'kategoriler': kategoriler,
        'projeler': projeler,
    }
    return render(request, 'core/index.html', context)


def pdf_olustur(request):
    proje_id_listesi = request.GET.get('ids', '')

    if proje_id_listesi:
        ids = proje_id_listesi.split(',')
        orijinal_projeler = Proje.objects.filter(id__in=ids)

        # Veritabanından gelen yazıları PDF'e basmadan önce İngilizce karaktere çeviriyoruz
        secilen_projeler = []
        for p in orijinal_projeler:
            p.baslik = clear_turkish_chars(p.baslik)
            p.aciklama = clear_turkish_chars(p.aciklama)
            if p.kategori:
                p.kategori.ad = clear_turkish_chars(p.kategori.ad)
            secilen_projeler.append(p)
    else:
        secilen_projeler = []

    logo_tam_yol = os.path.join(str(settings.BASE_DIR), 'core', 'static', 'core', 'images', 'logo.png').replace('\\',
                                                                                                                '/')

    template = get_template('core/pdf_sablonu.html')

    context = {
        'projeler': secilen_projeler,
        'logo_yolu': logo_tam_yol
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Zafer_Tech_Ozel_Katalog.pdf"'

    # Encoding'e gerek kalmadı, varsayılan olarak çalışacak
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF oluşturulurken bir hata meydana geldi.')
    return response


@login_required(login_url='/login/')
def musteri_portali(request):
    musteri_projeleri = Proje.objects.filter(musteri=request.user)
    context = {
        'projeler': musteri_projeleri
    }
    return render(request, 'core/portal.html', context)


def proje_detay(request, proje_id):
    secilen_proje = get_object_or_404(Proje, id=proje_id)
    context = {
        'proje': secilen_proje
    }
    return render(request, 'core/proje_detay.html', context)


def blog_liste(request):
    # Sadece 'yayinda_mi' işaretli olanları getir ve tarihe göre sırala
    yazilar = BlogYazisi.objects.filter(yayinda_mi=True).order_by('-olusturulma_tarihi')
    context = {
        'yazilar': yazilar
    }
    return render(request, 'core/blog_liste.html', context)

def blog_detay(request, blog_id):
    # Yazı bulunamazsa veya yayında değilse 404 ver
    yazi = get_object_or_404(BlogYazisi, id=blog_id, yayinda_mi=True)
    context = {
        'yazi': yazi
    }
    return render(request, 'core/blog_detay.html', context)