# ‹Sistem / mekanik adı›
<!-- Sistem tasarım belgesi (GDD). Doldurulan belge: docs/ai/tasarim/<sistem>.md; HAFIZA dizinine "ne zaman okunmalı" ipucuyla eklenir. Claude belgeyi bölüm bölüm okur: Özet'i her zaman güncel tut. -->

> **Durum:** Taslak / İncelemede / Onaylandı / Uygulandı · **Son güncelleme:** YYYY-AA-GG
> **Katman:** Temel / Çekirdek / Özellik / Sunum · **Öncelik:** MVP / Dikey dilim / Alfa / Tam vizyon · **Bağımlılıklar:** ‹…›

## Özet
‹2-3 cümle: ne, oyuncuya ne yapıyor, neden var. Jargon yok; Claude belgenin gerisini okuyup okumayacağına buna bakarak karar verir.›

## Genel bakış
‹Projeye yeni biri için tek paragraf: ne, oyuncu ne yapıyor, neden var.›

## Oyuncu fantezisi
‹Oyuncu ne HİSSETMELİ? Aşağıdaki tüm ayrıntı kararlarını bu yönlendirir.›

## Ayrıntılı tasarım
### Temel kurallar
<!-- Programcının soru sormadan uygulayabileceği kadar net; sıralı işler numaralı, özellikler madde. -->
1. ‹…›

### Durumlar ve geçişler
| Durum | Giriş koşulu | Çıkış koşulu | Davranış |
|---|---|---|---|
| ‹…› | | | |

### Diğer sistemlerle etkileşim
| Sistem | Giren veri | Çıkan veri | Sahiplik |
|---|---|---|---|
| ‹…› | | | |

## Formüller
<!-- Kullanılan her formül; örnek: -->
`sonuç = temel_değer * (1 + değiştirici_toplamı) * ölçek`

| Değişken | Tür | Aralık | Kaynak | Açıklama |
|---|---|---|---|---|
| ‹…› | | | | |

Beklenen çıktı aralığı: ‹min–max› · Uç durum: ‹ör. değiştirici_toplamı −0,9'da sınırlanır, sonuç negatif olmaz›

## Uç durumlar
| Senaryo | Beklenen davranış | Gerekçe |
|---|---|---|
| ‹…› | | |

## Ayar düğmeleri
<!-- Değerler koda gömülmez; ScriptableObject ya da config'te durur. -->
| Parametre | Şu anki değer | Güvenli aralık | Artırınca | Azaltınca |
|---|---|---|---|---|
| ‹…› | | | | |

## Görsel ve işitsel geri bildirim
| Olay | Görsel | İşitsel | Öncelik |
|---|---|---|---|
| ‹…› | | | |

## Oyun hissi
<!-- NE geri bildirim olduğunu değil, mekaniği kullanmanın NASIL hissettirdiğini tanımlar. Animasyon bütçesini, girdi mimarisini ve zamanlamayı belirlediği için sonradan eklemek pahalıdır. -->
- **His referansı:** ‹Hedef hissi veren belirli bir oyun, mekanik ya da an; isteğe bağlı "böyle olmasın" örneği.›
- **Ağırlık ve tepki:** ‹Ağır/kararlı mı, hafif/tepkisel mi? Hareket ortasında düzeltilebilir mi? Keskin mi yumuşak mı? İvmelenme anlık mı kademeli mi? Başarısızlık adil ve anlaşılır mı?›

| Eylem | En fazla girdi→tepki gecikmesi (ms) | Kare bütçesi (60 fps) | Not |
|---|---|---|---|
| ‹…› | | | |

| Darbe anı | Süre (ms) | Etki | Ayarlanabilir mi? |
|---|---|---|---|
| Vuruş duraklaması | ~80 | ‹…› | |
| Ekran sarsıntısı | ~150 | ‹…› | |

**His kabul kriterleri** (aletsiz test edilebilir; Manuel test listesine gider):
- [ ] ‹ör. Oynayan kimse "süzülüyor", "kaygan", "tepkisiz" demiyor.›

## Tempo ve zorluk eğrisi (isteğe bağlı)
<!-- Talep beceriyle birlikte artsın: fazla kolay sıkar, fazla zor kaygı verir. Her yeni talepten ya da zor bölümden sonra bir nefes molası. Ayrıntı: docs/ai/el-kitabi/adil-zorluk-ve-basarisizlik.md -->
| Aşama / bölüm / gece | Yeni talep | Beklenen oyuncu becerisi | Beklenen hâl (akış / sıkılma / kaygı) |
|---|---|---|---|
| ‹…› | | | |

- **Nefes molaları:** ‹nerede ve nasıl: kolay bölüm, ödül, sakin an›
- **Hız geçişleri (karma oyunlarda):** ‹hızlı tepki ile yavaş planlama nerede yer değiştiriyor, oyuncuya nasıl haber veriliyor›

## İlk 5 dakika (isteğe bağlı)
- **İlk anlamlı eylem:** ‹açılıştan kaç saniye sonra, ne› <!-- hedef: saniyeler içinde -->
- **Kanca:** ‹açıklamadan önce oyuncuyu ne yakalıyor› <!-- önce oynat, sonra anlat -->
- **Oyundan önce sürtünme yok:** ‹giriş, izin, uzun yükleme ve ayarlar ilk oyundan sonraya›
- **İlk yumuşak başarısızlık:** ‹ilk kayıp ne zaman geliyor, ne öğretiyor; bedeli küçük›

## Doruk ve bitiş (isteğe bağlı)
<!-- Bir deneyim en güçlü anıyla ve bitişiyle hatırlanır (Kahneman'ın doruk-son kuralı). -->
- **En güçlü an:** ‹oturumun ya da oyunun doruğu, nasıl hazırlanıyor›
- **Son nota:** ‹bir oturum ve oyun nasıl bitiyor, oyuncu hangi hisle kapatıyor›
- **Arkadaşa anlatılacak cümle:** ‹oyuncunun bir arkadaşına söyleyeceği tek cümle›

## UI gereksinimleri
| Bilgi | Nerede gösterilir | Güncellenme sıklığı | Koşul |
|---|---|---|---|
| ‹…› | | | |

## Bağımlılıklar ve bağlantılar
<!-- Başka bir belgenin belirli bir kuralına ya da değerine her bağımlılık burada yazılır. -->
| Bu belge şuna dayanır | Hedef belge | Öğe | Tür (veri / durum tetikleyici / kural / sahiplik devri) |
|---|---|---|---|
| ‹…› | | | |

## Kabul kriterleri
<!-- Bu sistemi uygulayan planın kabul kriterlerine kopyalanır. -->
- [ ] ‹…›
- [ ] Performans: sistem güncellemesi ‹X› ms içinde.
- [ ] Uygulamada koda gömülü ayar değeri yok.

## Ön-ölüm (isteğe bağlı)
<!-- Gary Klein'ın ön-ölüm (pre-mortem) yöntemi: başarısızlığı baştan varsay, sebeplerini şimdi bul. -->
‹Bu özellik ya da oyun başarısız oldu; en olası üç sebep ne, şimdi neyi değiştiririz?›

## Açık sorular
| Soru | Karar | Tarih |
|---|---|---|
| ‹…› | | |
