# Kullanım Kılavuzu

Claude Çalışma Şablonu'nu kurmak ve her gün kullanmak için kısa rehber. Tasarımın ayrıntıları ve gerekçeleri [README](README.tr.md) dosyasında.

**Hızlı başvuru**

| Ne yapmak istiyorsun | Nerede | Ne yazarsın |
|---|---|---|
| Şablonu bir projeye kurmak | Projenin klasöründe (yeni oyun için herhangi bir yerde) | `şablonu kur` |
| Projedeki şablonu yeni sürüme almak | Projenin klasöründe | `şablonu güncelle` |
| Kaldığın yerden devam etmek | Projenin klasöründe | `devam` |
| El kitabına video notu eklemek | Şablon klasöründe | `bu videoyu el kitabına ekle: <link>` (Chrome bağlı değilse Gemini'nin notunu da yapıştır) |

---

## 1. Şablonu bir bilgisayara kurmak (bir kez)

Her bilgisayarda bir kez:

1. **Repoyu klonla.** GitHub Desktop → **File → Clone repository** → `tahaexe/claude-code-work-template` → örneğin `C:\Users\<kullanıcı>\claude-code-work-template`.
2. **Global yönlendirmeyi ekle.** `~/.claude/CLAUDE.md` dosyasına aşağıdaki bloğu yapıştır. `<ŞABLON>` yerine klonladığın klasörü, `<UNITY_PROJELERİ>` yerine Unity projelerinin durduğu klasörü yaz. Bu adım olmadan Claude "şablonu kur" sözünü tanımaz.
   ```markdown
   ## Claude çalışma şablonu
   Şablon klasörü: <ŞABLON>
   Unity projeleri klasörü: <UNITY_PROJELERİ> (yeni Unity projeleri burada oluşturulur)
   - Kullanıcı bir projeye bu çalışma sistemini kurmak isterse ("şablonu kur", "planlı çalışma sistemini kur" gibi): <ŞABLON>\docs\ai\KURULUM.md dosyasını oku ve "Kurulum" bölümünü uygula.
   - Şablonu güncellemek isterse ("şablonu güncelle"): aynı dosyanın "Güncelleme" bölümünü uygula.
   - Bir projede çok adımlı bir işe başlanırken projede docs/ai/PROTOKOL.md yoksa kurulumu tek cümleyle öner; istenmezse ısrar etme.
   ```
   **Şablonun sahibiysen** (kendi bilgisayarların) bloğa şu satırı da ekle. Claude araçları ve eklentileri sormadan kurar, şablonu da yalnızca bu satırın olduğu bilgisayarda geliştirir:
   ```markdown
   - Bu bilgisayar şablon sahibinin: şablon burada geliştirilir; Unity CLI, Unity'nin Claude eklentisi ve şablonun eklentileri sormadan kurulur.
   ```
3. **Unity kullanıyorsan** ayrıca bir şey kurman gerekmez: Unity CLI, Unity'nin Claude eklentisi ve C# kod zekâsı (`csharp-ls` dil sunucusu ve `csharp-lsp` eklentisi; bilgisayarda .NET 10 SDK'sı yoksa atlanır) eksikse Claude kurar (sahibin bilgisayarında sormadan, başkasında bir kez sorarak). Unity'ye bağlantıda önce CLI kullanılır; Unity MCP yasak değil, CLI'ın yetmediği yerde Claude kullanabilir.
4. **Claude'a tarayıcı profili (her Claude hesabı için bir kez).** Claude'a "kendine tarayıcı profili kur" de. Claude, Chrome'da kendi adını taşıyan yeni bir profil açar ve Claude eklentisinin sayfasını gösterir. Claude'un adı, hesabının adıdır (giriş e-postasının @ öncesi, ör. alex). O pencerede şunları sen yaparsın: Chrome'a giriş yapmadan geç, **Chrome'a ekle → Uzantı ekle**'ye bas, eklentide o Claude hesabıyla giriş yap, sonra profil simgesi → **Profili özelleştir**'den profilin adını Claude'un adı yap. Claude yalnızca kendi profilini kullanır; senin profillerine ve başka tarayıcılara dokunmaz. Yalnızca Chrome kullanılır; başka tarayıcı yok.

### Başka biri kullanacaksa
1. **Erişim:** Depo herkese açık; GitHub'dan klonlamak yeterli. Şablonu kendine göre değiştirmek isteyen depoyu fork'layabilir.
2. **Onun bilgisayarında:** Claude masaüstü uygulaması ve kendi Claude hesabı → depoyu klonlar → yukarıdaki global bloğu kendi klasör yollarıyla ekler (sahip satırı olmadan) → Unity için Unity Hub ve editörü kurar (C# kod zekâsı için .NET 10 SDK'sını da). Unity CLI'ı ve eklentileri Claude kurmadan önce bir kez sorar.
3. **Güncellemeler:** Sahip push'ladıkça GitHub Desktop'ta **Pull**. Projeleri Claude bir sonraki plan kapanışında kendisi günceller; beklemek istemezsen `şablonu güncelle` de.
4. **Bilmesi gerekenler:** Claude Türkçe konuşur; çoğu plana onay beklemeden başlar; her commit otomatik push'lanır, gerekirse zorla push da yapar (`--force-with-lease`); tarayıcı işlerini izin almadan yapar; kurulum, açıksa agent-protocols ve engineering eklentilerini kapatır (biri Windows'ta bozuk, ikisi de kullanılmıyordu), Unity projelerinde Unity'nin Claude eklentisini ve C# kod zekâsını ekler. Şablon klasöründe Claude şablonu değiştirmez; şablon yalnızca sahibin bilgisayarında geliştirilir.

## 2. Bir projeye kurmak: `şablonu kur`

Claude Code'u projenin klasöründe aç ve `şablonu kur` yaz. Claude önce **ne projesi olduğunu** klasörden anlar; anlayamazsa sorar:

- **Unity + mevcut proje:** Genel kurulum, Unity eklentisi, eksik paketler (Pipeline, Test Framework), git ve izin kuralları kurulur. Unity ayarlarını doğru değerlerle karşılaştıran bir "ayar denetimi" plan adayı eklenir. Projeye uyan el kitabı girdileri eklenir. Kod singleton'lar ve dev yönetici sınıflarıyla yazılmışsa sıraya servis mimarisine geçiş planı eklenir; sen başlatana kadar kod değişmez. Görsel stil rehberi yoksa Claude ilk UI işinden önce taslağını yazar, sen düzeltirsin.
- **Unity + yeni oyun:** Beş soru sorar: ad, kısa fikir, 2D mi 3D mi, platform, gelir modeli. Projeyi Unity projeleri klasöründe, Unity ayarlarının platforma göre doğru değerleriyle oluşturur, oturumu yeni klasöre taşır ve kurulumu orada bitirir. Sonunda oyun özetini boş alanları kendi önerileriyle dolu olarak gösterir (sen düzeltirsin). İlk plandan önce ön araştırmayı yapar (aşağıda, §3 "Ön araştırma"); sonra ilk planı önerir, ilk plan servislerin kurulduğu başlangıç noktasıyla başlar. İlk UI işinden önce Claude görsel stil rehberinin taslağını yazar, sen düzeltirsin.
- **Diğer:** Genel kurulum yapılır: dosyalar, git, izinler, CLAUDE.md ve projeye özel kurallar.

**Android oyunlarında** ayrıca Google Play'in önerdiği oyun yapısı (Level Up) için rehber kurulur ve DURUM'daki **Up next** listesine bu yapıyı doğru sırayla ekleyen üç plan adayı yazılır: önce giriş, başarımlar ve Play Games Ödülleri; sonra Game Stats; en son FPS, büyük ekran, kumanda ve bulut kayıt. Claude ödülleri oyununa göre tasarlar ve değerleri Play Console'a kendi Chrome profilinden kendisi girer; Play Games Services kurulumu ve güncellemelerin tanıtım kartları da onda. Ödeme profili ve program şartlarını kabul etmek sende kalır. Play Console'un uyarıları (R8, uçtan uca ekran) için ayrı bir plan adayı yazılır.

**iOS oyunlarında** aynı yapının App Store karşılığı için rehber kurulur: Game Center girişi ve başarımlar, satın alımları geri yükleme düğmesi, uygulama içi etkinlikler. Bir plan adayı yazılır; App Store Connect'teki girişleri Claude yapar.

Kurulum sırasında yalnızca şu durumlarda onayın istenir:
- Bilgisayarda olmayan bir programın indirilmesi, örneğin Unity editörü. Unity CLI, Pipeline paketi, C# dil sunucusu (`csharp-ls`) ve eklentiler şablon sahibinin bilgisayarında sorulmadan kurulur; başka bir bilgisayarda Claude bir kez sorar.
- Uygulamanın, oturumu yeni klasöre taşımak için istediği onay.
- El kitabı girdisinin gerektirdiği bir araç, örneğin Sidekick aracı. "İstemiyorum" dersen bir daha sorulmaz.

## 3. Günlük kullanım (komut ezberlemen gerekmez)

| Ne istiyorsun | Örnek | Ne olur |
|---|---|---|
| Yeni bir iş | "Envanter sistemi ekleyelim" | Küçük işse doğrudan yapar; büyükse plan hazırlar, gösterir ve başlar. Plan senin kararını gerektiriyorsa (kapsam, para, geri dönüşü zor işlem) ya da fazlara bölünüyorsa onayını bekler. Plan dosyası kısa bir dizindir; her adımın ayrıntısı kendi dosyasında durur. Plan sonuna kadar kendi ilerler; her adımda hata kontrolü yapılır (derleniyor mu, çalışınca günlükte hata var mı), plana işlenir, commit'lenir ve push'lanır; sondan bir önceki adım kapsamlı testtir |
| Planı önce görmek | "önce planı göster" | Plana başlamadan onayını bekler |
| Bekleyen planı onaylamak | "tamam", "olur" | Plan başlar |
| Devam etmek | "devam", "devam et", "kaldığımız yerden" | Durumu, plan dizinini ve yalnız sürmekte olan adımın dosyasını okur (önce oradaki "Kaldığım yer" notunu); bitmiş adımları ve eski kayıtları yeniden okumaz. Yarım kalan işi toparlar, kısa bir derleme kontrolü yapar, sonra kaldığı yerden sürer |
| Durumu görmek | "nerede kalmıştık?" | Kısa durum özeti verir |
| Planı görmek | "planı göster", "tüm planlar" | İşaretli liste: ✓ Tamamlandı · ▶ Devam ediyor · ○ Yapılacak · ⛔ Engellendi |
| Planı değiştirmek | "4. adımdan sonra şunu ekle", "şunu çıkar", "şunu sıraya koy" | Plan güncellenir ve commit'lenir |
| Hızı ayarlamak | "yavaş gidelim" / "sen devam et" | Her adımda durur / otomatik ilerler |
| Düzeltmek | "bunu yapma, hep şöyle yap" | Düzeltir, dersi hafızaya yazar; kalıcı bir kuralsa CLAUDE.md'ye ekler ve söyler |
| Bir şey hatırlatmak | "bilgin olsun: …", "bunu hatırla: …" | Uygun hafıza dosyasına yazar |
| Hafızayı toparlamak | "hafıza bakımı" | Tekrarları birleştirir, eskimiş bilgileri düzeltir |
| Tarayıcıda bir iş | "Play Console'da ürünleri oluştur", "şu sayfaya bak" | Chrome'daki kendi profilinde izin almadan kendisi yapar (Claude in Chrome); yalnızca Claude'un kendi güvenlik onayları kalır |
| Sürüm çıkmak | "8.3 sürümünü hazırla", "sürüm çıkalım" | Yeni oyunda ve büyük güncellemede önce kalite kapısı (aşağıda): türün en çok oynanan üç oyunuyla kör puanlama, oyunu hiç görmemiş bir ajanın 10 dakikalık oyunu; `KAPI: GEÇTİ` olmadan gönderim yok. Sonra kapsamlı test aşaması (planın sondan bir önceki adımı): her adımın kendi dosyasındaki son testi tek tek, bütün testler bir kez, yayın kontrol listesi ve test listesi (aygıt matrisi, satın alma, reklam, analitik, performans, diller, erişilebilirlik, mağazanın ön yayın raporu), raporuyla. Sonra mağazalarda yeni sürümü doğrudan yayın olarak oluşturur (Play'de üretim kanalı ve %100, App Store'da otomatik yayın; test kanalı ve TestFlight yok) ve verilerini girer, Android ve iOS build'lerini `Builds/` klasörüne alır, sonra bekler. Build'leri mağazalara sen yükler, incelemeye sen gönderirsin (bilgisayarda oturum yöneticisi varsa onun kuralı geçerli); Android imzası için keystore şifresini açık editöre sen girersin |

Claude seçtiği yolu tek satırla söyler (ör. "→ Plan hazırlıyorum"); istersen hemen yönünü değiştirirsin.

**Otomatik ilerleme yalnızca şu durumlarda durur:** hata kontrolü geçmiyor ve denemeye değer fikir kalmamışsa, planın bir varsayımı yanlış çıkarsa, kapsamlı test aşamasında kırmızı bir testin nedeni anlaşılmıyorsa (oyun hatası mı, eskimiş test mi), planda olmayan ve geri dönüşü zor bir işlem (git'in geri getiremeyeceği silme, paket yükseltme ya da kaldırma, veri taşıma) gerekirse ya da senin kararın gerekirse.

**Kalite çıtası:** oyuncunun ya da izleyicinin göreceği işlerde (ekran, his, sanat, mağaza sayfası, video) Claude plandan önce aynı işin en iyi örneklerini inceler ve planı alanın uzman ajanına (Unity'de `unity-uzmani`) inceletir; bulgular planın başındaki "Review" (İnceleme) bölümüne yazılır. Kapanışta iş denenir, uzman sonucu inceler ve Claude "en iyilerin yanında nasıl duruyor?" sorusunu dürüstçe cevaplar; zayıfsa önce düzeltilir. Özensiz iş yapılmamış sayılır.

**Ön araştırma** (21 Ekim 2026'dan beri): yeni bir oyunda ya da kanalda ilk plandan önce (kurulum planları dahil) ve oyuncunun ya da izleyicinin göreceği her büyük işten önce Claude alanın en iyi işlerini alan alan inceler: pazar ve rakipler, oynanış ve bölüm tasarımı, grafik stili, shader ve efektler, oyun hissi, arayüz ekranları, simge, ses ve müzik, mağaza sayfası, ilk dakika, para kazanma (YouTube'da önde giden kanallar, başlıklar, küçük resimler, süre, tempo, yorumlar). İlk 2-3 rakibi Play Store'lu bir emülatörde oynar, her bilgiyi kaynağıyla yazar, görüntü ve klipleri projede saklar; duyamadığı ve hissedemediği şeyleri (ses, titreşim) "bakılmadı" diye işaretleyip özette sana sorar. Sonunda Türkçe rapor, referans paftası ve sana tek sayfalık bir özet hazırlar; alanın uzman ajanı inceler, bulgular plana girer. Yeni projenin ilk büyük planı bir kez de daha güçlü bir modele yalnız soru olarak sorulur (plan ve özet yapıştırılır: "yalnız verilene göre en büyük 5 risk, 5 iyileştirme, kesilecek 3 şey"); işe yarayanlar plana girer. Bir özellikte ya da yeni sürümde yalnız ilgili alanlara bakılır.

**Görsel işte senin onayın** (22 Ekim 2026'dan beri): oyunun görünüşü, ana ekranlar, mağaza görselleri ya da bir video sahnesi tasarlanmadan önce Claude farklı yönlerde 2-4 iç referans görsel hazırlar (hiçbir yerde yayımlanmaz; mağaza görselleri ve simgeler yapay zekâsız kalır), sen birini seçersin; iş seçilenle yan yana kurulur. Üç noktada onayın beklenir: referans seçimi, uzun bir işten (saatlerce render, toplu üretim) önce kısa önizleme, yükleme ya da yayın. Claude beklerken başka işlere bakar; göndermeden önce senin zevk notlarına bakar, uymayanı düzeltir ya da söyler.

**Kalite kapısı** (22 Ekim 2026'dan beri): yeni bir oyun ya da büyük bir güncelleme mağazaya veya web portalına (Poki, CrazyGames) gitmeden önce, içerik bitince ve kapsamlı testten önce bitmiş oyun türünün en çok oynanan üç oyunuyla aynı cihazda ve aynı anlarda kaydedilir: açılış, ilk dakika, aynı hareketler, ekranlar, simge ve mağaza görselleri. Projeyi bilmeyen iki ajan dört oyunu A-D diye karışık 11 alanda puanlar (ilk 60 saniye, oynanış hissi, görsel, arayüz, ses, içerik, reklam ve teklifler, teknik, erişilebilirlik, mağaza görselleri, farklılık); oyun en az bir alanda üç rakipten de iyi olmalı ve o alan oyunun kancası olmalı. Sonra oyunu hiç görmemiş bir ajan temiz kurulumla 10 dakika oynar (1.60'tan beri, senin 10 dakikalık oyunun yerine): dört soruya cevap verir (oynamaya devam eder miydin, bu oyunun tek özelliği ne, ucuz duran ne, rakiplerden hangisini seçerdin?) ve nerede takıldığını yazar. 1-3. bölümde ya da bir ekranda takılırsa oyun, düzeltilip yeni bir ajan oradan geçene kadar kapıdan geçmez. En çok iki düzeltme turundan sonra da geçmezse yeniden işlenir, yalnız uygun yerde yayımlanır (ör. yalnız Android) ya da rafa kalkar. Sonuç satırını (`KAPI: GEÇTİ` ya da `KAPI: KALDI`) bilgisayarda oturum yöneticisi varsa o, yoksa sen yazarsın. Stüdyonun öbür oyunlarına karşı da bakılır (mağazada ya da portalda olan ya da olacak uygulamalar; raftakiler GitHub'dan geçici olarak alınır, video projeleri katılmaz): her oyunun kendi arayüz görünümü ve ses efektleri, ortak görsel ya da ses dosyası yok, mağaza metinleri öbür oyunlarımıza ve ilk 3 rakibe en çok %25 benzer. App Store'a yeni oyunlar tek tek gider (incelemede aynı anda tek yeni oyun), inceleme notunda oyunun rakiplerinden farkları ve neyin stüdyonun, neyin lisanslı olduğu (oyunun lisans listesinden) yazılıdır. Fikir aşamasında da kısa bir ön kontrol var: kanca cümlesi ("‹tür›, ama ‹tek fark›, böylece ‹his›") ve türün en iyi üç oyunuyla bir tablo.

**Yayından sonra:** ölçüm olayları ilk sürümden oyunda olur. Yayından sonra en az 14 gün yeni içerik eklenmez (hata düzeltme, uyumluluk, mağaza politikası ve yorum cevapları sürer); sonra bir analiz raporu çıkar: D1, D7 ve ilk gün oyun süresi hedeflere karşı (hedefler oyun özetinin isteğe bağlı "Ölçüm hedefleri" bölümünde), oyuncunun nerede bıraktığı, oturum süresi, çökmeler, reklam ve satın alma geliri, mağaza dönüşümü, puan ve yorumlar; en çok 3 öneri. Karar senin: geliştir, bakımda tut ya da rafa kaldır (bilgisayarda oturum yöneticisi varsa onun). Yeni sürüm bu bulgulardan ve ilgili alanların kısa ön araştırmasından çıkar; yayından sonra döngü yeniden başlar.

**Test düzeni** (18 Ekim 2026'dan beri; 21 Ekim'de her adımın son testiyle): geliştirirken test yazılmaz ve koşturulmaz; her adımda yalnız hata kontrolü yapılır (kod hatasız derleniyor mu, editörsüz derleme yeter; oyun açılınca günlükte hata var mı). Her büyük parçanın sonunda Claude işi 2-3 dakika kendisi oynar ve ekran görüntüsü alır. Her adımın dosyasına, adım yazılırken "son testte nasıl denenecek, ne zaman geçmiş sayılır" yazılır. Her şey hazır denince, planın sondan bir önceki adımında kapsamlı test aşaması yapılır: her adımın son testi tek tek; yayında ayrıca bütün bölümler botla ya da çözücüyle, kayıt, aygıt matrisi (düşük ve güncel Android, tablet, iPhone), test kartlarıyla satın alma, test reklamları ve onay, ödül ve gün değişimi, analitik olaylar, performans ve bellek, iki dilde ekranlar ve gerçek dokunuşlar, erişilebilirlik, mevcut otomatik testlerin hepsi, emülatörde mağaza derlemesi ve onunla maymun koşusu (10.000 rastgele dokunuş, yalnız test reklamlarıyla), mağazanın ön yayın raporu, elle test listesi ve uzmanın incelemesi. Kırmızı çıkan madde düzeltilir, o madde ve komşuları yeniden denenir; rapor kanıtlarıyla yazılır, karar "yayınla" ise son adım (yayın) gelir. Yeni test yalnız orada, gerektiği kadar yazılır. Yayına girmeyecek prototipte bu aşama yok.

**Kaldığı yerden devam** (21 Ekim 2026'dan beri): planın her adımının üç hâli var: ✓ Tamamlandı · ▶ Devam ediyor · ○ Yapılacak (engellenen adım ⛔). Sohbetin bağlamı %90'a gelince (bir kanca ya da uyarı söyler) Claude yeni iş başlatmaz: sürmekte olan adımın dosyasına "Kaldığım yer" notunu yazar (ne bitti, sıradaki küçük iş, açık kalanlar), adımı ▶ işaretler, commit'ler ve push'lar, sonra senden `/clear` ister. `/clear`'dan sonra `devam et` demen yeter: Claude yalnız durumu, plan dizinini ve o adımın dosyasını okuyup kaldığı yerden sürer. Arka planda uzun bir iş başlatırken (derleme, yardımcı ajan) onu o an not eder; saatleri tahminle değil saatten yazar.

**Proje kaydı ve devir** (22 Ekim 2026'dan beri): projeyle ilgili her bilgi projenin içinde durur; projede çalışan oturum ya da ajan değişse de yeni gelen yalnız projeyi okuyarak devam eder. **Devir sayfası** (`docs/ai/DEVIR.md`) her oturumda yüklenir: önce okunacak 3-6 dosya, dışarıda bekleyen işler (cevap bekleyen sorular, incelemedeki mağaza gönderimleri, uzakta ya da sırada çalışan işler, bir işin gerektirdiği girişler ve konsollar (şifre asla), sana verilen sözler) ve kimden kime devredildiğini gösteren devir günlüğü. **Mağaza kaydı** (`docs/ai/hafiza/magaza.md`) kimlikleri, mağaza adlarını, her gönderim, ret ve yayının tarihli satırını, ürünleri ve fiyatları tutar. **Yazışma özeti** (`docs/ai/hafiza/yazisma.md`) sana ya da oturum yöneticisine sorulan her soruyu, cevabını ve verilen her görevi tek satırla tutar; karar veren bir cevap geldiği an tarihi ve kaynağıyla kararlara da yazılır. Devir sayfası plan kapanışında, proje devredilmeden önce ve dışarıda bekleyen bir iş başlayınca ya da bitince güncellenir. Yeni gelen Claude önce devir günlüğüne kendi satırını ekler, sonra önce okunacakları okur. Plan kapanışında `docs/ai/araclar/devir-kontrol.py` hafızanın boy sınırlarını ve her hafıza dosyasına bir dizinden ulaşılabildiğini de denetler (1.60); büyüyen kayıtların eski satırlarını `hafiza-arsiv.py` kelimesi kelimesine `hafiza/arsiv/`'e taşır, hiçbir şey özetlenip kaybolmaz.

**Proje kontrol listesi** (21 Ekim 2026'dan beri): oyun ve kanal projelerinde planın adımları el kitabındaki proje kontrol listesinden çıkar: ön araştırmadan yayın sonrasına 12 aşama, 100 madde; her maddenin ne zaman bitmiş sayıldığı, son testte nasıl deneneceği ve kaynağı yazılı. Yeni bir mobil oyunun ilk planı oradaki 41 adımlık iskeleti kopyalar (sondan üçüncü adım kalite kapısı). PC/Steam ve YouTube kanalları için farklar da orada.

**Yayın duyurusu:** bir sürüm yayına girdiği gün duyurulur: Türkçe ve İngilizce duyuru metni (`store/duyuru/<sürüm>.md`: başlık, kısa giriş, oyuncunun diliyle 3-5 yenilik, mağaza bağlantıları, kapak görseli) stüdyonun sitesinde ve topluluk devlog'unda (ör. Oyun Günlüğü) yayınlanır; devlog haftalık sınıra takılırsa not sıraya alınır. Yayınlanan commit `v<sürüm>` diye etiketlenir; birden çok oyunun varsa yeni oyun aynı gün öbür canlı oyunların "More Games" listesine eklenir (liste oyuna gömülüyse onların sıradaki sürümünde).

**Plan bitince:** Claude özet verir, yeni manuel testleri `docs/ai/manuel-testler.md`'ye ekler ve çalıştırılamadığı için "değerlendirilmedi" kalan kontrolleri söyler. Şablonun yeni bir sürümü çıkmışsa projeyi kendisi günceller ("şablonu güncelle"; CLAUDE.md'nin projeye özel kısmı, hafıza ve planlar korunur) ve ne değiştiğini tek satırla söyler. Manuel testleri istediğin zaman topluca yaparsın ("test oturumu yapalım" demen yeter). Yeni işe geçmeden `/clear` yaz; durum dosyalarda kayıtlı olduğu için hiçbir şey kaybolmaz.

**Claude karar verir:** Teknik ve tasarım seçimlerini, plana ne zaman başlayacağını ve kaç yardımcı ajan açacağını kendisi seçer, gerekçesini tek satırla yazar. Kurallar varsayılandır: uymadığı bir durumda Claude amaca en iyi hizmet edeni yapar ve nedenini söyler. Sana yalnızca kapsam, para, geri dönüşü zor işlemler ve senin vermen gereken kimlik bilgileri için sorar. Plan sürerken büyük bir iş verirsen hangisinin önce yapılacağına da kendisi karar verir ve söyler.

**Push otomatik.** Projenin uzak deposu varsa Claude her commit'ten sonra push'lar. Uzak depo ilerideyse (ör. başka bilgisayarda çalıştıysan) önce çekip birleştirir; çakışmayı iki tarafın amacı açıksa kendisi çözer, değilse sana sorar. Geçmişi yeniden yazmak gerekirse zorla push yapabilir; `--force-with-lease` kullandığı için başka bilgisayardan gelen commit'leri silmez.

**İsteğe bağlı kısa komutlar:** `plan: <iş>` · `devam` · `durum` · `planı göster` · `tüm planlar` · `adım adım` · `bunu hatırla: …` · `hafıza bakımı` · `şablonu kur` · `şablonu güncelle`

## 4. Güncellemek: `şablonu güncelle`

1. Önce GitHub Desktop'ta şablon deposu için **Fetch origin** ve **Pull** yap; şablonun yeni sürümü böyle gelir.
2. Projenin klasöründe `şablonu güncelle` yaz.

Yeni sürüm çıktığında Claude bunu projede oturumun ilk cevabında tek satırla söyler ve projeyi bir sonraki plan kapanışında kendisi günceller (1.54'ten beri); beklemek istemezsen `şablonu güncelle` yazarsın. Güncelleme birikimlidir, aradaki tüm sürümler tek seferde gelir.

- **Yenilenenler:** Çalışma kuralları (PROTOKOL, KURULUM, BAKIM), şablonlar, izin kuralları ve ayarlar, `.gitignore`'daki editör ve bilgisayar satırları, `.gitattributes`'taki `.sh` satır sonu kuralı (Unity'de ikili `.asset` dosyalarını koruyan satırlar da), Unity eklentisi, projeye uyan el kitabı girdileri. Git'te takip edilen editör dosyaları (`.vscode` gibi) takipten çıkarılır: dosyalar bilgisayarında kalır, diğer bilgisayarda bir sonraki pull'da silinir ve editör onları yeniden oluşturur.
- **Korunanlar:** Planlar, hafıza, `DURUM.md` ve projenin CLAUDE.md dosyası. CLAUDE.md'de yapısal bir değişiklik gerekiyorsa Claude yapar ve söyler (ör. 1.59'da devir sayfasının yükleme satırı). İstisnalar: El kitabı girdilerinin hafıza satırı ve plan adayları eklenir ya da güncellenir (ör. mevcut Android oyunlarında Google Play Level Up); bilgisayarda kalmış yerel notlar da hafızaya eklenir; 1.59'un proje kaydı bir kez oluşturulur ve doldurulur; 1.60'ın hafıza denetimi bulduklarını bir kez kayıpsız düzeltir ve farklılık dosyasındaki yanlış cümleyi değiştirir (aşağıda).
- **Bir kerelik dil geçişi (1.14):** 1.14'ten eski projelerde Claude önce sana sorar, sonra kendi okuduğu Türkçe dosyaları (CLAUDE.md, DURUM, HAFIZA, hafıza dosyaları, proje kuralları, bekleyen planlar) kısa İngilizceye çevirir. Bilgi kaybolmaz: her dosya ayrı commit'lenir, bir betik eski metindeki komut, yol, sayı ve tarihlerin yenisinde durduğunu denetler, orijinaller git geçmişinde kalır. Arşivdeki planlar, manuel testler ve tasarım belgeleri Türkçe kalır.
- **Bir kerelik hafıza taşıma (1.25):** Claude'un o bilgisayarda tuttuğu yerel notlar varsa projenin `docs/ai/hafiza/` klasörüne taşınır, commit'lenir ve yerel klasör silinir; yerel hafıza artık kapalıdır. Projeyi başka bir bilgisayarda da kullandıysan orada da bir kez `şablonu güncelle` de, oradaki notlar da taşınsın.
- **Bir kerelik proje kaydı (1.59):** güncelleme devir sayfasını, mağaza kaydını ve yazışma özetini oluşturur (projede zaten bir mağaza dosyası varsa hiçbir satırı silinmez). Mağaza kaydını `store/` klasöründen ve mevcut hafızadan, devir sayfasını durum dosyasından, planlardan ve bekleyen notlardan doldurur. Projenin dışında kalmış bilgileri (ör. oturum yöneticisinin hafızasındaki mağaza kayıtları ve kararlar) bir kez sorar, beklemeden sürer; cevap gelince her bilgiyi kaynağıyla ekler. Sonunda `docs/ai/araclar/devir-kontrol.py` dosyaların yerinde ve dolu olduğunu denetler.
- **Bir kerelik hafıza denetimi ve dürüst not (1.60):** güncelleme `devir-kontrol.py`'yi çalıştırır ve bulduklarını kayıpsız düzeltir: sınırı aşan kayıtların eski satırları arşive taşınır, büyük konu dosyaları bölünür, hiçbir dizinin göstermediği hafıza dosyaları dizine eklenir. Doldurulmuş farklılık dosyasının App Store notunda "All code, art and audio were made for this game" yazıyorsa o satır "neyin bizim, neyin lisanslı" satırına çevrilir ve oyunun lisans listesi (`docs/ai/tasarim/lisanslar.md`) oluşturulur; gönderilmiş notlar ve kapı kayıtları olduğu gibi kalır.
- **Sürümü görmek:** `docs/ai/PROTOKOL.md` dosyasının 2. satırında.

## 5. El kitabına kaynak eklemek

1. **Claude'a ver.** Claude Code'u şablon klasöründe aç ve "bu videoyu el kitabına ekle: <link>" yaz. Claude in Chrome bağlıysa Claude videoyu senin Chrome'undaki Gemini'ye kendisi analiz ettirir.
2. **Chrome bağlı değilse** videoyu Gemini'ye sen analiz ettir (prompt `el-kitabi/NASIL.md` dosyasında; başındaki üç satırı doldur) ve notu Claude'a yapıştır.
3. **Claude gözden geçirir ve ekler.** Koşulu daraltır, yanlışları düzeltir, eksik tuzakları ekler; sonra sürümü artırır, commit'ler ve push'lar.
4. **Projelere dağıt.** Projelerde `şablonu güncelle` dersen girdi, koşulu tutan projelere kurulur. Tutmayan projelerde bağlam maliyeti sıfırdır.

**Projeden gelen notlar:** Claude bir projede el kitabı girdisine yeni not eklerse "şablonu güncelle" bu notları silmez ve şablona önerir. Şablona almak için şablon klasöründe "<proje> projesinin el kitabı önerisini ekle" demen yeterli.

## 6. Şablonu geliştirmek

- Claude Code'u şablon klasöründe aç ve değişikliği iste. Klasörün kendi CLAUDE.md dosyası kuralları hatırlatır: sürümü artır, kontrol et, commit'le, push'la.
- Sürümler git etiketleriyle işaretli (v1.3, v1.4, …). GitHub Desktop'ta **History** sekmesinde görünür.

## 7. Sorun giderme

| Durum | Ne yapmalı |
|---|---|
| Kullanım hakkı bitti, iş yarıda kaldı | Hakkın yenilenince aynı ya da yeni bir oturumda `devam` yaz |
| Claude "şablonu kur"u tanımıyor | Global yönlendirme eksik (bölüm 1, adım 2). Geçici çözüm: şablondaki `docs/ai/` klasörünü projeye kopyala ve "docs/ai/KURULUM.md dosyasını oku ve uygula" yaz |
| Claude protokolü atlıyor | "protokole göre ilerle" de. Sık oluyorsa CLAUDE.md 160 satırı ya da 10.000 karakteri aşmış olabilir |
| Sohbet çok uzadı | Plan bitince `/clear` yaz; durum dosyalarda kayıtlı. Bağlam %90'a gelince Claude kaldığı yeri adımın dosyasına yazıp `/clear` ister; sonra `devam et` yaz |
| Kurulumda `‹?›` işaretli yerler var | Claude emin olamadığı komut ve kuralları işaretler; netleştir, o da düzeltir |
| Hafıza ya da plan dosyasını okumak istiyorum (İngilizce) | Claude'a "şunu Türkçe özetle" de |
| Bir projede superpowers'ı kullanmak istiyorum | Şablon onu projelerde kapatır. O projede `.claude/settings.local.json` dosyasına `"enabledPlugins": {"superpowers@claude-plugins-official": true}` yaz; yalnızca senin bilgisayarında açılır |
| Unity testleri takılıyor | Testler derleme bitmeden başlatılmaz. Editör açıkken Pipeline'ın test komutu kullanılır; o yoksa editör kapatılır ve testler projedeki `docs/ai/araclar/testler.sh` ile koşar: projenin kendi Unity sürümü, kendi log dosyası, en çok 30 dakika. `unity test` kullanılmaz: log seçeneği yok, senin açık editörünün de kullandığı ortak `Editor.log`'a yazıyor. Test Framework paketi yoksa testler hiç çalışmaz. Bellek az harcansın diye editör tek içe aktarma işçisiyle açılır; ilk açılış (boş `Library/`) ya da büyük bir içe aktarma yavaş kalırsa Claude işçi sayısını `IMPORT_WORKERS` ile artırır |
| agent-protocols ya da engineering skill'leri görünmüyor | 1.55'ten beri bilerek kapalı: agent-protocols'ün oturum başı kancası Windows'ta bozuk JSON üretiyordu, iki eklentinin skill'leri de kullanılmıyordu. Kurulum ve güncelleme ikisini kullanıcı düzeyinde kapatır, unity-perf'i kaldırır. Bir oturumda hâlâ görünüyorlarsa yeni oturum aç |
| Claude "tarayıcıda açtım" diyor ama bir şey göremiyorum, ya da Chrome bağlantısı hata veriyor | Claude sırayla kendisi dener: kendi profilinin penceresini öne getirir ve hangi pencerede olduğunu söyler; bu bilgisayardaki tarayıcıya mı bağlı diye bakar (aynı hesap öbür bilgisayarda da bağlı olabilir); bağlantıyı yeniden kurar; kendi profilini kapatıp açar. Eklentide giriş düşmüşse girişi sen yaparsın. Chrome'u tamamen kapatıp açmak senin pencerelerini de kapatır; bunu yalnızca sen yaparsın |

## 8. İpuçları

- **Claude'un dosyaları İngilizce, konuşma Türkçe.** Protokol, durum, hafıza, planlar ve kurallar daha az token harcasın diye kısa İngilizce maddelerle yazılır. Manuel testler ve tasarım belgeleri Türkçe kalır.
- **Plan modu (Shift+Tab) ile de çalışır.** Onaylanan plan şablonla `docs/ai/planlar/` altına kaydedilir.
- **Dosyaları elle de düzenleyebilirsin.** Claude bir sonraki okumada değişikliğini görür.
- **`docs/ai/` git'e dahil olmalı** ki hafıza da versiyonlansın ve bilgisayarlar arasında taşınsın; Claude bilgisayarda ayrı bir hafıza tutmaz. Proje GitHub Pages'i `docs/` klasöründen yayınlıyorsa bu klasör de yayınlanır; Pages'in kaynak klasörünü değiştir ya da `_config.yml` içine `exclude: [ai]` ekle.
- **Paralel oturum (worktree) kullanıyorsan** her branch kendi `DURUM.md`'sini taşır; birleştirirken bu dosyada çakışma çıkarsa güncel olanı tut.
