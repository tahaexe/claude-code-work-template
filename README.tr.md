<div align="center">

# Claude Code Çalışma Şablonu

**Claude Code için plan öncelikli bir çalışma sistemi.**<br>
Claude işi planlar, her adımı doğrulayıp commit'ler ve hafızasını senin reponda tutar;<br>
böylece oturumlar ve bilgisayarlar arasında hiçbir şey kaybolmaz.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-work%20template-D97757?logo=claude&logoColor=white)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-1.51-2EA44F)](https://github.com/tahaexe/claude-code-work-template/tags)
[![Unity add-on](https://img.shields.io/badge/Unity%206-add--on-000000?logo=unity&logoColor=white)](#unity-eklentisi)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[English](README.md) · **Türkçe**

[Özellikler](#özellikler) · [Nasıl çalışır](#nasıl-çalışır) · [Başlarken](#başlarken) · [Günlük kullanım](#günlük-kullanım) · [Unity eklentisi](#unity-eklentisi) · [El kitabı](#el-kitabı) · [Yapılandırma](#yapılandırma)

</div>

---

## Özellikler

- **Plan öncelikli çalışma.** Küçük işler hemen yapılır. Büyük işler incelenir, plana bağlanır ve adım adım yürütülür; her adım doğrulanır, plana işlenir, commit'lenir ve push'lanır.
- **Hafıza repoda.** Kararlar, dersler ve güncel durum `docs/ai/` klasöründe durur ve git ile oturumlar, bilgisayarlar ve bulut oturumları arasında taşınır. `/clear` ve `/compact` iş kaybettirmez.
- **Az bağlam.** Her oturumda yalnızca küçük bir çekirdek yüklenir (yeni kurulmuş bir projede yaklaşık 5 bin token). Gerisi gerektiğinde okunur ve her dosyanın, Claude'un kendisinin koruduğu bir boyut sınırı vardır.
- **Sınırları belli özerklik.** Teknik kararları Claude verir ve gerekçesini tek satırla yazar. Yalnızca kapsam, para, geri dönüşü zor işlemler ve kimlik bilgileri için durup sorar.
- **Unity eklentisi.** Önce Unity CLI, penceresiz test çalıştırıcı, C# kod zekâsı, SOLID ve servis yapısına dayanan kod kuralları, oyun tasarım şablonları ve her arayüz adımından sonra görsel stil kontrolü.
- **Koşullu el kitabı.** Google Play, App Store, Firebase, ASO, shader'lar, Synty asset'leri ve daha fazlası üzerine sahada denenmiş notlar. Yalnızca işe yarayacağı projelere kurulur, diğerlerinde bağlam harcamaz.
- **Kendi profilinde tarayıcı işi.** Claude in Chrome ile Claude, Chrome'daki kendi profilinde çalışır (Play Console, App Store Connect, bir sayfayı kontrol etmek) ve senin profillerine dokunmaz.

## Nasıl çalışır

```text
İstek
 ├─ Küçük iş → yap → doğrula → commit + push
 └─ Büyük iş → keşfet → (soru) → plan yaz → başla
                 (yalnızca karar senin olduğunda ya da iş fazlıysa onayını bekler)
                                               ↓
    Her adım:  uygula → doğrula → plana işle → commit + push → sonraki adım
               (engel · karar · planda olmayan riskli işlem → durur ve sorar)
                                               ↓
    Kapanış:   özet + manuel testler + hafıza güncellemesi + arşiv
```

| Katman | Dosyalar | Ne zaman yüklenir |
|---|---|---|
| Çekirdek | `CLAUDE.md`, `PROTOKOL.md`, `DURUM.md`, `HAFIZA.md` | Her oturumda |
| Aktif iş | `planlar/<aktif plan>.md` | O plan üzerinde çalışılırken |
| Bilgi | `hafiza/*.md` | Konu gerektirdiğinde |
| Nadir | `sablonlar/`, `BAKIM.md`, `KURULUM.md` | Plan yazarken ya da kapatırken, kurulumda |
| Proje kuralları | `.claude/rules/*.md` | Yalnızca eşleşen dosyalar okunduğunda |

Claude'un kendi dosyaları, token tasarrufu için kısa İngilizce maddelerle yazılır. Claude seninle Türkçe konuşur; senin için yazdığı dosyalar da Türkçedir.

## Başlarken

### Gereksinimler

- [Claude Code](https://claude.com/claude-code) (masaüstü uygulaması ya da CLI) ve Git.
- Unity eklentisi için Unity Hub üzerinden Unity 6. Unity CLI, Unity'nin Claude eklentisi ve C# kod zekâsı eksikse Claude kurar (C# kod zekâsı .NET 10 SDK'sı gerektirir).

### Kurulum

1. Bu repoyu **klonla**, örneğin `C:\Users\<kullanıcı>\claude-code-work-template` klasörüne.
2. Aşağıdaki **global yönlendirmeyi** kendi klasörlerinle `~/.claude/CLAUDE.md` dosyasına ekle. Bu olmadan Claude kurulum isteğini tanımaz.

   ```markdown
   ## Claude çalışma şablonu
   Şablon klasörü: <ŞABLON>
   Unity projeleri klasörü: <UNITY_PROJELERİ> (yeni Unity projeleri burada oluşturulur)
   - Kullanıcı bir projeye bu çalışma sistemini kurmak isterse ("şablonu kur", "planlı çalışma sistemini kur" gibi): <ŞABLON>\docs\ai\KURULUM.md dosyasını oku ve "Kurulum" bölümünü uygula.
   - Şablonu güncellemek isterse ("şablonu güncelle"): aynı dosyanın "Güncelleme" bölümünü uygula.
   - Bir projede çok adımlı bir işe başlanırken projede docs/ai/PROTOKOL.md yoksa kurulumu tek cümleyle öner; istenmezse ısrar etme.
   ```
3. **Bir projeye kur.** Claude Code'u projenin klasöründe aç ve *"şablonu kur"* de. Claude proje türünü (Unity ya da diğer) anlar, dosyaları kopyalar; git'i, izin kurallarını ve `CLAUDE.md`'yi hazırlar, projeye özel kuralları yazar.
4. **Sonra güncelle.** Bu repoyu çek (pull), ardından projede *"şablonu güncelle"* de. Yalnızca sabit dosyalar yenilenir; planlar, hafıza ve `CLAUDE.md` korunur.

Adım adım kurulum, ipuçları ve sorun giderme [Kullanım Kılavuzu](KILAVUZ.md)'nda.

### Kurulumdan sonra proje yapısı

```text
proje/
├─ CLAUDE.md                 proje bilgisi, Claude doldurur
├─ .claude/rules/            projeye özel kurallar
├─ .claude/settings.json     izin kuralları (bağlam harcamaz)
└─ docs/ai/
   ├─ PROTOKOL.md            çalışma kuralları            (sabit)
   ├─ KURULUM.md             kurulum ve güncelleme        (sabit)
   ├─ BAKIM.md               kapanış ve temizlik          (sabit)
   ├─ sablonlar/             CLAUDE.sablon.md, plan.md    (sabit)
   ├─ araclar/               kayip-kontrol.py             (sabit)
   ├─ DURUM.md               neredeyiz
   ├─ HAFIZA.md              hafıza dizini
   ├─ manuel-testler.md      senin yapacağın testler
   ├─ hafiza/                kararlar, dersler, teknik borç, …
   └─ planlar/               tarihli planlar ve arşivleri
```

*Sabit* dosyalar şablondan gelir ve güncellemede yenilenir; geri kalan her şey projenin kendi verisidir.

## Günlük kullanım

Ezberlenecek komut yok, normal konuşman yeterli. Claude'un tepki verdiği birkaç ifade:

| Ne dersin | Ne olur |
|---|---|
| *"Envanter sistemi ekleyelim"* | Küçük iş doğrudan yapılır. Büyük iş için plan hazırlanır, gösterilir ve başlanır. |
| *"Önce planı göster"* | Plan senin onayını bekler. |
| *"Devam"* | Yarım kalan işi toparlar, kısa bir derleme kontrolü yapar ve sonraki adıma geçer. |
| *"Nerede kalmıştık?"* | `DURUM.md` ve aktif plandan bir iki satırlık durum özeti. |
| *"Bunu yapma, hep şöyle yap"* | Düzeltir ve dersi kaydeder; kalıcı kurallar `CLAUDE.md`'ye girer. |
| *"Bunu hatırla: …"* | Uygun hafıza dosyasına yazılır. |
| *"Hafıza bakımı"* | Tekrarları birleştirir, eskimiş bilgileri düzeltir. |

Plan bitince Claude özet verir, yeni manuel testleri `docs/ai/manuel-testler.md`'ye ekler ve doğrulanamayanları söyler. Yeni işe geçmeden `/clear` yaz; durum zaten diskte kayıtlı.

## Unity eklentisi

Kurulumda Unity seçilince şunlar eklenir:

| Eklenen | Nerede | Ne zaman yüklenir |
|---|---|---|
| Unity bölümü: skill'ler, Unity CLI, doğrulama, C# kod zekâsı | `CLAUDE.md` | Her oturumda |
| Yalnızca okuyan Unity uzmanı ajanı | `.claude/agents/unity-uzmani.md` | Çağrıldığında |
| Kod kuralları: varlıklar, oyun kodu, arayüz, test, shader | `.claude/rules/unity-*.md` | Eşleşen dosyalar okunduğunda |
| Kendi log dosyası, süre sınırı ve tek içe aktarma işçisiyle penceresiz test çalıştırıcı | `docs/ai/araclar/testler.sh` | Editör kapalıyken testlerde |
| C# kod zekâsı (`csharp-lsp` eklentisi, `csharp-ls` sunucusu) | `.claude/settings.local.json` | Her oturumda |
| Oyun tasarım şablonları: tasarım sütunlarıyla oyun özeti, GDD, görsel stil rehberi, prototip ve oyun testi raporları, post-mortem, yayın kontrol listesi | `docs/ai/sablonlar/oyun/` | Kullanıldığında |

- **Önce Unity CLI.** Editör, derleme ve build işleri Unity CLI ile yapılır; Unity MCP yalnızca CLI'ın yetmediği yerde. Eksik paketler (`com.unity.pipeline`, `com.unity.test-framework`) kurulumda eklenir.
- **Mimari.** SOLID ve tek bir başlangıç noktasında kurulan, arayüz arkasındaki servisler. Singleton ağırlıklı koda sessizce dokunulmaz, geçiş için plan adayı eklenir.
- **Görsel kimlik.** İlk arayüz işinden önce stil rehberi taslağı yazılır; görünen her değişiklikten sonra Claude ekran görüntüsünü rehberle karşılaştırır.
- **Arka planda çalışır.** Editör penceresiz açılır, build ve testler odağını çalmaz.
- **Mağaza yayını hazırlığı.** Claude mağaza sürümlerini ve `Builds/` altındaki build'leri hazırlar; yüklemek ve incelemeye göndermek sende kalır, imza şifreleri hiçbir yere yazılmaz.

## El kitabı

El kitabı (`el-kitabi/`), belirli teknolojiler, platformlar ve asset paketleri üzerine resmi belgelerden, makalelerden ve saha çalışmasından derlenmiş notları tutar. Her girdinin bir koşulu vardır: yalnızca koşulun tuttuğu projeye kurulur ve yalnızca ilgili işte okunur. Girdiler plan adayı ekleyebilir (örneğin Google Play Level Up yapısı); bir projede girdiye eklenen notlar güncellemede şablona önerilir.

<details>
<summary><b>21 girdinin tamamı</b></summary>

| Girdi | Ne zaman kurulur |
|---|---|
| Synty Sidekick: yüz ifadeleri ve göz kırpma | Projede Sidekick karakterleri var |
| Synty: gündüzü geceye çevirme | URP'li projede Synty ortam asset'leri var |
| Synty karakterlerine editörde poz verme | Projede Synty karakterleri var |
| Ortam sesi (2D) ve 3D konumsal ses | Unity projesi |
| Google Play'in önerdiği oyun yapısı (Level Up), R8 denetimi `r8-kontrol.py` ile | Hedefi Google Play olan Unity projesi |
| App Store: Game Center, uygulama içi etkinlikler, ilk gönderim | Hedefi App Store olan Unity projesi |
| Unity proje ayarları (6.3) ve git'te ikili `.asset` dosyaları | Unity projesi |
| Unity CLI saha notları ve penceresiz editör | Unity projesi |
| Unity'de oyuncu derlemesi: başsız komutlar, derleme belleği, mağaza derlemeleri, emülatörde denetim | Unity projesi |
| Shader derleme takılmaları: ölç, izle, ısındır | Unity 6 projesi |
| Tarayıcı bağlantısı: her Claude hesabına bir Chrome profili | Her proje |
| Layer Lab GUI Pro arayüz paketleri | Projede GUI Pro kullanılıyor |
| Firebase ile oyuncu hunisi, D1/D7 tutma ve Remote Config | Firebase SDK'sı olan mobil Unity projesi |
| Mağaza sayfası ve ASO | Google Play'de ya da App Store'da yayında |
| Mağaza etkinlikleri: Play tanıtım içeriği ve App Store uygulama içi etkinlikleri | Yayındaki oyun ya da uygulama |
| C# kod zekâsı, editörsüz derleme denetimi ve Unity dışında test | Unity ya da herhangi bir C# projesi |
| Adil zorluk ve başarısızlık | Unity oyunu |
| Hedef katmanları, güvenli bırakma noktaları ve sağlıklı liderlik tablosu | İlerlemesi, etkinlikleri ya da liderlik tablosu olan mobil oyun |
| Rakip ya da referans oyun incelemesi | Oyun projesi, yalnızca istenince |
| Renk körlüğüne dayanıklı palet (`cvd_palette.py` ile) | Renk eşleştirmeli oyun |
| Lansman haftasında kısa video (Shorts, TikTok, Reels) | Yayındaki ya da çıkışa hazırlanan oyun |
| Kısa video ölçümlerini okumak ve haftalık değerlendirme | Kısa video paylaşan proje |
| Steam mağaza sayfası, Next Fest, Playtest ve demo, erişilebilirlik etiketleri | Steam'e çıkacak oyun |
| Bulmaca ve casual oyunlarda ödüllü reklam: AdMob kuralları, yerleşim, ödül boyu | Ödüllü reklamı olan Unity oyunu |

</details>

Kaynak eklemek için Claude Code'u şablon klasöründe aç ve *"bu videoyu el kitabına ekle: &lt;link&gt;"* de. Adımlar ve analiz prompt'u [`el-kitabi/NASIL.md`](el-kitabi/NASIL.md) dosyasında.

## Yapılandırma

Kurulumun Claude Code'un kendi ayarlarına yazdıkları bağlam harcamaz.

<details>
<summary><b>Kurulumda uygulanan ayarlar</b></summary>

- **İzin kuralları** (`.claude/settings.json`): adım commit'leri ve push'lar onay beklemeden çalışır (zorla push yalnızca `--force-with-lease` ile); Unity doğrulama komutları ve Claude in Chrome araçları da öyle. Silme, diğer paket eklemeleri, build ve serbest C# bypass modu dışında yine izin ister.
- **Eklentiler:** superpowers projelerde kapalıdır, çünkü katı akışı protokolle çatışır; plugin-dev yalnızca şablon klasöründe açıktır. Oturum başına tahminen 1,9–3,2 bin token tasarruf sağlar.
- **Skill listesi:** agent-protocols ve engineering skill'leri yalnızca adıyla listelenir. `/batch` kapalıdır (her parça için ayrı worktree ve PR, tek dallı adım commit'lerine uymuyor); `/simplify` açık kalır.
- **İç içe ajan yok:** Kaç yardımcı ajan açılacağına Claude karar verir, ama bir yardımcı kendi ajanını açamaz.
- **Yerel otomatik hafıza kapalı** (`autoMemoryEnabled: false`): hafıza yalnızca `docs/ai/` ve git'te durur; bilgisayarda kalmış notlar bir kez projeye taşınır.
- **`.gitignore` ve `.gitattributes`:** editör ve bilgisayar dosyaları yok sayılır (gerekirse takipten çıkarılır), `.sh` dosyaları LF kalır ve Unity'nin ikili `.asset` dosyalarına `binary` satırları eklenir; böylece pişmiş veriler bilgisayarlar arasında bozulmaz.

</details>

<details>
<summary><b>Bağlam bütçesi</b></summary>

Bir Unity projesinde `/context` ile ölçüldü: çekirdek 20.939 karakter, **8,2 bin token** tuttu (token başına yaklaşık 2,5 karakter). Bu oranla tahminler:

| Durum | Her oturumda yüklenen | ≈ Token |
|---|---|---|
| Yeni kurulmuş proje | ~12.200 karakter | ~4.900 |
| Unity projesi (Unity bölümü ve ajan tanımı) | ~15.000 karakter | ~6.000 |
| Sınırlarına kadar dolu bir proje | ~27.600 karakter | ~11.000 |

| Dosya | Sınır |
|---|---|
| `CLAUDE.md` | 160 satır, 10.000 karakter |
| `DURUM.md` | 30 satır, 3.000 karakter (teknik borç kendi dosyasına gider) |
| `HAFIZA.md` | 40 satır, 4.000 karakter |
| Hafıza konu dosyası | ~150 satırı ya da 15.000 karakteri geçince bölünür |
| Plan | ~15.000 karakteri geçince fazlara bölünür; adımlar en fazla 6 satır; parça parça okunur |

</details>

<details>
<summary><b>Tasarım kararları</b></summary>

- **`@` yalnızca çekirdek için.** `@dosya` her oturumda yüklenir; düz yollar gerektiğinde okunur.
- **Durum her adımda diskte,** bu yüzden `/compact` ve `/clear` iş kaybettirmez; `CLAUDE.md` sıkıştırmadan sonra yeniden okunur.
- **Şablon dosyası `CLAUDE.md` değil `CLAUDE.sablon.md`,** böylece alt klasörlerden otomatik yüklenmez.
- **`.claude/rules/` altındaki kurallar** `paths:` sayesinde yalnızca eşleşen dosyalarda yüklenir.
- **Her adım ayrı commit,** böylece her adıma kolayca geri dönülür.
- **Kayıpsız kısaltma:** `kayip-kontrol.py`, hafıza kısaltılırken ya da çevrilirken komutların, yolların, sayıların, tarihlerin ve düşebilecek cümle parçalarının korunduğunu denetler.
- **Sabit eşik değil, varsayılan kural:** Claude kuralları duruma uyarlar ve nedenini söyler; yalnızca "geri dönüşü zor işlemlerden önce sor" kuralı sabittir.
- **Yardımcı ajan yalnızca değdiğinde:** geniş keşif, bağımsız paralel işler, kapanış incelemesi.

</details>

## Belgeler

| Belge | İçerik |
|---|---|
| [`KILAVUZ.md`](KILAVUZ.md) | Kullanım kılavuzu: kurulum, günlük kullanım, güncelleme, sorun giderme |
| [`docs/ai/PROTOKOL.md`](docs/ai/PROTOKOL.md) | Claude'un uyduğu çalışma protokolü |
| [`docs/ai/KURULUM.md`](docs/ai/KURULUM.md) | Kurulum ve güncelleme adımları |
| [`eklentiler/unity/KURULUM-UNITY.md`](eklentiler/unity/KURULUM-UNITY.md) | Unity eklentisinin kurulumu |
| [`el-kitabi/`](el-kitabi) | El kitabı girdileri |

## Teşekkür

Unity eklentisinin bazı kısımları *Claude-Code-Game-Studios*'tan (sürüm `7ed2c3e`, 2026-09-24) uyarlanmıştır.

## Lisans

[MIT](LICENSE) · Sürüm **1.51** · 2026-10-17
