# Yayın Kontrol Listesi: ‹Sürüm› · ‹Platform›
<!-- Yayın hazırlığı planında bu liste plana kopyalanır ve maddeleri kabul kriteri olur. Uygun olmayan maddeyi silme, "Yok" diye işaretle. Otomatik doğrulanamayanlar Manuel test listesine gider. -->

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

## Kalite
- [ ] Açık kritik ya da büyük hata yok (istisnalar gerekçesiyle yazılı)
- [ ] Kritik yoldaki tüm özellikler test edildi; tüm testler geçiyor
- [ ] Uzun oynama testi (4+ saat) sorunsuz; bellek sızıntısı yok
- [ ] En düşük hedef cihazda hedef FPS: ‹gerçek / hedef›
- [ ] Bellek ve yükleme süreleri bütçe içinde
- [ ] Uç durumlar test edildi
- [ ] Arayüz her sürümde ekran matrisiyle test edildi: telefon ve tablet profilleri, güvenli alan, iki dil; otomatik denetimler yeşil (`docs/ai/el-kitabi/arayuz-kalitesi-testleri.md`)
- [ ] His ve akıcılık denendi: dokunuşa aynı karede cevap, menülerde hedef FPS, titreşim ve "Hareketi azalt" ayarı (`docs/ai/el-kitabi/oyun-hissi.md`)

## İçerik
- [ ] Geçici varlıklar değiştirildi; mağazaya gri kutu, yer tutucu, çıplak Unity arayüzü ya da "New Text" çıkmıyor; değişen her ekran en iyi iki örnekle yan yana puanlandı, hiçbir ölçüt 4'ün altında değil (`docs/ai/el-kitabi/arayuz-kalitesi.md`)
- [ ] Metinler düzeltildi; koda gömülü metin yok
- [ ] Yerelleştirme tamam: ‹diller›
- [ ] Ses miksajı son hâlinde
- [ ] Emeği geçenler ve üçüncü taraf lisans bildirimleri tamam

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
- [ ] App Store yapısı (`docs/ai/el-kitabi/app-store-game-center.md`): Game Center girişi ve başarımlar, satın alımları geri yükleme düğmesi tamam ya da eksikler gerekçesiyle yazılı; incelemeye göndermeden önceki maddeler (§7) gözden geçirildi

## Platform: PC (varsa)
- [ ] En düşük ve önerilen sistem gereksinimleri yazılı
- [ ] Klavye+fare ve gamepad tam çalışıyor
- [ ] Çözünürlük ölçekleme ve pencere modları çalışıyor; grafik ayarları kaydediliyor
- [ ] Mağaza SDK'sı, başarımlar ve bulut kayıt çalışıyor (varsa)

## Mağaza ve dağıtım
- [ ] Mağaza sayfası metni, ekran görüntüleri, tanıtım videosu ve görseller güncel
- [ ] App Store ekran görüntüleri: zorunlu iPhone "Dynamic Island (orta boy ekran)" kümesi, bir büyük küme (6,9" ya da 6,5") ve oyun iPad'de çalışıyorsa iPad 13" (ölçüler: `docs/ai/el-kitabi/store-listing-optimization.md` › Limits)
- [ ] Yaş derecelendirmesi alındı
- [ ] Gizlilik politikası ve kullanım şartları hazır; Google Play veri güvenliği ve App Store gizlilik formları politikayla aynı
- [ ] Fiyatlandırma tüm bölgelerde ayarlı; Play'de dolardan çevrilen ürünlerin Türkiye fiyatı aynı basamağın App Store Türkiye fiyatı (`docs/ai/el-kitabi/google-play-level-up.md` › Play Console work)
- [ ] Doğrudan yayın ayarları: Play'de üretim kanalı, %100 yayın, yönetilen yayın kapalı; App Store'da otomatik yayın, aşamalı yayın kapalı; test kanalı ve TestFlight yok
- [ ] Play'de ilk yayın: mağaza sayfası, bütün çeviriler, görseller, uygulama içi ürünler ve beyanlar ilk "incelemeye gönder"den önce girildi; inceleme sürerken değişiklik gönderilmiyor (uygulamayı sıranın sonuna itebilir). İlk yayında yönetilen yayın yok: onay gelince yayına girer
- [ ] Oyuncunun göreceği yeni içerik ya da süreli bir oyun içi etkinlik varsa mağaza etkinliği: Play'de tanıtım içeriği, App Store'da uygulama içi etkinlik (Major Update ya da uygun rozet); içerik o tarihlerde gerçekten oyunda; incelemesi için en az 4 gün önce gönderildi (`docs/ai/el-kitabi/store-events.md`)
- [ ] Mağazalarda yeni sürüm oluşturuldu ve sürüm verileri girildi: sürüm adı, iki dilde yenilikler notu, gerekiyorsa mağaza sayfası (Claude, Play Console ve App Store Connect'te Chrome'dan)
- [ ] Build'ler mağazalara yüklendi ve incelemeye gönderildi (sen; Claude yüklemez, göndermez)

## Yayına hazırlık
- [ ] Analitik veri alıyor; çökme raporlama kurulu
- [ ] Gerekirse ilk gün yaması hazır
- [ ] Duyurular ve tanıtım kodları hazır
- [ ] Bilinen sorunlar listesi hazır
- [ ] Geri dönüş planı yazılı: yayın doğrudan ve %100 olduğu için sorunlu sürüm durdurulamaz; düzeltme yeni bir sürümle çıkar

## Son karar
- **Karar:** YAYINLA / BEKLET
- **Gerekçe:** ‹Hazırlık özeti; BEKLET ise engelleyen maddeler ve tahmini çözüm süresi.›
- **Kabul edilen riskler:** ‹…›
