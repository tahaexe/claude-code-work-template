# El kitabına girdi ekleme
<!-- Şablon klasöründe çalışırken okunur; projelere kopyalanmaz. -->

El kitabı, belirli bir teknoloji ya da asset paketiyle çalışırken Claude'un bilmesi gereken, dışarıdan (video, makale, belge) derlenmiş notlardır. Her girdi yalnızca **koşulu tutan** projelere kurulur ve orada yalnızca **ilgili işte** okunur.

## Adımlar
1. **Kaynağı al.**
   - **Video:** Claude in Chrome bağlıysa Claude, aşağıdaki prompt'u kullanıcının Chrome'undaki Gemini'de (gemini.google.com) izin almadan kendisi çalıştırır ve notu alır (Gemini videoyu izleyebilir, Claude izleyemez). Bağlı değilse kullanıcı Gemini'nin notunu yapıştırır ya da transkript kullanılır (YouTube → "Transkripti göster").
   - **Makale ya da belge:** Bağlantıyı oku.
   - **Projeden saha notu:** Bir projenin kendi kopyasına eklediği notlar (güncelleme korur ve önerir) → projedeki dosyayı şablondaki girdiyle karşılaştır, yeni ve düzeltilmiş notları birleştir; projeye özgü adları örnek olarak belirt, kaynağı `source` ve `added` alanlarına yaz.
2. **Gözden geçir** (girdiyi yazmadan önce):
   - Erişim doğrulaması tutuyor mu? Başlık, kanal ve süre gerçek videoyla uyuşmalı; uyuşmuyorsa not uydurma olabilir, kullanma.
   - 2-3 zaman damgasını kullanıcıya kontrol ettir.
   - "Videoda olmayan ek notlar"ı doğrula; yanlış ya da abartılı olanı düzelt veya sil.
   - Koşulu dar ve kontrol edilebilir yaz (klasör, paket ya da dosya adı). Geniş koşul girdiyi gereksiz projelere taşır.
   - En fazla ~150 satır; yalnızca uygulanabilir bilgi.
   - Tek başına değeri düşük parçaları (ör. videodaki örnek sahnenin tarifi) ayrı girdi yapma; işe yarayan kısmını ilgili girdiye birleştir. İçerik belirli bir pakete özgü değilse koşulu genel tut (ör. "Unity projesi").
   - İlgili resmi skill varsa (ör. `unity:optimize-audio`) girdiden ona yönlendir.
3. **Yaz:** `el-kitabi/<konu-adi>.md` (ASCII, küçük harf, tire). Girdiyi Claude okur: İngilizce, kısa maddeler halinde yaz; Türkçe bir notu çevirirken bilgi kaybetme. Künye alanları: `title`, `condition`, `read_when`, `requires` (yoksa `—`), `source`, `tech` (Unity ya da ilgili teknoloji ve sürüm), `added`. İsteğe bağlı `plan_candidates`: Girdi projede yapılması gereken somut bir iş tanımlıyorsa (ör. `google-play-level-up.md`), kurulunca DURUM'daki **Up next** listesine yazılacak plan adayları. Her madde tek satır olsun ve girdinin yolunu içersin.
4. **Kaydet:** README'deki el kitabı tablosuna satır ekle, şablon sürümünü artır, commit'le ve push'la.
5. **Projelere:** Projede "şablonu güncelle" denince koşulu tutan girdiler kurulur.

## Video analiz prompt'u (Gemini için)
Başındaki üç satırı doldur, gerisini olduğu gibi yapıştır.

```
Sen deneyimli bir Unity geliştiricisisin. Aşağıdaki videoyu baştan sona izle ve bir yapay zekâ kod asistanının (Claude Code) Unity projelerinde okuyup doğrudan uygulayabileceği bir "el kitabı notu" çıkar.

VİDEO: [video linki]
KONU: [ör. Synty karakterlerini Unity'de kullanmak]
PROJE BAĞLAMI: [ör. Unity 6, URP, mobil ve PC oyunlar]

ÖNCE ERİŞİMİ DOĞRULA: Videonun başlığını, kanalını ve süresini yaz. Videoya erişemiyorsan ya da içeriğini göremiyorsan bunu açıkça söyle ve dur. Tahminle not yazma.

KURALLAR
1. Sadece videoda gösterilen ya da söylenenleri yaz. Emin olmadığın her şeyi [emin değil] diye işaretle.
2. Her önemli adım ve ayar için zaman damgası ver (dk:sn).
3. Adları Unity arayüzündeki gibi, İngilizce ve tam olarak yaz: menü yolları, pencere, bileşen, özellik adları ve değerler.
4. Anlatım değil, uygulanabilir talimat yaz. Giriş, tanıtım ve reklam kısımlarını atla.
5. Videodaki Unity sürümünü ve render pipeline'ı belirt; tavsiye bunlara bağlıysa söyle.
6. Videoda olmayan bilgileri yalnızca en sondaki "Videoda olmayan ek notlar" bölümüne yaz.
7. Koşulu mümkün olduğunca dar ve kontrol edilebilir yaz: klasör, paket ya da dosya adıyla.
8. Notun tamamı en fazla 150 satır olsun, tekrar yapma. Notu İngilizce ve kısa maddeler halinde yaz; Unity terimleri arayüzdeki gibi kalsın.

ÇIKTIYI TAM OLARAK BU BİÇİMDE, TEK BİR MARKDOWN BELGESİ OLARAK VER:

---
title: [kısa başlık]
condition: [Bu not hangi projede geçerli? Klasör, paket ya da dosya adıyla.]
read_when: [Hangi işte okunmalı?]
requires: [Bu iş için gereken araç ya da paket ve nasıl kurulduğu; yoksa —]
source: [video başlığı] · [kanal] · [link] · [süre] · [yayın tarihi, biliniyorsa]
tech: [videodaki Unity sürümü ve render pipeline]
---
# [başlık]

## Summary
[2-3 cümle: Hangi sorunu çözüyor, sonunda ne elde ediliyor?]

## Know first: pitfalls
[Videoda uyarılan ya da gösterilen hatalar ve çözümleri, zaman damgasıyla.]

## Steps
[Numaralı, sırayla uygulanabilir adımlar; her adımda tam menü yolu ya da ayar ve zaman damgası.]

## Settings and values
| Setting | Value | Why | Time |
|---|---|---|---|

## Verification
[İşin doğru yapıldığı nasıl anlaşılır?]

## Can it be automated?
[Her adım için: kodla ya da komutla yapılabilir mi, yoksa editörde elle mi yapılmalı?]

## Unclear points
[Videoda net olmayan kısımlar, zaman damgasıyla.]

## Extra notes not in the video
[İsteğe bağlı; yalnızca önemli olduğundan ve doğruluğundan eminsen.]
```
