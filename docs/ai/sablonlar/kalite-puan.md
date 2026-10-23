KAPI: ‹GEÇTİ | KALDI› ‹sürüm› · ‹kararı veren› · ‹YYYY-AA-GG SS:DD›
# Kalite Kapısı Puan Kâğıdı: ‹Oyun› ‹Sürüm› · Tur ‹0 · 1 · 2›
<!-- Doldurulan kopya: docs/ai/tasarim/kalite-kapisi/‹sürüm›/puan.md. Kurallar, kayıt ve kanıt düzeni: docs/ai/el-kitabi/kalite-kapisi.md. İlk satır sonuç satırıdır: kararı veren (makineye özel CLAUDE.md bir oturum yöneticisi adlandırıyorsa o, yoksa oyunun sahibi) en son yazar; o zamana kadar "KAPI: bekliyor ‹sürüm›". Tur 0 ilk puanlama, en çok iki düzeltme turu gelir. Hakeme yalnız "Hakem formu" bölümü ve kor/ klasörü verilir; bu kâğıdın gerisi, anahtar.md ve farklılık dosyası verilmez. -->

## Hakem formu
<!-- Hakem projeyi bilmeyen yeni bir yardımcı ajandır: yalnız kor/ altındaki kanıta bakar, başka dosya okumaz. Her oyunu (A-D) her alanda öbür üç oyuna göre puanlar, her puana bir satır gerekçe yazar ve cevabını bu tabloyla verir; ana oturum cevabı olduğu gibi hakem-‹n›.md olarak saklar. Her turda yeni hakemler. -->
**Ölçek** (her oyun, öbür üç oyuna göre): 1 = bozuk ya da yok · 2 = öbür üçün en zayıfından kötü · 3 = öbür üçün ortası kadar · 4 = en iyisi kadar · 5 = üçünden de iyi, ilk ekran görüntüsüne konacak kadar.
**Farklılık:** 1 = kopya · 2 = yalnız yeni tema · 3 = küçük bir değişiklik · 4 = ilk dakikada görünen net bir fark · 5 = net fark ve öbür üçünde olmayan bir tema, kitle ya da meta birleşimi.

| Alan | Kanıt (`kor/`) | A | B | C | D |
|---|---|---|---|---|---|
| İlk 60 saniye | soğuk açılış videosu (simgeye dokunuştan), ilk dokunuşa süre, oyuna kaç dokunuş | ‹puan: gerekçe› | | | |
| Oynanış hissi | aynı hareketlerin 20 sn klipleri, gecikme tablosu, geri bildirim matrisi | | | | |
| Görsel ve animasyon | aynı anların 6 görüntüsü ve 3 klibi | | | | |
| Arayüz ve okunurluk | ana ekran, HUD, kazanma, kaybetme, mağaza, ayarlar; ölçüler | | | | |
| Ses ve titreşim | sesli klipler, titreşim listesi | | | | |
| İçerik ve ilerleme | bölüm sayısı, yenilik takvimi, zorluk eğrisi, 12 rastgele bölümlük pafta | | | | |
| Reklam ve teklifler | reklam ve teklif tablosu (`olcumler.md`): ilk geçiş reklamı (bölüm, dakika), 10 dakikadaki geçiş reklamı sayısı, ödüllü teklifler ve verdikleri, reklam gelmeyince ve çevrimdışıyken ne olduğu | | | | |
| Teknik | FPS, bellek, yükleme, boyut ve çökme tablosu (`olcumler.md`) | | | | |
| Erişilebilirlik | renk körlüğü benzetimleri, ayarlar listesi | | | | |
| Mağaza ve portal görselleri | türün ızgarasında simge, ilk 3 ekran görüntüsü, videonun ilk 5 sn'si | | | | |
| Farklılık | `ozellikler.md`, kayıtlar | | | | |

## Birleştirme (hakeme verilmez)
<!-- Ana oturum anahtarla bizim harfimizi bulur ve hakemlerin bizim için verdiği puanları yazar. Alan puanı iki hakemin ortalaması; bizim bir alanımızda iki hakem 2 ya da daha çok ayrışırsa üçüncü hakem, o alanda üçünün ortancası. 4,5 puan 5 sayılmaz. Kanıt sütunu kor/ altındaki dosyaya bağlanır. -->
- **Bizim harfimiz:** ‹A-D› (`anahtar.md`) · **Kancanın alanı** (puanlamadan önce farklılık dosyasında yazılı): ‹alan›
- **Hakemler:** ‹hakem-1.md, hakem-2.md, hakem-3.md (gerekirse)› · **Taze oyuncu:** ‹oyuncu-1.md› · **Kanıtın commit'i:** ‹…›

| Alan | En az | Kanıt | H1 | H2 | H3 | Puan | Gerekçe (kısa) |
|---|---|---|---|---|---|---|---|
| İlk 60 saniye | 4 | ‹`kor/‹harf›/…`› | | | | | |
| Oynanış hissi | 3 | | | | | | |
| Görsel ve animasyon | 3 | | | | | | |
| Arayüz ve okunurluk | 3 | | | | | | |
| Ses ve titreşim | 3 | | | | | | |
| İçerik ve ilerleme | 3 | | | | | | |
| Reklam ve teklifler | 3 | | | | | | |
| Teknik | 3 | | | | | | |
| Erişilebilirlik | 3 | | | | | | |
| Mağaza ve portal görselleri | 3 | | | | | | |
| Farklılık | 4 | | | | | | |

**Hesap:**
- [ ] Her alan en az kendi sınırında (İlk 60 saniye ve Farklılık 4, diğerleri 3)
- [ ] Ortalama ‹x,xx› ≥ 3,5
- [ ] En az bir alan 5 ve kancanın alanı onlardan biri: ‹alan›
- [ ] Kanca ilk 60 saniyede ve 1-2. ekran görüntülerinde görünüyor
- [ ] Rakiplerin puanları akla yatkın (türün liderine her alanda 2 veren hakem kanıtı yanlış okumuştur: yeni hakem)

## Kesin şartlar (geçti / kaldı)
| Şart | Ölçüm ve kanıt | Sonuç |
|---|---|---|
| Kapının cihaz matrisi koşularında çökme ve ANR yok | ‹koşular, günlük› | |
| En düşük hedef telefonda en ağır bölüm 60 FPS (p95 kare ≤ 16,7 ms) | | |
| Web: ilk indirme ≤ 20 MB (portalların üst sınırı 50 MB, yalnız yazılı gerekçeyle), oyuna ≤ 10 sn | ‹ya da "web yok"› | |
| Yer tutucu görsel ya da metin yok | | |
| İngilizce tam | | |

## Portföy denetimleri (stüdyonun öbür oyunlarına karşı)
| Denetim | Kanıt | Sonuç |
|---|---|---|
| Ortak oyun görseli, sesi ya da modeli yok (`varlik-cakisma.py`, izin listesi `izinli-ortak.txt`) | `portfoy/varlik-cakisma.txt` | |
| Mağaza metinleri (açıklama, tanıtım metni, yenilikler) öbür oyunlarımıza en çok %25 benzer (`metin-benzerlik.py`) | `portfoy/metin-benzerlik.txt` | |
| Kendi arayüz görünümü: çerçeve, renk, yazı tipi, simgeler ve ana ekran düzeni öbür oyunlarımızdan farklı | `portfoy/arayuz-paftasi.png` (bütün oyunlarımızın ana ekran, HUD ve kazanma ekranı yan yana) | |
| Temel hareketin ses efektleri bu oyuna ait | | |
| Satın alınmış hazır proje şablonu yok (varlık paketleri olur) | | |

## Taze oyuncunun oturumu
<!-- Projeyi hiç görmemiş bir yardımcı ajan, kapı derlemesini temiz kurulumla 10 dakika oynar (web derlemesi sürdüğü bir tarayıcıda, değilse emülatörde adb dokunuşları ve ekran görüntüleriyle), tek oyuncu profili, ipucu almadan. Netliği ölçer, eğlenceyi değil: 1-3. bölümde ya da bir ekranda takılırsa bulgu düzeltmeye gider ve kapı, yeni bir taze oyuncu oradan geçene kadar geçmez; öbür cevaplar puanların yanında kararı verene gider. Ana oturum cevabı olduğu gibi oyuncu-‹n›.md olarak saklar; her turda yeni bir taze oyuncu. (Oyunun sahibinin 10 dakikalık oyununun yerine; sahibi 2026-10-22: kendisi test yapmaz.) -->
- **Tarih, derleme, nerede oynandı:** ‹…›
1. **Oynamaya devam eder miydin?** ‹evet · hayır, neden›
2. **Bu oyunun tek özelliği ne?** ‹…›
3. **Ucuz duran ne?** ‹… ya da "yok"›
4. **Rakiplerden hangisini seçerdin, neden?** (oynadıktan sonra `kor/`'daki kayıtlara bakarak) ‹…›
- **Takıldığı yerler:** ‹dk:sn · bölüm ya da ekran · ne yapmaya çalıştı · ne kadar sürdü; yoksa "yok"›

## Gerçek oyuncu testi (isteğe bağlı, web)
- ‹Poki Playtest ya da Player Fit (önce Poki'nin özel yayın şartlarına bakılır): sonuç ve bağlantı; yoksa —›

## Sonuç
- **Engelleyenler:** ‹yok · ya da: kırmızı kesin şart, sınırın altında alan, ortalama 3,5'in altında, 5 yok ya da kanca değil, kanca ilk 60 saniyede ya da 1-2. görüntüde yok, portföy bulgusu, taze oyuncunun 1-3. bölümde ya da bir ekranda takılması, eksik kanıt›
- **Sonraki tur:** ‹düzeltilecekler bu sırayla: engeller, ilk dakika, oynanış hissi, görsel ve arayüz, ses, mağaza görselleri›
- **İkinci turdan sonra da kalırsa karar:** ‹yeniden işle · yalnız uygun yerde yayımla (ör. yalnız Android ya da web) · rafa kaldır›
