# Oyun Özeti: ‹Çalışma adı›
<!-- Tek ekranlık özet; bir alan ikinci paragrafa taşıyorsa GDD yazıyorsun demektir. Doldurulan belge: docs/ai/tasarim/oyun-ozeti.md, HAFIZA dizinine eklenir. -->

**Tek cümlelik tanıtım:** ‹Oyunu heyecanla tek cümlede anlat; iki cümle gerekiyorsa kısalt.›
**Kimin için, ne hissettirir:** ‹Oyuncu ve his, tek satır.› <!-- önerilen -->
**Kimin için değil:** ‹Bilerek hedeflemediğimiz oyuncu, tek satır.› · **Benzer oyunlar:** ‹2-3 oyun› <!-- isteğe bağlı -->
**Sanat ve ses yönü:** ‹Varlık seçimlerini yönlendiren estetik niyet, tek satır.› <!-- önerilen; ayrıntısı görsel stil rehberinde (gorsel-stil.md) -->
**Platform ve gelir modeli:** ‹ör. Android + iOS · reklam + uygulama içi satın alma› <!-- el kitabı koşulları (ör. Google Play) buna bakar -->

## Tasarım sütunları
<!-- 3-5 sütun: oyunun her kararda öne aldığı şeyler. Sütunlar fikir öldürmez, sıralar (kullanıcı, 2026-10-15: "bir şeyi feda etmeyelim"). Her yeni özellik fikri hizmet ettiği sütunu söyler; söyleyemiyorsa sıranın sonuna yazılır. "Dikkat": sütunu korumak için ölçülecek ya da gözetilecek şey. Ön araştırmadan sonra (docs/ai/tasarim/on-arastirma/) onun bulgularıyla gözden geçirilir. -->
| Sütun | Öne aldığı | Dikkat |
|---|---|---|
| ‹ör. Kısa tur› | ‹2-3 dakikada biten, tek elle oynanan turlar› | ‹tur süresi ölçülür; turu uzatan özellik ayrı bir moda gider› |

## Üç tasarım sorusu
<!-- Sütunlarla birlikte yazılır, her biri 1-2 satır; yeni bir özellik bunlara da uyar (kullanıcı, 2026-10-23; bir oyun tasarımı yazısından esinlenildi, metni alınmadı). -->
- **Oyuncuyu her şeyi söylemeden nasıl yönlendiriyoruz?** ‹görsel, oynanış ve ses aynı şeyi söylüyor; ekran kalabalık değil›
- **Oyuncunun kontrolünü nerede elinden alıyoruz, neden?** ‹yalnız deneyim gerçekten istiyorsa (ör. kısa bir kutlama); yoksa "hiçbir yerde"›
- **Kurallar tutarlı ve öğrenilebilir mi?** ‹aynı görünen aynı davranır; bir istisna varsa oyuncuya nasıl gösteriliyor›

## Çekirdek döngü
<!-- Tekrarlanan döngü: oyuncu ne yapar → ne kazanır → neden tekrar eder. 2-4 madde. -->
- ‹…›

## Oyuncu hedefi ve kaybetme durumu
<!-- Oyuncu neye ulaşmaya çalışıyor, bir tur ya da oyun nasıl biter. Planların kabul kriterleri buradan türetilir. 1-2 satır. -->
‹…›

## MVP: oyun olması için şart olanlar
<!-- Acımasızca kısa; her madde bir plan adayıdır. ~7 maddeyi aşıyorsa MVP değildir. -->
1. ‹…›

**Tek bir şeyi çıkarmak zorunda olsak ne olurdu?** ‹hangisini çıkarırdık, oyun ne kaybederdi› <!-- isteğe bağlı; demo ve ilk sürüm için kapsam kontrolü -->

## Kapsam dışı
<!-- Bilerek yapılmayanlar, net yaz: "çok oyunculu yok", "kayıt sistemi yok", "tek seviye". -->
- ‹…›

## Yapım sırası
<!-- En riskli ya da eğlencenin çekirdeği olan parça önce: cilalamadan önce eğlenceli olduğunu kanıtla. Maddeler DURUM.md'de Up next listesine plan adayı olarak yazılır. -->
1. ‹…›

## Ölçüm hedefleri (isteğe bağlı)
<!-- İlk yayından önce, veri gelmeden yazılır; veri görüldükten sonra eşik değişmez. Ölçüm olayları ilk sürümle çıkar. Yayından en az 14 gün sonraki analiz bu satırlara bakar, karar (geliştir · bakım · rafa kaldır) DURUM'a yazılır (docs/ai/BAKIM.md › After release). Az kurulumda oran aralık olarak okunur (docs/ai/el-kitabi/firebase-olcum-ve-uzaktan-ayar.md). -->
| Ölçüt | Devam eşiği | Büyütme eşiği | Nereden |
|---|---|---|---|
| D1 (ertesi gün dönen oyuncu) | ‹ör. ≥ %35› | ‹ör. ≥ %40› | ‹Firebase, sürüme göre› |
| D7 | ‹ör. ≥ %12› | ‹…› | ‹…› |
| İlk gün oyun süresi | ‹ör. ≥ 15 dk› | ‹…› | ‹…› |
