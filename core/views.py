import os
from django.conf import settings
from django.shortcuts import render
from .models import EnerjiHesaplayiciAyar, Kategori, Proje
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def ana_sayfa(request):
    hesaplayici_ayar = EnerjiHesaplayiciAyar.objects.first()
    if not hesaplayici_ayar:
        hesaplayici_ayar = EnerjiHesaplayiciAyar.objects.create(guncel_kwh_fiyati=2.50, ortalama_tasarruf_orani=60)

    # Veritabanındaki tüm kategorileri ve projeleri çekiyoruz
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
        secilen_projeler = Proje.objects.filter(id__in=ids)
    else:
        secilen_projeler = []

    # LOGO YOLUNU BULUYORUZ: İşletim sistemindeki tam dosya yolunu alıyoruz
    logo_tam_yol = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'images', 'logo.png')

    template = get_template('core/pdf_sablonu.html')

    # logo_tam_yol değişkenini de context içine ekliyoruz ki HTML bunu alabilsin
    context = {
        'projeler': secilen_projeler,
        'logo_yolu': logo_tam_yol
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Zafer_Tech_Ozel_Katalog.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF oluşturulurken bir hata meydana geldi.')
    return response


@login_required(login_url='/login/')
def musteri_portali(request):
    # Veritabanından, SADECE o an giriş yapmış olan kişiye (request.user) atanmış projeleri çekiyoruz.
    # Başka müşterinin projesini kesinlikle göremez.
    musteri_projeleri = Proje.objects.filter(musteri=request.user)

    context = {
        'projeler': musteri_projeleri
    }
    return render(request, 'core/portal.html', context)


def proje_detay(request, proje_id):
    # Tıklanan projeyi veritabanından buluyoruz, yoksa 404 hatası verir
    secilen_proje = get_object_or_404(Proje, id=proje_id)

    context = {
        'proje': secilen_proje
    }
    return render(request, 'core/proje_detay.html', context)