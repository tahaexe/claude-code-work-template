# Farklılık Dosyası: ‹Oyun›
<!-- Fikir aşamasında başlar: kanca cümlesi ve ilk 3 tablosu (docs/ai/el-kitabi/proje-kontrol-listesi.md 1.4; ön araştırmanın rakipleri). Kalite kapısında tamamlanır: kancanın alanı, portföy denetimi, App Store notu, ekler (docs/ai/el-kitabi/kalite-kapisi.md). Doldurulan belge: docs/ai/tasarim/farklilik.md; her kapıda o günkü kopyası docs/ai/tasarim/kalite-kapisi/‹sürüm›/farklilik.md. Yalnız doğru olan yazılır (store/facts.md, docs/ai/el-kitabi/metin-denetimi.md). Kör puanlamada hakemlere verilmez. -->

## Kanca
- **Kanca cümlesi:** ‹tür›, ama ‹tek fark›, böylece ‹his›.
- **İngilizcesi** (App Store notu ve mağaza için): "‹genre› where ‹the one thing› so that ‹feeling›."
- **Kancanın alanı** (kapıda puanlamadan önce yazılır; bu alan 5 almalı): ‹İlk 60 saniye · Oynanış hissi · Görsel ve animasyon · Arayüz ve okunurluk · Ses ve titreşim · İçerik ve ilerleme · Mağaza ve portal görselleri · Farklılık›
- **Nerede görünüyor:** ilk 60 saniyede ‹dk:sn, bölüm› · 1. ekran görüntüsünde ‹…› · önizlemenin ilk 3 saniyesinde ‹…›

## İlk 3 rakip
<!-- Türün tam alt türünde en çok oynanan üç oyun: mağaza listeleri ve kurulum sayıları, okunduğu tarihle; genelde ön araştırmanın liderleri. Kapıda aynı üç oyun bizimkiyle aynı cihazda, aynı anlarda kaydedilir. -->
| Oyun | Bağlantı | Kurulum · puan (tarih) | Nasıl incelendi (oynandı, video, mağaza sayfası) |
|---|---|---|---|
| ‹…› | ‹…› | ‹…› | ‹…› |

## Eşitlik · farkımız · eksiğimiz
<!-- Eşitlik: üçünün de yaptığı; fark sayılmaz (süre yok, çok bölüm, ipucu gibi her rakibin söylediği şeyler). Farkımız: üçünde de olmayan somut bir şey, en az 1, tercihen 2; mekanik, tema ya da dünya, kitle ya da meta. Fark yoksa boya değil mekanik, dünya ya da kitle değişir. Eksiğimiz: onlarda olup bizde olmayan; her biri düzeltildi ya da gerekçesiyle kabul edildi. -->
| Eşitlik (üçünün de yaptığı) | Farkımız (üçünde de yok) | Eksiğimiz (düzeltildi / kabul, neden) |
|---|---|---|
| ‹…› | ‹…› | ‹…› |

## Rakip başına üç fark (App Store notu için)
| Rakip | Mekanik | İçerik | Sunum |
|---|---|---|---|
| ‹…› | ‹…› | ‹…› | ‹…› |

## Portföy denetimi (kapıda, stüdyonun öbür oyunlarına karşı)
| Denetim | Sonuç | Kanıt |
|---|---|---|
| Ortak görsel, ses ya da model (`varlik-cakisma.py`) | ‹0 dosya · izin listesindekiler ve nedenleri› | `kalite-kapisi/‹sürüm›/portfoy/varlik-cakisma.txt` |
| Mağaza metni benzerliği (`metin-benzerlik.py`, en çok %25) | ‹en yüksek difflib · 5-gram ve hangi oyunla› | `kalite-kapisi/‹sürüm›/portfoy/metin-benzerlik.txt` |
| Arayüz görünümü | ‹çerçeve, renk, yazı tipi, simgeler, ana ekran düzeni: neyi farklı› | `kalite-kapisi/‹sürüm›/portfoy/arayuz-paftasi.png` |
| Temel hareketin ses efektleri | ‹bu oyuna ait mi› | |
| Hazır proje şablonu | ‹yok · kullanılan varlık paketleri› | |

## App Store inceleme notu (Review Notes, İngilizce)
<!-- Her gönderimde. Sürümün olağan notları (hesap yok, reklamlar, satın almalar) da eklenir: docs/ai/el-kitabi/app-store-game-center.md §7. Gerçekler, pazarlama yok. -->
```text
What is distinct: <hook sentence>.
Compared with the three most-played games of its genre:
1. <Rival 1>: <mechanic difference>; <content difference>; <presentation difference>.
2. <Rival 2>: <...>; <...>; <...>.
3. <Rival 3>: <...>; <...>; <...>.
All code, art and audio were made for this game; no template was used. Engine and SDKs: <engine and version>, <SDK list>.
The distinct mechanic appears at <0:20> of the attached video (level <2>).
```

## Ekler (App Review Information › Attachment)
- [ ] Açılıştan kancaya 30-60 sn kayıt: ‹dosya›
- [ ] Açıklamalı 2 ekran görüntüsü: ‹dosya›, ‹dosya›

## Gönderim kaydı
<!-- App Store'da hesap başına incelemede tek yeni oyun; sıradaki, öncekinin onayından sonra ve 1-2 hafta arayla; aynı gün toplu gönderim yok. 4.3 gelirse önce Resolution Center'da hangi bulgunun geçerli olduğu sorulur (ikili dosya, metin ya da fikir); aynı derleme gerekçeyle yeniden gönderilmez; tek itiraz yalnız yeni kanıtla. Portala yeniden gönderim yalnız KAPI: GEÇTİ'den sonra, değişiklik listesiyle. -->
| Tarih | Mağaza ya da portal | Sürüm | Sonuç | Not |
|---|---|---|---|---|
| ‹YYYY-AA-GG› | ‹…› | ‹…› | ‹…› | ‹…› |
