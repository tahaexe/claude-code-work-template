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
3. **Güncellemeler:** Sahip push'ladıkça GitHub Desktop'ta **Pull**, sonra projelerde `şablonu güncelle`. Yeni sürümü Claude zaten hatırlatır.
4. **Bilmesi gerekenler:** Claude Türkçe konuşur; çoğu plana onay beklemeden başlar; her commit otomatik push'lanır, gerekirse zorla push da yapar (`--force-with-lease`); tarayıcı işlerini izin almadan yapar; kurulum bazı eklentileri ekler (agent-protocols üçüncü taraf, kendi hook'u var). Şablon klasöründe Claude şablonu değiştirmez; şablon yalnızca sahibin bilgisayarında geliştirilir.

## 2. Bir projeye kurmak: `şablonu kur`

Claude Code'u projenin klasöründe aç ve `şablonu kur` yaz. Claude önce **ne projesi olduğunu** klasörden anlar; anlayamazsa sorar:

- **Unity + mevcut proje:** Genel kurulum, Unity eklentisi, eksik paketler (Pipeline, Test Framework), git ve izin kuralları kurulur. Unity ayarlarını doğru değerlerle karşılaştıran bir "ayar denetimi" plan adayı eklenir. Projeye uyan el kitabı girdileri eklenir. Kod singleton'lar ve dev yönetici sınıflarıyla yazılmışsa sıraya servis mimarisine geçiş planı eklenir; sen başlatana kadar kod değişmez. Görsel stil rehberi yoksa Claude ilk UI işinden önce taslağını yazar, sen düzeltirsin.
- **Unity + yeni oyun:** Beş soru sorar: ad, kısa fikir, 2D mi 3D mi, platform, gelir modeli. Projeyi Unity projeleri klasöründe, Unity ayarlarının platforma göre doğru değerleriyle oluşturur, oturumu yeni klasöre taşır ve kurulumu orada bitirir. Sonunda oyun özetini boş alanları kendi önerileriyle dolu olarak gösterir (sen düzeltirsin) ve ilk planı önerir; ilk plan servislerin kurulduğu başlangıç noktasıyla başlar. İlk UI işinden önce Claude görsel stil rehberinin taslağını yazar, sen düzeltirsin.
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
| Yeni bir iş | "Envanter sistemi ekleyelim" | Küçük işse doğrudan yapar; büyükse plan hazırlar, gösterir ve başlar. Plan senin kararını gerektiriyorsa (kapsam, para, geri dönüşü zor işlem) ya da fazlara bölünüyorsa onayını bekler. Plan sonuna kadar kendi ilerler; her adım doğrulanır, plana işlenir, commit'lenir ve push'lanır |
| Planı önce görmek | "önce planı göster" | Plana başlamadan onayını bekler |
| Bekleyen planı onaylamak | "tamam", "olur" | Plan başlar |
| Devam etmek | "devam", "kaldığımız yerden" | Önce yarım kalan işi toparlar ve kısa bir derleme kontrolü yapar, sonra sıradaki adıma geçer |
| Durumu görmek | "nerede kalmıştık?" | Kısa durum özeti verir |
| Planı görmek | "planı göster", "tüm planlar" | ✓ → ○ işaretli liste |
| Planı değiştirmek | "4. adımdan sonra şunu ekle", "şunu çıkar", "şunu sıraya koy" | Plan güncellenir ve commit'lenir |
| Hızı ayarlamak | "yavaş gidelim" / "sen devam et" | Her adımda durur / otomatik ilerler |
| Düzeltmek | "bunu yapma, hep şöyle yap" | Düzeltir, dersi hafızaya yazar; kalıcı bir kuralsa CLAUDE.md'ye ekler ve söyler |
| Bir şey hatırlatmak | "bilgin olsun: …", "bunu hatırla: …" | Uygun hafıza dosyasına yazar |
| Hafızayı toparlamak | "hafıza bakımı" | Tekrarları birleştirir, eskimiş bilgileri düzeltir |
| Tarayıcıda bir iş | "Play Console'da ürünleri oluştur", "şu sayfaya bak" | Chrome'daki kendi profilinde izin almadan kendisi yapar (Claude in Chrome); yalnızca Claude'un kendi güvenlik onayları kalır |
| Sürüm çıkmak | "8.3 sürümünü hazırla", "sürüm çıkalım" | Mağazalarda yeni sürümü doğrudan yayın olarak oluşturur (Play'de üretim kanalı ve %100, App Store'da otomatik yayın; test kanalı ve TestFlight yok) ve verilerini girer, Android ve iOS build'lerini `Builds/` klasörüne alır, sonra bekler. Build'leri mağazalara sen yükler, incelemeye sen gönderirsin; Android imzası için keystore şifresini açık editöre sen girersin |

Claude seçtiği yolu tek satırla söyler (ör. "→ Plan hazırlıyorum"); istersen hemen yönünü değiştirirsin.

**Otomatik ilerleme yalnızca şu durumlarda durur:** doğrulama geçmiyor ve denemeye değer fikir kalmamışsa, planın bir varsayımı yanlış çıkarsa, bir test hatalı görünüp plan onu değiştirmeyi içermiyorsa, planda olmayan ve geri dönüşü zor bir işlem (git'in geri getiremeyeceği silme, paket yükseltme ya da kaldırma, veri taşıma) gerekirse ya da senin kararın gerekirse.

**Plan bitince:** Claude özet verir, yeni manuel testleri `docs/ai/manuel-testler.md`'ye ekler ve çalıştırılamadığı için "değerlendirilmedi" kalan kontrolleri söyler. Manuel testleri istediğin zaman topluca yaparsın ("test oturumu yapalım" demen yeter). Yeni işe geçmeden `/clear` yaz; durum dosyalarda kayıtlı olduğu için hiçbir şey kaybolmaz.

**Claude karar verir:** Teknik ve tasarım seçimlerini, plana ne zaman başlayacağını ve kaç yardımcı ajan açacağını kendisi seçer, gerekçesini tek satırla yazar. Kurallar varsayılandır: uymadığı bir durumda Claude amaca en iyi hizmet edeni yapar ve nedenini söyler. Sana yalnızca kapsam, para, geri dönüşü zor işlemler ve senin vermen gereken kimlik bilgileri için sorar. Plan sürerken büyük bir iş verirsen hangisinin önce yapılacağına da kendisi karar verir ve söyler.

**Push otomatik.** Projenin uzak deposu varsa Claude her commit'ten sonra push'lar. Uzak depo ilerideyse (ör. başka bilgisayarda çalıştıysan) önce çekip birleştirir; çakışmayı iki tarafın amacı açıksa kendisi çözer, değilse sana sorar. Geçmişi yeniden yazmak gerekirse zorla push yapabilir; `--force-with-lease` kullandığı için başka bilgisayardan gelen commit'leri silmez.

**İsteğe bağlı kısa komutlar:** `plan: <iş>` · `devam` · `durum` · `planı göster` · `tüm planlar` · `adım adım` · `bunu hatırla: …` · `hafıza bakımı` · `şablonu kur` · `şablonu güncelle`

## 4. Güncellemek: `şablonu güncelle`

1. Önce GitHub Desktop'ta şablon deposu için **Fetch origin** ve **Pull** yap; şablonun yeni sürümü böyle gelir.
2. Projenin klasöründe `şablonu güncelle` yaz.

Yeni sürüm çıktığında Claude bunu projede oturumun ilk cevabında tek satırla hatırlatır. Her sürümden sonra güncellemen gerekmez; güncelleme birikimlidir, aradaki tüm sürümler tek seferde gelir.

- **Yenilenenler:** Çalışma kuralları (PROTOKOL, KURULUM, BAKIM), şablonlar, izin kuralları ve ayarlar, `.gitignore`'daki editör ve bilgisayar satırları, `.gitattributes`'taki `.sh` satır sonu kuralı (Unity'de ikili `.asset` dosyalarını koruyan satırlar da), Unity eklentisi, projeye uyan el kitabı girdileri. Git'te takip edilen editör dosyaları (`.vscode` gibi) takipten çıkarılır: dosyalar bilgisayarında kalır, diğer bilgisayarda bir sonraki pull'da silinir ve editör onları yeniden oluşturur.
- **Korunanlar:** Planlar, hafıza, `DURUM.md` ve projenin CLAUDE.md dosyası. CLAUDE.md'de yapısal bir değişiklik gerekiyorsa Claude yapar ve söyler. İstisnalar: El kitabı girdilerinin hafıza satırı ve plan adayları eklenir ya da güncellenir (ör. mevcut Android oyunlarında Google Play Level Up); bilgisayarda kalmış yerel notlar da hafızaya eklenir (aşağıda).
- **Bir kerelik dil geçişi (1.14):** 1.14'ten eski projelerde Claude önce sana sorar, sonra kendi okuduğu Türkçe dosyaları (CLAUDE.md, DURUM, HAFIZA, hafıza dosyaları, proje kuralları, bekleyen planlar) kısa İngilizceye çevirir. Bilgi kaybolmaz: her dosya ayrı commit'lenir, bir betik eski metindeki komut, yol, sayı ve tarihlerin yenisinde durduğunu denetler, orijinaller git geçmişinde kalır. Arşivdeki planlar, manuel testler ve tasarım belgeleri Türkçe kalır.
- **Bir kerelik hafıza taşıma (1.25):** Claude'un o bilgisayarda tuttuğu yerel notlar varsa projenin `docs/ai/hafiza/` klasörüne taşınır, commit'lenir ve yerel klasör silinir; yerel hafıza artık kapalıdır. Projeyi başka bir bilgisayarda da kullandıysan orada da bir kez `şablonu güncelle` de, oradaki notlar da taşınsın.
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
| Sohbet çok uzadı | Plan bitince `/clear` yaz; durum dosyalarda kayıtlı |
| Kurulumda `‹?›` işaretli yerler var | Claude emin olamadığı komut ve kuralları işaretler; netleştir, o da düzeltir |
| Hafıza ya da plan dosyasını okumak istiyorum (İngilizce) | Claude'a "şunu Türkçe özetle" de |
| Bir projede superpowers'ı kullanmak istiyorum | Şablon onu projelerde kapatır. O projede `.claude/settings.local.json` dosyasına `"enabledPlugins": {"superpowers@claude-plugins-official": true}` yaz; yalnızca senin bilgisayarında açılır |
| Unity testleri takılıyor | Testler derleme bitmeden başlatılmaz. Editör açıkken Pipeline'ın test komutu kullanılır; o yoksa editör kapatılır ve testler projedeki `docs/ai/araclar/testler.sh` ile koşar: projenin kendi Unity sürümü, kendi log dosyası, en çok 30 dakika. `unity test` kullanılmaz: log seçeneği yok, senin açık editörünün de kullandığı ortak `Editor.log`'a yazıyor. Test Framework paketi yoksa testler hiç çalışmaz. Bellek az harcansın diye editör tek içe aktarma işçisiyle açılır; ilk açılış (boş `Library/`) ya da büyük bir içe aktarma yavaş kalırsa Claude işçi sayısını `IMPORT_WORKERS` ile artırır |
| agent-protocols ya da engineering skill'leri görünmüyor | Masaüstü uygulaması eklentileri claude.ai hesabına göre getiriyor; diğer hesapta eksik olabilir. "şablonu güncelle" eksikleri kullanıcı düzeyinde kurar, unity-perf'i kaldırır. Sonra yeni oturum aç |
| Claude "tarayıcıda açtım" diyor ama bir şey göremiyorum, ya da Chrome bağlantısı hata veriyor | Claude sırayla kendisi dener: kendi profilinin penceresini öne getirir ve hangi pencerede olduğunu söyler; bu bilgisayardaki tarayıcıya mı bağlı diye bakar (aynı hesap öbür bilgisayarda da bağlı olabilir); bağlantıyı yeniden kurar; kendi profilini kapatıp açar. Eklentide giriş düşmüşse girişi sen yaparsın. Chrome'u tamamen kapatıp açmak senin pencerelerini de kapatır; bunu yalnızca sen yaparsın |

## 8. İpuçları

- **Claude'un dosyaları İngilizce, konuşma Türkçe.** Protokol, durum, hafıza, planlar ve kurallar daha az token harcasın diye kısa İngilizce maddelerle yazılır. Manuel testler ve tasarım belgeleri Türkçe kalır.
- **Plan modu (Shift+Tab) ile de çalışır.** Onaylanan plan şablonla `docs/ai/planlar/` altına kaydedilir.
- **Dosyaları elle de düzenleyebilirsin.** Claude bir sonraki okumada değişikliğini görür.
- **`docs/ai/` git'e dahil olmalı** ki hafıza da versiyonlansın ve bilgisayarlar arasında taşınsın; Claude bilgisayarda ayrı bir hafıza tutmaz. Proje GitHub Pages'i `docs/` klasöründen yayınlıyorsa bu klasör de yayınlanır; Pages'in kaynak klasörünü değiştir ya da `_config.yml` içine `exclude: [ai]` ekle.
- **Paralel oturum (worktree) kullanıyorsan** her branch kendi `DURUM.md`'sini taşır; birleştirirken bu dosyada çakışma çıkarsa güncel olanı tut.
