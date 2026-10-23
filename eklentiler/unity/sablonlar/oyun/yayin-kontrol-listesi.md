# Yayın Kontrol Listesi: ‹Sürüm› · ‹Platform›
<!-- Yayın hazırlığı planında bu liste plana kopyalanır ve maddeleri kabul kriteri olur. Uygun olmayan maddeyi silme, "Yok" diye işaretle. Otomatik doğrulanamayanlar Manuel test listesine gider. Testlerin nasıl yapılacağı ve rapor şablonu: `docs/ai/el-kitabi/yayin-oncesi-test-listesi.md` (kapsamlı test aşaması, planın sondan bir önceki adımı; son adım yayın). -->

- **Yayın tarihi:** YYYY-AA-GG · **Karar:** [ ] YAYINLA · [ ] BEKLET

## Build
- [ ] Tüm hedef platformlarda temiz build (`unity build`)
- [ ] Derleme uyarısı yok ya da gerekçesi yazılı
- [ ] Sürüm numarası ayarlı; mobilde build/version code artırılmış
- [ ] Android imzalı AAB ve iOS Xcode projesi `Builds/` altında hazır (Claude, Unity ile; keystore şifresini açık editöre sen girersin)
- [ ] Build, etiketlenmiş commit'ten yeniden üretilebilir
- [ ] Build boyutu bütçe içinde
- [ ] Tüm varlıklar dahil ve yükleniyor
- [ ] Hata ayıklama ve geliştirici özellikleri kapalı (Development Build, hile menüleri, ayrıntılı loglar)
- [ ] Android: yerel hata ayıklama sembolleri pakette (derleme betiğinde `DebugSymbols.level = SymbolTable`, `format = IncludeInBundle`; AAB'de `BUNDLE-METADATA/com.android.tools.build.debugsymbols` var), yoksa Play uyarır ve çökmeler okunamaz (`docs/ai/el-kitabi/unity-derleme-ve-bellek.md`)
- [ ] Uygulama simgesi pakette doğru: AAB'deki `base/res/mipmap-xxxhdpi-v4/app_icon.png` ve Xcode projesindeki simge gözle denetlendi; Unity'nin varsayılan simgesi sessizce girebiliyor (`docs/ai/el-kitabi/oyun-simgesi.md`)

## Kalite
- [ ] Açık kritik ya da büyük hata yok (istisnalar gerekçesiyle yazılı)
- [ ] Kalite kapısı geçti (yeni oyun ya da büyük güncelleme): `docs/ai/tasarim/kalite-kapisi/<sürüm>/puan.md`'nin ilk satırı `KAPI: GEÇTİ <sürüm>`; portföy denetimleri yeşil (öbür oyunlarımızla ortak görsel ve ses yok, mağaza metinleri en çok %25 benzer, kendi arayüz görünümü); kapsamlı test bundan sonra başladı (`docs/ai/el-kitabi/kalite-kapisi.md`)
- [ ] Kapsamlı test aşaması bitti: her adım dosyasının son testi ve test listesinin bu oyuna uyan bütün maddeleri tek tek denendi; rapor (madde, sonuç, kanıt) `Logs/claude/release/<sürüm>/rapor.md`'de, özeti test adımının dosyasında; karar YAYINLA (`docs/ai/el-kitabi/yayin-oncesi-test-listesi.md` §15)
- [ ] Mevcut otomatik testlerin hepsi bir kez koştu; kırmızı kalan yok: oyun hatası düzeltildi, eskimiş ya da kararsız test gerekçesiyle devre dışı ve teknik borçta
- [ ] Uzun oynama testi (4+ saat) sorunsuz; bellek sızıntısı yok
- [ ] En düşük hedef cihazda hedef FPS: ‹gerçek / hedef›
- [ ] Bellek ve yükleme süreleri bütçe içinde
- [ ] Uç durumlar test edildi
- [ ] Arayüz yayın öncesi aşamada ekran matrisiyle denendi: 5 telefon ve tablet profili, güvenli alan, iki dil; otomatik denetimler yeşil (`docs/ai/el-kitabi/arayuz-kalitesi-testleri.md`)
- [ ] His ve akıcılık denendi: dokunuşa aynı karede cevap, menülerde hedef FPS, titreşim ve "Hareketi azalt" ayarı (`docs/ai/el-kitabi/oyun-hissi.md`)

## İçerik
- [ ] Geçici varlıklar değiştirildi; mağazaya gri kutu, yer tutucu, çıplak Unity arayüzü ya da "New Text" çıkmıyor; ana ekran, HUD, kazanma, kaybetme ve mağaza en iyi iki örnekle yan yana puanlandı ve puan tabanını geçti; önceki ve sonraki puanlar raporda (taban ve hedef: `docs/ai/el-kitabi/arayuz-kalitesi.md` §5)
- [ ] Metinler düzeltildi; koda gömülü metin yok
- [ ] Yerelleştirme tamam: ‹diller›
- [ ] Ses miksajı son hâlinde
- [ ] Emeği geçenler ve üçüncü taraf lisans bildirimleri tamam; lisans listesi (`docs/ai/tasarim/lisanslar.md`: her paket ya da dosya, kaynağı, lisansı, nerede kullanıldığı) bu sürümün bütün varlıklarıyla güncel (`docs/ai/el-kitabi/proje-kontrol-listesi.md` 4.8)

## Platform: Mobil (Android / iOS)
- [ ] Android: hedef API seviyesi mağaza şartına uygun; AAB; IL2CPP + ARM64; imzalama anahtarı güvende ve yedekli
- [ ] iOS: Xcode projesi derleniyor; imzalama/provisioning tamam; izin açıklama metinleri (Info.plist) yazılı
- [ ] Yalnızca gereken izinler isteniyor
- [ ] Unity ayarları (`docs/ai/el-kitabi/unity-proje-ayarlari.md`): Unity açılış logosu kapalı; iOS'ta oyun ivmeölçeri okumuyorsa Accelerometer Frequency kapalı; Metal API doğrulaması kapalı; hedef FPS satırı var (yoksa oyun 30 FPS'te kalır)
- [ ] Güvenli alan / çentik, ekran yönü ve farklı en-boy oranları doğru
- [ ] Uygulama arka plana alınıp dönünce (arama, bildirim) doğru devam ediyor; kayıt kaybı yok
- [ ] Düşük seviye cihazda performans, ısınma ve pil tüketimi kabul edilebilir
- [ ] Uygulama içi satın alma ve satın alımları geri yükleme test edildi (varsa)
- [ ] Reklamlar ve onay akışı (GDPR / ATT) test edildi (varsa)
- [ ] Geçiş reklamının yeri (varsa): bir yere götüren düğmeye basınca (İleri, Devam, Tekrar → reklam → bölüm) ya da bölüm başında çıkmıyor; sonuç ekranında, puan sayımından ~0,5 sn sonra, yalnız reklam yüklüyse ve oyuncu o kısa beklemede dokunmadıysa çıkıyor; paneldeki düğmeler baştan görünür ve basılabilir, beklemedeki bir dokunuş reklamı iptal ediyor; gezinme düğmeleri reklamın çevresinde hiç gizlenmiyor (Apple bunu reddediyor); reklam kapanınca oyuncu aynı ekranda (`docs/ai/el-kitabi/google-play-level-up.md` §9)
- [ ] Google Play yapısı (`docs/ai/el-kitabi/google-play-level-up.md`): "Build order" bölümündeki parçalar ve 7. bölümdeki yönergeler tamam ya da eksikler gerekçesiyle yazılı; Play Games Ödülleri teklifleri Play Console'da etkin
- [ ] Play Console'daki önerilen işlemler ve Android vitals (son sürüm) gözden geçirildi; düzeltilecekler planda (R8, uçtan uca ekran gibi)
- [ ] Android vitals'ta bellek ölçümleri (son sürüm) Play'in eşiklerinin altında; Şubat 2027'den itibaren bütün Play'de şart (`docs/ai/el-kitabi/google-play-level-up.md` §7, Memory)
- [ ] App Store yapısı (`docs/ai/el-kitabi/app-store-game-center.md`): Game Center girişi ve başarımlar, satın alımları geri yükleme düğmesi tamam ya da eksikler gerekçesiyle yazılı; incelemeye göndermeden önceki maddeler (§7) gözden geçirildi; erişilebilirlik beyanları bu sürümde yeniden denendi (renk dışında ayırt etme için Gri Tonlama turu)

## Platform: PC (varsa)
- [ ] En düşük ve önerilen sistem gereksinimleri yazılı
- [ ] Klavye+fare ve gamepad tam çalışıyor
- [ ] Çözünürlük ölçekleme ve pencere modları çalışıyor; grafik ayarları kaydediliyor
- [ ] Mağaza SDK'sı, başarımlar ve bulut kayıt çalışıyor (varsa)

## Mağaza ve dağıtım
- [ ] Mağaza sayfası metni, ekran görüntüleri, tanıtım videosu ve görseller güncel
- [ ] İddialar denetlendi: mağaza (her dil), site, basın kiti ve video metinleri `store/facts.md`'ye karşı okundu; değişen iddia geçtiği her yerde düzeltildi, "son kontrol edilen sürüm" bu sürüm; yeni ya da değişen metin taze bir gözden geçirmeden geçti; fiyat ve hukuk iddiaları sana soruldu (`docs/ai/el-kitabi/metin-denetimi.md`)
- [ ] App Store ekran görüntüleri: zorunlu iPhone "Dynamic Island (orta boy ekran)" kümesi, bir büyük küme (6,9" ya da 6,5") ve oyun iPad'de çalışıyorsa iPad 13" (ölçüler: `docs/ai/el-kitabi/store-listing-optimization.md` › Limits)
- [ ] Tablet: arayüz tablet boylarında düzgün (ekran matrisi); Play'de 7 ve 10 inç tablet görüntüleri, her boyda en az 4. PC'de Google Play Games yalnız stüdyonun seçtiği oyunlarda, öbürlerinde form faktörü kapalı; Android XR şimdilik yok (`docs/ai/el-kitabi/store-listing-optimization.md`)
- [ ] Yaş derecelendirmesi alındı
- [ ] Gizlilik politikası ve kullanım şartları hazır; Google Play veri güvenliği ve App Store gizlilik formları politikayla aynı
- [ ] Fiyatlandırma tüm bölgelerde ayarlı; Play'de dolardan çevrilen ürünlerin Türkiye fiyatı aynı basamağın App Store Türkiye fiyatı (`docs/ai/el-kitabi/google-play-level-up.md` › Play Console work)
- [ ] Doğrudan yayın ayarları: Play'de üretim kanalı, %100 yayın, yönetilen yayın kapalı; App Store'da otomatik yayın, aşamalı yayın kapalı; test kanalı ve TestFlight yok
- [ ] Play'de ilk yayın: mağaza sayfası, bütün çeviriler, görseller, uygulama içi ürünler ve beyanlar ilk "incelemeye gönder"den önce girildi; inceleme sürerken değişiklik gönderilmiyor (uygulamayı sıranın sonuna itebilir). İlk yayında yönetilen yayın yok: onay gelince yayına girer
- [ ] Oyuncunun göreceği yeni içerik ya da süreli bir oyun içi etkinlik varsa mağaza etkinliği: Play'de tanıtım içeriği, App Store'da uygulama içi etkinlik (Major Update ya da uygun rozet); içerik o tarihlerde gerçekten oyunda; incelemesi için en az 4 gün önce gönderildi (`docs/ai/el-kitabi/store-events.md`)
- [ ] Mağazalarda yeni sürüm oluşturuldu ve sürüm verileri girildi: sürüm adı, iki dilde yenilikler notu, gerekiyorsa mağaza sayfası (Claude, Play Console ve App Store Connect'te Chrome'dan)
- [ ] App Store'a yeni oyun: hesapta incelemede başka yeni oyun yok (sıradaki, öncekinin onayından sonra ve 1-2 hafta arayla; aynı gün toplu gönderim yok); inceleme notunda farklılık dosyası (kanca, 3 rakip ve her biriyle 3 fark, neyin bizim neyin lisanslı olduğu (kullanılan paketler lisans listesinden, `docs/ai/tasarim/lisanslar.md`; şablon yok), kancanın videodaki yeri), ekte açılıştan kancaya 30-60 sn kayıt ve 2 açıklamalı ekran görüntüsü (`docs/ai/el-kitabi/kalite-kapisi.md` › Store and portal submissions)
- [ ] Build'ler mağazalara yüklendi ve incelemeye gönderildi (sen; Claude yüklemez, göndermez; oturum yöneticisi olan bilgisayarda yöneticinin kuralı geçerli)

## Yayına hazırlık
- [ ] Analitik veri alıyor; çökme raporlama kurulu
- [ ] Gerekirse ilk gün yaması hazır
- [ ] Duyurular ve tanıtım kodları hazır
- [ ] Yayın duyurusu hazır: `store/duyuru/<sürüm>.md`, Türkçe ve İngilizce (başlık, 1-2 cümle giriş, oyuncunun diliyle 3-5 yenilik, mağaza bağlantıları, kapak görseli); sürüm yayına girdiği gün stüdyonun sitesinde ve topluluk devlog'unda (ör. Oyun Günlüğü) yayınlanır; devlog haftalık sınıra takılırsa not sıraya alınır (yeni oyunlar önce), atlanmaz (`docs/ai/BAKIM.md` › After release)
- [ ] Yayınlanan commit `v<sürüm>` etiketli ve etiket push'lu
- [ ] Stüdyonun birden çok oyunu varsa yeni oyun öbür canlı oyunların "More Games" listesinde: liste uzaktaysa (ayar, katalog) aynı gün, oyuna gömülüyse o oyunların sıradaki sürümünde
- [ ] Bilinen sorunlar listesi hazır
- [ ] Geri dönüş planı yazılı: yayın doğrudan ve %100 olduğu için sorunlu sürüm durdurulamaz; düzeltme yeni bir sürümle çıkar

## Son karar
- **Karar:** YAYINLA / BEKLET
- **Gerekçe:** ‹Hazırlık özeti; BEKLET ise engelleyen maddeler ve tahmini çözüm süresi.›
- **Kabul edilen riskler:** ‹…›
