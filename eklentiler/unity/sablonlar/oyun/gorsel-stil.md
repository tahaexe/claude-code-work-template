# Görsel Stil Rehberi: ‹Çalışma adı›
<!-- Oyunun görsel kimliği. Claude UI, sahne ve varlık işlerinden önce okur, ekran görüntülerini buna göre kontrol eder. Kısa tut: kararlar, örnekler, sayılar. Zevk kararı kullanıcınındır; Claude bu belgeye uyumu kontrol eder. Doldurulan belge: docs/ai/tasarim/gorsel-stil.md, HAFIZA dizinine eklenir. -->

**Genel his:** ‹3-5 kelime, ör. "sıcak, sade, el yapımı"› <!-- oyun özetindeki "Sanat ve ses yönü" satırının ayrıntısı -->
**Referanslar:** ‹2-3 oyun ya da görsel; bunlardan neyi alıyoruz, neyi almıyoruz›

## Renk paleti
<!-- Kodlarıyla yaz; yeni bir renk önce buraya eklenir. Metin ile zemini arasında okunur kontrast olmalı (en az 4,5:1). -->
| Rol | Renk | Kod | Nerede |
|---|---|---|---|
| Ana | ‹…› | ‹#…› | ‹butonlar, vurgu› |
| İkincil | ‹…› | ‹#…› | ‹…› |
| Zemin | ‹…› | ‹#…› | ‹paneller› |
| Metin | ‹…› | ‹#…› | ‹…› |
| Başarı / uyarı / tehlike | ‹…› | ‹#… / #… / #…› | ‹…› |

## Yazı tipleri
<!-- En fazla 2 font ailesi. Türkçe karakterler (ğ ü ş ı İ ö ç) ve oyunun desteklediği diğer diller font atlasında olmalı. -->
| Kullanım | Font (TMP font asset) | Boyut | Kalınlık |
|---|---|---|---|
| Başlık | ‹…› | ‹…› | ‹…› |
| Gövde metni | ‹…› | ‹…› | ‹…› |
| Sayılar (skor, para) | ‹…› | ‹…› | ‹…› |
| En küçük okunur boyut | — | ‹ör. telefonda 28 px› | — |

## Arayüz dili
- **Köşe ve kenar:** ‹ör. 16 px yuvarlak köşe, kenarlık yok›
- **Boşluk ızgarası:** ‹ör. 8 px'in katları›
- **Buton durumları:** ‹normal, basılı ve pasif hâl nasıl görünür›
- **İkonlar:** ‹dolu ya da çizgi, kalınlık, boyut›
- **Paneller ve pencereler:** ‹zemin, gölge, açılış animasyonu›

## Sahne görünümü
- **Işık ve gölge:** ‹…›
- **Sis ve atmosfer:** ‹…›
- **Görüntü efektleri (post-processing):** ‹bloom, renk ayarı, vinyet…›
- **Kamera:** ‹açı, mesafe, görüş alanı›

## Hareket dili
- **Süreler:** ‹ör. arayüz geçişleri 0,2 sn, ödül animasyonları 0,6 sn›
- **Yumuşatma (easing):** ‹…›
- **Geri bildirim (juice):** ‹sarsıntı, parçacık ve ses ne zaman, ne kadar›

## Yapılmayacaklar
<!-- Stili bozan şeyler, ör. "saf siyah metin yok", "ikiden fazla font yok", "neon renk yok". -->
- ‹…›
