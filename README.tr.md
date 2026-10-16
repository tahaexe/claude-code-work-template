# Claude Çalışma Şablonu

[English](README.md) · **Türkçe**

Claude Code için, her projede kullanılabilen bir çalışma sistemi. Kurulduğu projede Claude şunları yapar:

- **İşi önce anlar, kararı kendisi verir.** Büyük işleri inceleyip plana bağlar ve başlar. Onayını yalnızca senin kararın gerekiyorsa (kapsam, para, geri dönüşü zor işlem) ya da iş fazlara bölünecek kadar büyükse bekler.
- **Plana göre ilerler.** Planı adım adım, sonuna kadar kendisi uygular. Her adımı doğrular, plana işler, commit'ler ve push'lar.
- **Hafızasını yönetir.** Kararları, dersleri ve kaldığı yeri projenin içindeki dosyalarda tutar, böylece oturumlar ve bilgisayarlar arasında unutmaz.
- **Bağlamı (context) korur.** Her oturumda yalnızca küçük bir çekirdek yüklenir, gerisini gerektiğinde okur.
- **Tarayıcı işini kendisi yapar.** Tarayıcı gereken işleri (Play Console, Gemini, bir sayfayı kontrol etmek) izin almadan Chrome'daki kendi profilinde Claude in Chrome ile yapar (her Claude hesabının kendi adını taşıyan bir profili olur, ör. `alex`); senin profillerine ve başka tarayıcılara dokunmaz, yalnızca Claude'un kendi güvenlik onayları kalır.

Komut ezberlemen gerekmez, Claude'la normal konuşman yeterli.

> **Hızlı başlangıç, komutlar ve sorun giderme için [Kullanım Kılavuzu](KILAVUZ.md).**

> Şablon sürümü: **1.50** (2026-10-16) · Unity projeleri için ek bir eklenti içerir (aşağıda).

---

## Nasıl çalışır?

| Katman | Dosyalar | Ne zaman yüklenir |
|---|---|---|
| **Çekirdek** | `CLAUDE.md`, `PROTOKOL.md`, `DURUM.md`, `HAFIZA.md` | Her oturumda, otomatik |
| **Aktif iş** | `planlar/<aktif plan>.md` | O plan üzerinde çalışılırken |
| **Bilgi** | `hafiza/*.md` | Konu gerektirdiğinde (hafıza dizini yönlendirir) |
| **Nadir** | `sablonlar/`, `BAKIM.md`, `KURULUM.md` | Plan yazarken, plan bitince, kurulumda |
| **Projeye özel kurallar** | `.claude/rules/*.md` | Yalnızca eşleşen dosyalar okunduğunda |

**Dil:** Claude'un kendi okuduğu dosyalar (protokol, durum, hafıza, planlar, kurallar, el kitabı) kısa İngilizce maddeler hâlinde yazılır, böylece daha az token harcanır. Claude seninle Türkçe konuşur. Senin okuduğun dosyalar Türkçe kalır: manuel testler, tasarım belgeleri, bu README ve KILAVUZ.

```text
İstek
 ├─ Küçük iş → yap → doğrula → commit + push
 └─ Büyük iş → keşfet → (soru) → plan yaz → başla
                 (senin kararın gerekiyorsa ya da iş fazlıysa önce SENİN ONAYIN)
                                               ↓
    Her adım:  uygula → doğrula → plana işle → commit + push → sonraki adım
               (engel · karar · planda olmayan riskli işlem → durur ve sorar)
                                               ↓
    Kapanış:   özet + manuel testler (manuel-testler.md) + hafıza güncellemesi + arşiv
```

## Klasör yapısı (kurulumdan sonra projede)

```text
proje/
├─ CLAUDE.md                 proje bilgisi: kurulumda Claude doldurur
├─ .claude/rules/            projeye özel kurallar: kurulumda Claude yazar
├─ .claude/settings.json     izin kuralları: kurulumda eklenir, bağlam harcamaz
└─ docs/ai/
   ├─ PROTOKOL.md            çalışma kuralları          (sabit)
   ├─ KURULUM.md             kurulum ve güncelleme      (sabit)
   ├─ BAKIM.md               kapanış ve temizlik        (sabit)
   ├─ sablonlar/             CLAUDE.sablon.md, plan.md  (sabit)
   ├─ araclar/               kayip-kontrol.py           (sabit)
   ├─ DURUM.md               neredeyiz
   ├─ HAFIZA.md              hafıza dizini
   ├─ manuel-testler.md      senin yapacağın testler (Türkçe)
   ├─ hafiza/                kararlar.md, dersler.md, teknik-borc.md, …
   └─ planlar/               YYYY-MM-DD-ad.md, arsiv/
```

**Sabit** dosyalar her projede aynıdır ve şablondan güncellenir. Diğerleri projenin kendi verisidir.

Unity projelerinde ayrıca şunlar kurulur: `.claude/agents/unity-uzmani.md`, `.claude/rules/unity-*.md`, `docs/ai/sablonlar/oyun/` ve doldurulan tasarım belgeleri için `docs/ai/tasarim/`. Koşulu tutan el kitabı girdileri de `docs/ai/el-kitabi/` altına kurulur.

---

## Kurulum ve kullanım

Adım adım kurulum (global yönlendirme dahil), günlük kullanım, güncelleme, ipuçları ve sorun giderme [Kullanım Kılavuzu](KILAVUZ.md)'nda. Kısaca:

1. Bu repoyu klonla, örneğin `C:\Users\<kullanıcı>\claude-code-work-template` klasörüne.
2. Kılavuzdaki (bölüm 1) global yönlendirme bloğunu, şablon ve Unity klasörlerinle birlikte `~/.claude/CLAUDE.md` dosyasına ekle. Bu blok olmadan Claude "şablonu kur" sözünü tanımaz.
3. Projede **"şablonu kur"** de. Claude proje türünü klasörden anlar (anlayamazsa Unity mi Diğer mi diye sorar) ve gerisini kendisi yapar.
4. Şablon geliştikçe projede **"şablonu güncelle"** de. Yalnızca sabit dosyalar yenilenir; planlar, hafıza ve CLAUDE.md korunur. Yeni sürüm çıktığında Claude bunu oturumun ilk cevabında tek satırla hatırlatır.
5. Günlük işte normal konuş. Büyük işler plana bağlanır ve adım adım ilerler; her adım commit'lenip push'lanır.

---

## Unity eklentisi

"şablonu kur" deyip proje türü olarak Unity'yi seçtiğinde, genel kurulumla birlikte Unity eklentisi de kurulur. Eklenti şablonda `eklentiler/unity/` klasöründe durur.

| Eklenen | Projede nerede | Ne zaman yüklenir |
|---|---|---|
| Unity bölümü: skill'ler, Unity CLI, doğrulama, C# kod zekâsı | `CLAUDE.md` içinde | Her oturumda |
| Unity uzmanı ajanı (sadece okur ve inceler; çağrılınca CLAUDE.md zincirini yüklemez) | `.claude/agents/unity-uzmani.md` | Tanımı her oturumda (~70–90 token), kendisi çağrılınca |
| Kod kuralları: varlıklar, oyun kodu, UI, test, shader | `.claude/rules/unity-*.md` | Yalnızca eşleşen dosyalar okunduğunda |
| Test çalıştırıcı: editör kapalıyken testleri projenin Unity sürümüyle, kendi log dosyasıyla, süre sınırıyla ve tek içe aktarma işçisiyle (daha az bellek) koşar | `docs/ai/araclar/testler.sh` | Editör kapalıyken test koşulduğunda |
| C# kod zekâsı: her `.cs` düzenlemesinden sonra yeni derleyici hataları, tanım ve referansları sembolle bulma (`csharp-lsp` eklentisi, `csharp-ls` dil sunucusu; tuzakları el kitabı girdisinde) | `.claude/settings.local.json` (git'e girmez; her bilgisayarda ve her Claude hesabında ayrı kurulur) | Her oturumda etkin; hata raporu bir `.cs` dosyası düzenlenince gelir |
| Unity proje ayarları: platforma göre doğru değerler (el kitabı girdisi) | `docs/ai/el-kitabi/unity-proje-ayarlari.md` | Yeni projede, platform eklerken, yayın hazırlığında, performans ve boyut işlerinde |
| Oyun tasarım şablonları: oyun özeti (tasarım sütunlarıyla), GDD, görsel stil rehberi, prototip raporu, oyun testi raporu, post-mortem, yayın kontrol listesi | `docs/ai/sablonlar/oyun/` (doldurulanlar `docs/ai/tasarim/`) | Kullanıldığında |

**Unity CLI ve skill'lerin unutulmaması için üç katman var:**
1. CLAUDE.md'deki Unity bölümü her oturumda şunu hatırlatır: önce uygun `unity:*` skill'i kullanılır; editör, derleme (`unity recompile`) ve build işleri Unity CLI ile yapılır. Testler açık editörde Pipeline'ın test komutuyla, editör kapalıyken `docs/ai/araclar/testler.sh` ile koşar; `unity test` kullanılmaz (log seçeneği yok, açık editörünün de kullandığı ortak `Editor.log`'a yazıyor). Unity'ye bağlantıda önce Unity CLI kullanılır (senin tercihin); skill'lerin MCP adımları da CLI ile yapılır. Unity MCP yasak değil: CLI'ın yetmediği yerde Claude kullanabilir ve bunu söyler. CLI ya da Pipeline paketi eksikse kurulur (şablon sahibinin bilgisayarında sormadan, başkasında bir kez sorarak).
2. Plandaki her adımın **Araç** alanı. Skill ya da araç plan yazılırken seçilir, otomatik ilerlerken adımda hazır durur.
3. Unity kuralları, ilgili dosyalar okunduğunda devreye girer.

**Kurulum sırasında ayrıca:**
- Unity CLI'ı, Unity'nin Claude eklentisini (`unity:*` skill'leri) ve C# kod zekâsını (`csharp-ls` ve `csharp-lsp`; bilgisayarda .NET 10 SDK'sı yoksa atlanır) kontrol eder, eksikse kurar: şablon sahibinin bilgisayarında sormadan, başkasında bir kez sorarak. Açık bir editör olup olmadığına bakar.
- Eksik paketleri ekler: CLI'ın editörü kontrol edebilmesi için `com.unity.pipeline`, testler için `com.unity.test-framework`.
- Doğrulama komutlarını CLAUDE.md'ye yazar (gerçek bir projede çalıştığı görülen komutlar varsayılandır).
- Kural dosyalarını projenin klasör yapısına göre uyarlar.
- Kodu olan bir projede mimariye bakar: global singleton'lar ve dev yönetici sınıfları varsa sıraya "servis mimarisine geçiş" plan adayı ekler. Kod, sen o planı başlatana kadar değişmez.

**Kod mimarisi:** SOLID, temiz kod ve servis yapısı oyun kodu kuralında kısa maddeler olarak yazılı: servisler arayüzün arkasında durur ve tek bir başlangıç noktasında kurulur, her sınıfın tek sorumluluğu olur, eski kod adım adım taşınır. Yeni bir oyunda ilk plan servislerin kurulduğu başlangıç noktasıyla başlar.

**Görsel kimlik:** Her oyun için bir görsel stil rehberinin (renkler, yazı tipleri, arayüz dili, sahne görünümü) taslağını ilk UI işinden önce Claude yazar, sen düzeltirsin. Oyuncunun gördüğü bir şeyi değiştiren her adımdan sonra Claude ekran görüntüsü alıp rehberle karşılaştırır, açık sapmaları düzeltir, zevke bağlı olanları manuel testlere yazar. Zevk kararı sende; Claude rehbere uyumu kontrol eder. Kapanışta Unity uzmanı ekranları tutarlılık açısından da inceler.

**Arka planda çalışır:** Sen çalışırken editör penceresiz açılır, build ve test oyunları arka planda koşar. Bir pencere ancak bir test gerektirirse ve sana söylendikten sonra öne gelir. Unity CLI'ın sahada öğrenilen tuzakları "Unity CLI saha notları" el kitabı girdisinde (aşağıda).

**Yayın:** Claude mağazalarda (Play Console, App Store Connect) yeni sürümü oluşturur ve sürüm verilerini girer: sürüm adı, iki dilde yenilikler notu, gerekiyorsa mağaza sayfası. Yayın her zaman doğrudan: Play'de üretim kanalı ve %100, App Store'da onaydan sonra otomatik yayın; test kanalı, TestFlight ve kademeli yayın yok. Sürüm numaralarını ayarlar, Android (imzalı AAB) ve iOS (Xcode projesi) build'lerini proje klasöründe `Builds/` altına alır ve bekler. Build'leri mağazalara sen yükler, incelemeye sen gönderirsin; Claude build yüklemez ve incelemeye göndermez. Android imzası için keystore şifresini açık editöre sen girersin; şifre hiçbir dosyaya, belgeye ya da komuta yazılmaz.

**Android oyunları:** Google Play'in Level Up ile önerdiği oyun yapısı (Play Games Services girişi, başarımlar, Play Games Ödülleri, Game Stats, bulut kayıt, FPS, büyük ekran, kumanda) için el kitabı girdisi kurulur. Girdi Play Games Services'in Play Console kurulumunu (onay ekranı, imza parmak izleri, yapılandırmayı yayınlama), güncellemeler için tanıtım içeriğini, Play Console uyarılarını (R8, uçtan uca ekran), Level Up'ın getirisini (ücretler, Görevler), Şubat 2027'de başlayan bellek eşiklerini, ilk yayını ve geçiş reklamının yerini de anlatır. DURUM'daki **Up next** listesine bu yapıyı doğru sırayla ekleyen üç plan adayı ve uyarılar için bir plan adayı yazılır (aşağıda "El kitabı").

**iOS oyunları:** Aynı yapının App Store karşılığı için ayrı bir el kitabı girdisi kurulur: Game Center girişi ve başarımlar (Play'dekiyle aynı liste), satın alımları geri yükleme düğmesi, güncellemeler için uygulama içi etkinlikler, kalite maddeleri, doğrudan yayın ayarları ve incelemeye göndermeden önce bakılacaklar (ret riskleri, gizlilik, yaş anketi, iPad, erişilebilirlik etiketleri). Play Games Ödülleri ve Game Stats'in iOS'ta karşılığı yok. Bir plan adayı yazılır.

> Uyarlama kaynağı: Claude-Code-Game-Studios, sürüm `7ed2c3e` (2026-09-24). O repo güncellenirse bu sürümle karşılaştırılır.

---

## El kitabı

Belirli bir teknoloji, platform ya da asset paketiyle ilgili, dışarıdan (video, makale, resmi belge) derlenmiş notlar. Şablonda `el-kitabi/` klasöründe durur.

- **Sadece gereken projeye kurulur.** Her girdinin başında bir koşul var, örneğin "projede Synty Sidekick karakterleri var". Kurulumda ve "şablonu güncelle" dediğinde koşulu tutan girdiler projeye kopyalanır ve hafıza dizinindeki ortak el kitabı satırına birkaç kelimelik bir ipucuyla eklenir. Koşul tutmuyorsa hiçbir şey eklenmez, o projede bağlam maliyeti sıfır olur.
- **Sadece ilgili işte okunur.** Girdinin kendisi yalnızca o konuda bir iş yapılırken açılır.
- **Gereken araçlar önerilir.** Girdi bir araç gerektiriyorsa (örneğin Sidekick Character Creator) ve projede yoksa Claude kurmayı önerir. İstemezsen geçer ve bir daha sormaz.
- **Gerekirse plan adayı ekler.** Girdi projede yapılması gereken bir iş tanımlıyorsa (örneğin Google Play Level Up), kurulunca bu iş DURUM'daki **Up next** listesine plan adayı olarak yazılır. İş zaten yapılmışsa eklenmez.
- **Projede eklenen notlar kaybolmaz.** Claude bir projede girdiye yeni saha notu eklerse "şablonu güncelle" bunları korur ve şablona önerir. Böylece bir projede öğrenilen, diğer projelere de taşınır.
- **Girdiler İngilizce:** Onları Claude okuduğu için kısa İngilizce maddelerle yazılır.

| Girdi | Koşul | Ne zaman okunur |
|---|---|---|
| Synty Sidekick: yüz ifadeleri ve göz kırpma | Projede Sidekick karakterleri var | Yüz ifadesi, blendshape, göz kırpma ve Face katmanı işlerinde |
| Synty: gündüzü geceye çevirme | Projede Synty ortam asset'leri var ve proje URP kullanıyor | Gece atmosferi, ortam ışığı, sis, gökyüzü, post-processing ve iç mekân ışığı işlerinde |
| Synty karakterlerine editörde poz verme | Projede Synty karakterleri var | Poz verirken ve tanıtım, mağaza ya da konsept görseli hazırlarken |
| Unity'de ortam sesi (2D) ve 3D konumsal ses | Unity projesi (Synty'ye özgü değil) | Ortam sesi ya da 3D ses eklerken, ses sorunlarında |
| Google Play'in önerdiği oyun yapısı (Level Up) | Unity projesi, hedefte Android (Google Play) | Google Play yayını (ilk yayın dahil), Play Games Services, başarım, ödül, satın alma, Game Stats, bulut kayıt, FPS, büyük ekran ve kumanda işlerinde; Level Up'ın getirisine (ücretler, Görevler) bakarken; Play Console uyarıları (R8, uçtan uca ekran), Android vitals bellek ölçümleri, tanıtım içeriği ve yayın ayarlarında; geçiş reklamını yerleştirirken. Kurulunca 4 plan adayı ekler |
| App Store yapısı: Game Center, uygulama içi etkinlikler, ilk gönderim, doğrudan yayın | Unity projesi, hedefte iOS (App Store) | App Store yayını ve ilk gönderim (ret riskleri, gizlilik ve ATT, gizlilik bildirimleri, yaş anketi, iPad pencere boyutu, erişilebilirlik etiketleri), Game Center girişi, başarım, liderlik tablosu, iOS'ta satın alma, uygulama içi etkinlik ve iOS kalite işlerinde. Kurulunca 1 plan adayı ekler |
| Unity proje ayarları (Unity 6.3; Android, iOS, PC) ve git'te Unity'nin ikili `.asset` dosyaları | Unity projesi | Yeni proje kurarken (hemen uygulanır), platform eklerken, yayın hazırlığında, FPS, bellek, boyut ya da build sorunlarında; `.gitattributes` yazarken ya da pişmiş bir varlık (NavMesh, ışık, arazi) bilgisayarlar arasında farklı çıktığında. Project Auditor ile ayar denetimi için 1 plan adayı ekler |
| Unity CLI saha notları ve penceresiz editör | Unity projesi | Rutin derleme ve test dışındaki Unity CLI işlerinde (editörü sürme, eval, ekran görüntüsü, PlayMode testleri, paketler, build) ve bir komut beklenmedik davrandığında. Küçük penceresiz işlerde editör tek içe aktarma işçisiyle açılır (bir projede bellek tepesi 8,1 GB'tan 4,4 GB'a indi, süre aynı kaldı). İki Unity projesinin saha notlarından derlendi |
| Shader derleme takılması: ölç, izle, ısındır (Unity 6 `GraphicsStateCollection`) | Unity 6 projesi | Bir efekt, malzeme, bölge ya da kalite düzeyi ilk kez göründüğünde build takıldığında; yayın, demo ya da mağaza videosu çekimi hazırlarken; DX12, Vulkan ya da Metal'e geçerken; yeni kalite düzeyleri ya da çok sayıda yeni malzeme eklerken. Bir proje oturumunun araştırmasından |
| Tarayıcı bağlantısı: her Claude hesabına kendi Chrome profili | Her proje | Claude'a tarayıcı profili kurulurken, Claude in Chrome bağlanmadığında, hata verdiğinde ya da sekme açamadığında; Claude "açık" deyip senin bir şey görmediğinde (sıralı sorun giderme adımları). Bir projenin saha notlarından derlendi |
| Layer Lab GUI Pro arayüz paketleri (Casual Game, Survival Clean, Fantasy RPG) | Projede GUI Pro paketi var ya da arayüz GUI Pro ile yenilenecek | Arayüz denetiminde, paketten parça alırken, düğme ve dokunma alanı ölçerken, Unity 6000.6'da güvenli alan işinde |
| Firebase ile oyuncu hunisi, D1/D7 tutma ve uzaktan ayar | Unity projesi, hedefte Android ya da iOS, projede Firebase Unity SDK'sı var | Analitik olayı planlarken ya da eklerken, oyuncunun nerede bıraktığına bakarken, Remote Config ya da A/B testi kurarken, zorluk ya da ödül kararında, yeni olaylardan sonra mağaza gizlilik beyanlarında |
| Mağaza sayfası ve ASO (Google Play, App Store) | Google Play'de ya da App Store'da yayınlanan proje | Mağaza metni, simge, ekran görüntüsü (App Store'un zorunlu ölçüleri dahil) ya da önizleme videosu hazırlarken; mağaza A/B testi ya da App Store özel ürün sayfası planlarken; puan isteme zamanını seçerken; sayfayı incelemeye göndermeden önce |
| Mağaza etkinlikleri: Google Play tanıtım içeriği ve App Store uygulama içi etkinlikleri (ücretsiz görünürlük) | Google Play'de ya da App Store'da yayınlanan oyun ya da uygulama | Oyuncunun göreceği yeni içerik getiren bir sürümü (bölüm, mod, bölge, sezon) ya da süreli bir oyun içi etkinliği planlarken; tanıtım içeriği ya da uygulama içi etkinlik yazarken, gönderirken ve sonucunu ölçerken; mağaza birini reddettiğinde. Şablon kuralı: yeni içerikli her sürümün planında bir mağaza etkinliği adımı. Bir proje oturumunun araştırmasından |
| C# kod zekâsı: `csharp-lsp` eklentisi ve `csharp-ls` dil sunucusu; Unity için editörsüz derleme denetimi | Unity projesi ya da `.csproj` dosyaları olan herhangi bir C# projesi | C# kod zekâsını kurarken ya da denetlerken; bir `.cs` düzenlemesinden sonra hata raporu gelmediğinde ya da LSP çağrıları hata verdiğinde; yeni bir dosyada ya da yeni asmdef'lerden sonra olmayan hatalar göründüğünde; başka bir projenin C# koduna dokunurken; editör açılamazken (meşgul, kapalı ya da ağır iş sırası bekleniyor) Unity C# kodunu saniyeler içinde denetlerken. Bir Unity projesinde denendi; derleme denetimi iki projeden |
| Adil zorluk ve başarısızlık: oyuncunun kaybı kendi seçimine bağlayabilmesi, başarısızlık döngüsü, algılanan şans, akış, bölüm zorluğu puanı | Unity oyun projesi | Zorluğu ve zorluk eğrisini ayarlarken; çözücüyle üretilen ya da denetlenen bölümleri puanlarken; bölüm başına başarısızlık oranını ve deneme sayısını okurken; ölüm, tekrar deneme, devam ve kayıt noktalarını tasarlarken; boss ve özel düşmanlarda; ganimet, ödül ya da teklif olasılıklarında; oyuncular bir şeye "haksız" dediğinde; oyun testi raporundaki kayıpları okurken |
| Hedef katmanları, güvenli bırakma noktaları, geri dönüş nedenleri ve sağlıklı liderlik tablosu | İlerlemesi, etkinlikleri ya da liderlik tablosu olan mobil oyun | Bölüm, ödül ve hedef akışını tasarlarken; günlük ödül, seri, etkinlik, bildirim ya da liderlik tablosu eklerken; oturumun nerede bitebileceğine karar verirken; oyuncuların neden geri dönmediğine bakarken (D1/D7) |
| Rakip ya da referans oyun incelemesi (katmanlı okuma) | Oyun projesi; yalnızca istenince kullanılır | Yalnızca sen ya da bir plan bir rakip veya referans oyunun incelenmesini istediğinde. Claude kendiliğinden araştırma başlatmaz, kontrol etmediği bilgiyi yazmaz |
| Renk körlüğüne dayanıklı palet (renk eşleştirmeli oyunlar) | Oyunun ana kuralı parçaları renkle ayırıyor (renk sıralama, jam, eşleştirme, renk savunma) | Oyunda anlamı olan renkleri, zemini ya da onları boyayan ışığı seçerken; stil rehberini yazarken; renk körü kipi planlarken; paleti gösteren mağaza görsellerinden önce; bir oyuncu iki rengin benzediğini söylediğinde. Ölçüm aracı `cvd_palette.py` birlikte gelir |
| Lansman haftasında kısa video (YouTube Shorts, TikTok, Instagram Reels), reklam bütçesi olmadan | Mağazada (Google Play, App Store) yayında olan ya da çıkışa hazırlanan oyun (büyük bir güncellemenin tanıtımı dahil) | Lansman haftasını (L-5 → L+7) ya da büyük bir güncellemenin tanıtımını planlarken; kısa video hazırlayıp paylaşırken; video platformlarına mağaza bağlantısı koyarken; ön kayıt, ön sipariş ve özel mağaza sayfası bağlantılarında; içerik üreticilerine ulaşırken; ilk günlerin sayılarını okurken. Tanıtım oturumunun araştırmasından |
| Kısa videolarda izlenme verisini okumak ve haftalık ölçüm (YouTube Shorts, TikTok, Instagram Reels) | Oyunları için kısa video paylaşan proje ya da klasör | Paylaşılan klipleri değerlendirirken, sonraki kesimi ya da denemeyi planlarken, haftalık tanıtım bakışında, izlenmesi sıfıra yakın bir klipte ya da hesapta, ölçüm çekişini (YouTube Analytics API) kurarken |

**Yeni girdi eklemek:** Claude Code'u şablon klasöründe aç ve "bu videoyu el kitabına ekle: <link>" yaz. Claude in Chrome bağlıysa Gemini analizini Claude kendisi yaptırır; değilse Gemini'nin çıkardığı notu yapıştır. Adımlar ve Gemini prompt'u `el-kitabi/NASIL.md` dosyasında.

---

## Ayarlar (bağlam harcamaz)

Bunlar Claude Code'un kendi ayarları. Claude'a gösterilmedikleri için bağlam ve kullanım hakkı harcamazlar.

- **İzin kuralları** (`.claude/settings.json`, kurulumda eklenir):
  - Adım commit'leri ve push (`git add`, `git commit`, `git mv`, `git push`) onay beklemeden çalışır. Zorla push yasak değil: geçmişi yeniden yazmak gerektiğinde Claude `--force-with-lease` ile yapar, başka bilgisayardan gelen commit'ler silinmez.
  - Unity projelerinde doğrulama komutları (`unity status`, `recompile`, `test`, `list`) ve Pipeline paketinin kurulumu (`unity pipeline install`) da onaysız çalışır.
  - Claude in Chrome araçları da onaysız çalışır. Sayfada JavaScript çalıştırma, serbest C# gibi, izin moduna bağlı kalır.
  - Silme, diğer paket eklemeleri, build ve serbest C# çalıştırma, bypass modu dışında izin penceresi açar.
  - Böylece otomatik ilerlerken izin sorularına takılma azalır.
- **Plugin'ler** (`enabledPlugins`): superpowers projelerde kapalı, çünkü her oturuma "şu skill'i kullanmak zorundasın" diyen katı bir akış getiriyor; şablon sahibinin bilgisayarlarında kurulum ve güncelleme onu kullanıcı düzeyinde de kapatır (1.33). plugin-dev yalnızca şablon geliştirmede gerekiyor: projelerde kapalı, şablon klasöründe açık. Projede oturum başına tahminen 1,9–3,2 bin token tasarruf sağlar.
- **Skill listesi** (`skillOverrides`): Masaüstü uygulamasının her oturuma eklediği agent-protocols ve engineering skill'leri yalnızca adıyla listelenir. Uzun açıklamaları bağlama girmez, Unity skill'lerine yer kalır; Claude bir adımda gerekirse yine çağırır. PROTOKOL'de bu iki grubun ne işe yaradığını anlatan tek satır var. unity-perf skill'leri gizli; Unity için yalnızca Unity'nin resmi skill'leri kullanılır.
- **Eklentiler:** Kurulum ve güncelleme, agent-protocols ile engineering eksikse onları kullanıcı düzeyinde kurar (şablon sahibinin bilgisayarında sormadan, başkasında bir kez sorarak); `tianzhiying/unity-perf` bulunursa kaldırır. Masaüstü uygulaması eklentileri claude.ai hesabına göre getirdiği için hesaplar arasındaki fark böylece kapanır.
- **Ajanlar ajan açamaz** (`env`): Kaç yardımcı ajan açılacağına Claude karar verir. Tek sınır, bir ajanın kendi ajanını açamaması: o maliyeti ana Claude göremez. Masaüstü uygulamasının bu değişkene uyduğu henüz doğrulanmadı.
- **`/batch` kapalı** (`skillOverrides`): Her parça için ayrı worktree ve PR açan akışı, projelerin tek dal ve adım commit'i düzenine uymuyor. `/simplify` açık; Claude gerekirse kendisi kullanır.
- Kurulumdan sonra yeni bir oturumda bir kez `/context` yazman önerilir: çekirdek dosyalar görünmeli, kapatılan plugin'lerin skill'leri görünmemeli.
- **Bildirimler:** Masaüstü uygulamasında "görev bitti", "soru var" ve "izin gerekiyor" bildirimleri zaten varsayılan olarak açık, uygulama ayarlarından değiştirilebilir.
- **Durum satırı (statusLine):** Sadece terminal arayüzünde görünüyor. Masaüstü uygulamasında gösterilmediği için eklenmedi.
- **Yerel hafıza kapalı** (`autoMemoryEnabled`): Claude'un bilgisayarda tuttuğu otomatik hafıza projelerde kapalı; Claude onu ne okur ne de oraya yazar. Tüm hafıza projenin `docs/ai/` klasöründe ve git'te durur, böylece başka bir bilgisayarda çalışırken hiçbir şey kaybolmaz. Kurulum ve güncelleme, bilgisayarda kalmış eski notları önce projeye taşır, sonra o yerel klasörü siler.
- **`.gitignore`:** Kurulum ve güncelleme, editöre ve bilgisayara özel dosyaları yok sayılanlara ekler: `.vscode`, `.idea`, `.vs`, Claude'un yerel ayarları ve worktree'leri, Windows ile macOS'un ürettiği dosyalar; Unity'de ayrıca Unity'nin ürettiği çözüm dosyaları. Var olan satırlara dokunmaz. Bu dosyalar git'te takip ediliyorsa takipten çıkarır: dosyalar bilgisayarda kalır, diğer bilgisayarda bir sonraki pull'da silinir ve editör onları yeniden oluşturur. Böylece `git status` temiz kalır ve bilgisayarlar arasında çakışma çıkmaz.
- **`.gitattributes`:** Kurulum ve güncelleme `*.sh text eol=lf` satırını ekler, var olan satırlara dokunmaz. Windows'ta git satır sonlarını çevirdiği için (`core.autocrlf=true`) yeni bir klonda `.sh` betikleri (ör. test çalıştırıcı) CRLF ile geliyor ve bash'te çalışmıyordu. Unity projelerinde `.asset` dosyalarını metin sayan bir kural (`*.asset text eol=lf` gibi) varsa, Unity'nin ikili yazdığı `.asset` dosyaları (pişmiş NavMesh, ışık verisi, arazi) için onun arkasına `binary` satırları eklenir: yoksa her commit bu dosyalardaki CR LF baytlarını siler ve dosya öbür bilgisayarda bozuk çıkar (bir projenin NavMesh'inde görüldü).

---

## Bağlam bütçesi

**Ölçüm** (bir Unity projesinde, 1.14'e geçtikten sonra `/context`): Çekirdek 20.939 karakter, **8,2 bin token** tuttu (CLAUDE.md 2k, PROTOKOL 3,6k, DURUM 1,2k, HAFIZA 1,4k). Bu, yaklaşık 2,5 karakter başına 1 token demek. Aşağıdaki satırlar bu oranla tahmin edildi:

| Durum | Her oturumda yüklenen | Yaklaşık token |
|---|---|---|
| Yeni kurulmuş proje | ~12.200 karakter | ~4.900 |
| Unity projesi (+ Unity bölümü ve ajan tanımı) | ~15.000 karakter | ~6.000 |
| Sınırların sonuna kadar dolu bir proje | ~27.100 karakter | ~10.800 |

Türkçe ile İngilizce arasındaki fark ölçülmedi: bir projenin eski Türkçe çekirdeğini (28.600 karakter) ölçmekten 2 Ekim'de vazgeçildi, yeni çekirdek kullanımda daha iyi bulundu. Gerektiğinde okunan dosyalar (tahmin): plan şablonu ~0,8 bin, `BAKIM.md` ~1,4 bin, `KURULUM.md` ~2,8 bin token.

Kesin sayıyı görmek için projede Claude Code'u açıp `/context` yaz. Dosya bazında dökümü "Memory files" satırında görürsün.

Sınırlar protokolde tanımlı ve Claude bunları kendisi korur. Claude'u değil, her mesajda yeniden yüklenen dosyaları sınırlarlar: sınır olmadan dosyalar şişiyor (bir projede DURUM 7.500 karaktere çıkmıştı) ve uzun CLAUDE.md'de kurallar daha az uygulanıyor. Bir dosya sınırı aşarsa Claude onu kendisi toparlar (CLAUDE.md dahil):

| Dosya | Sınır |
|---|---|
| `CLAUDE.md` | en fazla 160 satır ve 10.000 karakter |
| `DURUM.md` | en fazla 30 satır ve 3.000 karakter; teknik borç `hafiza/teknik-borc.md`'ye gider |
| `HAFIZA.md` | en fazla 40 satır ve 3.500 karakter |
| Hafıza konu dosyası | yaklaşık 150 satırı ya da 15.000 karakteri geçerse bölünür |
| Plan | bağımsız parçaları varsa ya da yaklaşık 15.000 karakteri geçerse fazlara bölünür; adım tanımı en fazla 6 satır; aktif plan parça parça okunur |

---

## Neden bu tasarım?

- **Çekirdek `@` ile eklenir:** `@dosya` ile eklenen dosyalar her oturumun başında yüklenir. Başında `@` olmayan düz bir dosya yolu yüklenmez. Bu yüzden `@` sadece her zaman gereken dört küçük dosya için kullanılıyor, geri kalanlar düz yolla gösteriliyor ve gerektiğinde okunuyor.
- **CLAUDE.md sıkıştırmadan sonra yeniden okunur:** `/compact` sonrasında proje kökündeki CLAUDE.md diskten yeniden okunur. Durum her adımda diske yazıldığı için sıkıştırma ya da `/clear` iş kaybettirmez.
- **Şablonun adı `CLAUDE.sablon.md`:** Alt klasörlerde `CLAUDE.md` adında bir dosya olsaydı, Claude o klasördeki bir dosyayı okuduğunda o dosyayı da otomatik yüklerdi. Farklı ad bunu engelliyor.
- **Projeye özel kurallar `.claude/rules/` altında:** `paths:` alanı sayesinde yalnızca ilgili dosyalar okunduğunda yüklenirler ve her oturumda bağlamı doldurmazlar.
- **Hafıza repoda tutuluyor:** Claude'un yerleşik otomatik hafızası sadece o bilgisayarda durur ve git'e girmez. Repodaki hafıza ise başka bir bilgisayarda ve bulut oturumlarında da kullanılabilir. Bu yüzden 1.25'ten beri otomatik hafıza projelerde kapalı; kişisel tercihler ve düzeltmeler de `docs/ai/hafiza/` klasörüne yazılır.
- **Her adım ayrı commit:** Otomatik ilerlemede herhangi bir adıma kolayca geri dönmeyi sağlar.
- **Claude'un dosyaları İngilizce:** Kısa maddeler hızlı taranıyor ve İngilizcenin aynı bilgi için daha az token tutması bekleniyor; kazanç ölçülmedi (bir projede çekirdek, içerik taşınarak 28.600 karakterden 20.939'a indi). Eski projelerdeki Türkçe hafıza "şablonu güncelle" ile bir kerelik ve kayıpsız çevrilir: `docs/ai/araclar/kayip-kontrol.py` eski metindeki her komutun, yolun, sayının ve tarihin yeni metinde durduğunu denetler, orijinaller git geçmişinde kalır.
- **Kısaltırken bilgi kaybolmaz:** Hafıza toparlanırken ya da kısaltılırken `kayip-kontrol.py` iki şeye bakar: eski metindeki somut bilgiler (komut, yol, sayı, tarih, ad) yenisinde duruyor mu, ve hiçbir yeni satırda birlikte geçmeyen cümle parçaları var mı. İkincisi, satırın geri kalanı dururken düşen bir gerekçeyi, koşulu ya da istisnayı yakalar ("…yoksa referanslar bozulur" gibi). Claude listelenen her parçanın anlamının korunduğunu kontrol eder. El kitabı ipuçları da kısaltılırken "ne zaman okunur" işlerini korur; ortak satır, emin olunamayan girdinin başlığına bakılmasını söyler.
- **Sınırlar karakterle de:** Satır sınırı uzun satırlarla aşılabiliyordu (bir projede 28 satırlık DURUM 7.500 karakterdi). Karakter sınırı ve ayrı teknik borç dosyası bunu önler.
- **Kararları Claude verir:** Teknik ve tasarım seçimlerini, plana ne zaman başlanacağını ve kaç yardımcı ajan açılacağını kendisi seçer, gerekçesini tek satırla yazar. Yalnızca kapsam, para, geri dönüşü zor işlemler (git'in geri getiremeyeceği silmeler dahil) ve uydurulamayacak kimlik bilgileri sorulur; böylece soru-cevap turları ve kullanım hakkı azalır.
- **Kurallar varsayılan, sabit sayı yok:** Protokolün kuralları varsayılandır; uymadığı bir durumda Claude amaca en iyi hizmet edeni yapar ve nedenini söyler. Yalnızca geri dönüşü zor işlemlerden önce sorma kuralı sabittir. "3 adımda plan", "8 adımda sor", "3 denemede dur", "plan başına 2 ajan" gibi eşikler 1.33'te kalktı; yerlerinde kuralın amacı yazıyor, böylece Claude duruma göre karar verebiliyor.
- **Yardımcı ajanlar Claude'un kararı:** Paralel çok ajanlı sistemler en çok kullanım hakkı harcayanlar, bu yüzden Claude bir ajanı ancak kendi aramasından daha iyi iş çıkaracaksa açar: geniş keşif, bağımsız paralel işler, kapanış incelemesi. Aynı anda çalışmak toplam kullanımı artırmaz, sadece hızlandırır. Keşif CLAUDE.md yüklemeyen Explore ajanıyla yapılır.

---

## Sürüm

Bu depo, şablonun **1.50** sürümünün (16 Ekim 2026) herkese açık kopyasıdır. Sürüm numarası `docs/ai/PROTOKOL.md` dosyasının 2. satırında da yazar.

## Lisans

[MIT](LICENSE)
