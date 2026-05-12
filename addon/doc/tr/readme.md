# NVDA.ES Eklenti Mağazası

> **⚠️ Beta sürümü test kullanıcıları için önemli uyarı:**
> Eğer **TiendaNVDA_Modern** eklentisini test ediyorsanız, lütfen **bu sürümü kurmadan önce kaldırın**. O sürüm bir test ve beta sürümüydü; bu nihai sürümle birlikte bulunmamalıdır. Kaldırmak için NVDA menüsü → Araçlar → Eklenti Mağazası yoluna gidin, "TiendaNVDA_Modern" seçeneğini bulun ve silin. NVDA’yı yeniden başlatın, ardından bu yeni sürümü kurun.

NVDA için Birleşik Eklenti Mağazası: **İspanyolca Konuşan Topluluk Mağazası (NVDA.ES)** ile **NV Access Resmî Mağazası**nı tek bir erişilebilir arayüzde birleştirir.

**Yazar:** Héctor J. Benítez Corredera
**Lisans:** GNU General Public License v2
**Sürüm:** 2026.05.09
**Uyumluluk:** NVDA 2025.1 – NVDA 2026.1
**Depo:** [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA)

---

## İçindekiler

1. Giriş
2. Kurulum
3. İlk adımlar
4. Üç mağaza
5. Mağaza arayüzü
6. Durum göstergeleri
7. Kısayol tuşları ve özel işlevler
8. Bağlam menüsü
9. Kurulu eklentilerin yönetimi
10. Eklenti paketleyici
11. Güncelleme arama
12. Seçenekler paneli
13. Önbellek sistemi
14. Çevrimdışı mod
15. Yedekleme ve geri yükleme
16. Açıklama çevirisi
17. Özel sunucular
18. Notlar ve korumalar
19. Kısayol özeti
20. Değişiklik günlüğü

---

## Giriş

**NVDA Eklenti Mağazası**, eski NVDA.ES Mağazası’nın tamamen yeniden tasarlanmış bir devamıdır. Daha modern, hızlı ve birleşik bir deneyim sunmak için sıfırdan geliştirilmiştir.

### Önceki sürüme göre yenilikler

* **Birleşik Mağaza:** NVDA.ES ve NV Access resmî mağazasındaki eklentileri tek pencereden inceleyebilirsiniz.
* **Durum göstergeleri:** Her eklenti gerçek zamanlı durum bilgisi gösterir: kurulu, güncellenebilir, devre dışı, uyumsuz vb.
* **Yerel yönetim:** Mağazadan çıkmadan eklentileri etkinleştirme, devre dışı bırakma veya kaldırma.
* **Çok katmanlı önbellek:** Sunucu, çeviri ve liste önbelleği ile çok hızlı yükleme.
* **Çevrimdışı mod:** İnternet olmadan önbelleğe alınmış verilerle mağazada dolaşma.
* **Yedekleme ve geri yükleme:** Eklentilerinizi yedekleyip başka bilgisayara aktarabilirsiniz.
* **Paketleyici:** Kurulu eklentilerden `.nvda-addon` dosyası oluşturur.
* **Sessiz kurulum:** Arka planda ara iletişim kutuları olmadan kurulum yapar.
* **Akıllı yeniden başlatma:** Gerçekten bir şey kurulmuşsa yeniden başlatma ister.
* **Bağımlılık kontrolü:** Kurulum öncesi gerekli bağımlılıkları denetler.
* **Önbellekli çeviri:** F3 ile açıklamalar anında çevrilir ve tekrar sorgulanmaz.
* **Geliştirilmiş bildirimler:** Güncelleme bildirimleri artık kaynağı (NVDA.ES veya Resmî) ve eklenti adlarını belirtir.

---

## Kurulum

1. `.nvda-addon` dosyasını depo içindeki Releases sayfasından indirin.
2. İndirilen dosyayı açın veya NVDA penceresine sürükleyin.
3. NVDA kurulum onayı istediğinde kabul edin.
4. Eklentiyi etkinleştirmek için NVDA’yı yeniden başlatın.

---

## İlk adımlar

Eklenti **atanmış klavye kısayolları olmadan gelir**. Kendi kısayollarınızı şu yoldan atayabilirsiniz:

**NVDA Menüsü → Tercihler → Girdi Hareketleri → NVDA Eklenti Mağazası**

Burada şu eylemler bulunur:

* NVDA.ES eklentilerini göster
* NVDA.ES kurulu eklentileri için güncelleme ara
* Resmî mağaza eklentilerini göster
* Resmî mağaza güncellemelerini ara
* Tüm kaynakları içeren birleşik mağazayı göster

### Menüden erişim

Şu yoldan da erişebilirsiniz:

**NVDA Menüsü → Araçlar → NVDA.ES Eklenti Mağazası**

Alt menüler:

* **NVDA.ES Mağazası:** İspanyolca topluluk eklentileri ve güncelleme arama
* **Resmî NVDA Mağazası:** Resmî mağaza eklentileri ve güncellemeleri
* **Birleşik Mağaza (Tüm kaynaklar):** Tüm eklentileri tek listede gösterir
* **Eklenti Paketleyici:** Kurulu eklentileri `.nvda-addon` olarak paketler
* **Yardım:** Bu belgeyi varsayılan tarayıcıda açar

---

## Üç mağaza

Yeni sürüm üç görünüm modu içerir:

### NVDA.ES Eklenti Mağazası

İspanyolca konuşan topluluğun mağazasıdır. Eklentileri `https://nvda.es` ve eklediğiniz özel sunuculardan alır.

### Resmî NVDA EklentiMağazası

NV Access’in resmî eklenti mağazasına erişir. Eklentiler API üzerinden alınır ve uyumluluk bilgileriyle gösterilir.

### Birleşik Mağaza

Tüm kaynaklardaki eklentileri tek listede gösterir. Kaynaklar:

* `[ES]` = İspanyolca topluluk
* `[OF]` = Resmî mağaza

---

## Mağaza arayüzü

Mağaza iki panelden oluşur.

### Sol panel

1. **Arama kutusu:** Açılışta odak buradadır. Arama yazıp Enter ile filtreleme yapılır.
2. **Eklenti listesi:** Durum göstergeleriyle tüm eklentiler görünür.
3. **Eylem düğmesi (Kur/Güncelle):**

   * Kurulu değilse: **Kur**
   * Güncelleme varsa: **Güncelle**

### Sağ panel

Seçili eklenti bilgileri:

* Ad ve özet
* Sunucudaki sürüm
* Kurulu sürüm
* Yazar
* Tam açıklama
* NVDA uyumluluğu
* İndirme sayısı
* Kurulum durumu

---

## Durum göstergeleri

| Gösterge | Anlamı                     |
| -------- | -------------------------- |
| `[I]`    | Kurulu                     |
| `[U]`    | Güncelleme mevcut          |
| `[U-I]`  | Uyumsuz güncelleme         |
| `[D]`    | Devre dışı                 |
| `[R]`    | Kaldırılmak üzere işaretli |
| `[I-I]`  | Kurulu ama uyumsuz         |
| `[X]`    | Uyumlu değil               |

Birleşik mağazada ayrıca:

| Etiket | Kaynak                   |
| ------ | ------------------------ |
| `[ES]` | NVDA.ES sunucuları       |
| `[OF]` | NV Access resmî mağazası |

---

## Kısayollar ve özel işlevler

### F1 — Geçerli konum

Bulunduğunuz listedeki sırayı söyler.
Örnek: “200 eklentiden 15. eklentidesiniz.”

### Ctrl+F1 — Durum açıklaması

Durum göstergesinin anlamını açıklar.

### F2 — Tam bilgiyi oku

Sağ panele geçmeden tüm teknik bilgi ve açıklamayı okur.

### F3 — Açıklamayı çevir

Açıklamayı ayarlanan dile çevirir.

> **Not:** F3 için çeviri özelliği etkin olmalı ve internet bağlantısı gerekir.

---

## Bağlam menüsü

**Uygulama tuşu** veya **Shift+F10** ile açılır.

### Filtreler

* Tüm eklentileri göster
* API uyumluluğuna göre filtrele
* Yazara göre sırala
* İndirme sayısına göre sırala

### Panoya kopyala

* Bilgileri kopyala
* Web bağlantısını kopyala
* İndirme bağlantısını kopyala

---

## Kurulu eklenti yönetimi

Kurulu bir eklenti için:

1. `[I]`, `[D]` veya `[U]` işaretli eklentiyi seçin.
2. Uygulamalar tuşuna basın.
3. **Kurulu yönetimi** alt menüsünü açın.

Seçenekler:

* Etkinleştir / Devre dışı bırak
* Kaldır
* Belgeleri görüntüle

---

## Eklenti paketleyici

Kurulu eklentilerden `.nvda-addon` oluşturur.

Kullanım:

1. **NVDA Menüsü → Araçlar → NVDA Eklenti Mağazası → Eklenti Paketleyici**
2. Eklenti seçin
3. Kayıt klasörü seçin
4. Dosya şu biçimde oluşturulur:
   `ad_sürüm_Gen.nvda-addon`

---

## Güncelleme arama

### Elle arama

Araçlar menüsünden yapılır.

Bu pencerede:

* Boşluk: seç / kaldır
* Alt+S: tümünü seç
* Alt+D: tümünü kaldır
* Alt+A: güncellemeyi başlat
* Alt+K / Escape / Alt+F4: kapat

### Otomatik kontrol

Etkinleştirildiğinde:

* Arka planda güncelleme arar
* Bildirim gösterir
* Gereksiz sunucu yükünü önlemek için otomatik durur

Örnek bildirim:

```text
3 güncelleme bulundu.
- NVDA.ES (2): Eklenti A, Eklenti B
- Resmî Mağaza (1): Eklenti C

Eklenti güncellemelerini ara komutunu çalıştırın.
```

---

## Seçenekler paneli

Erişim:

**NVDA Menüsü → Tercihler → Ayarlar → NVDA.ES Eklenti Mağazası**

Bölümler:

* NVDA.ES
* Resmî mağaza
* Güncellemeler
* Çeviri
* Genel seçenekler
* Yedekleme ve geri yükleme

Örnek seçenekler:

* Sunucu seçimi
* Resmî mağazayı etkinleştir
* Uyumsuz eklentilere izin ver
* Güncellemeleri Otomatik Denetle
* Çeviri dili
* Sessiz kurulum
* Sunucu önbelleği
* Çevrimdışı mod
* Yedek oluştur / geri yükle

---

## Önbellek sistemi

Üç katman:

### Sunucu önbelleği

Eklenti listelerini diskte saklar.

### Çeviri önbelleği

F3 çevirilerini JSON dosyasında tutar.

### Bellek önbelleği

Sık sorguları RAM’de tutar.

---

## Çevrimdışı mod

İnternet olmadan mağazada dolaşabilme imkanı sağlar.

Gerekenler:

1. Sunucu önbelleği açık olmalı
2. Çevrimdışı mod açık olmalı
3. Daha önce çevrimiçi kullanım yapılmış olmalı

> Çevrimdışı modda kurulum ve indirme yapılamaz.

---

## Yedekleme ve geri yükleme

### Yedek oluştur

Kurulu eklenti listesini JSON olarak kaydeder.

### Yedekten geri yükleme

JSON dosyasını yükleyip eklentileri toplu kurar.

---

## Açıklama çevirisi

Google Translate tabanlıdır.

Adımlar:

1. Çeviriyi etkinleştir
2. Hedef dil seç
3. Listede F3 bas

Özellikler:

* Başlangıç/bitiş sesleri
* Önbellekleme
* İnternet gerektirir

---

## Özel sunucular

Üçüncü taraf eklenti depoları eklenebilir.

### Sunucu ekleme

1. Sunucu yönetimine gir
2. **Ekle**
3. Ad ve URL gir
4. Kaydet

Örnek:

* **Ad:** Rus Topluluğu
* **URL:** `https://nvda-addons.ru/get.php?addonslist`

---

## Notlar ve korumalar

Koruma özellikleri:

1. Kaldırılacak eklentiler güncelleme kontrolünden hariç tutulur
2. API uyumluluğu doğrulanır
3. Kurulum hataları bildirilir
4. Yeniden başlatmadan sonra ek kontrol engeli
5. Yeniden başlatma hatırlatmaları
6. İnternet yoksa sesli uyarı
7. Akıllı yeniden başlatma
8. Bağımlılık kontrolü

---

## Kısayol özeti

### Ana pencere

| İşlem           | Tuş                     |
| --------------- | ----------------------- |
| Arama kutusu    | Alt+A                   |
| Eklenti listesi | Alt+L                   |
| Yükle / Güncelle  | Alt+Y                   |
| Bilgi paneli    | Alt+i                   |
| Web sayfası     | Alt+W                   |
| Sunucu değiştir | Alt+Ğ                   |
| Kapat           | Alt+K / Escape / Alt+F4 |

### Eklenti listesi

| İşlem            | Tuş                     |
| ---------------- | ----------------------- |
| Konum bilgisi    | F1                      |
| Durum açıklaması | Ctrl+F1                 |
| Tam bilgi oku    | F2                      |
| Çeviri           | F3                      |
| Bağlam menüsü    | Uygulama tuşu / Shift+F10 |

### Güncelleme penceresi

| İşlem               | Tuş                     |
| ------------------- | ----------------------- |
| Tümünü seç          | Alt+S                   |
| Tümünü kaldır       | Alt+R                   |
| Güncellemeyi başlat | Alt+G                   |
| Kapat               | Alt+K / Escape / Alt+F4 |

---

## Değişiklik günlüğü

### Sürüm 2026.05.11

* Rusça dil desteği eklendi. (Valentín N. Kupriyanov)

### Sürüm 2026.05.10

* Türkçe dil desteği eklendi. (Umut KORKMAZ)

### Sürüm 2026.05.09

* NVDA için Birleşik Eklenti Mağazası’nın ilk sürümü
* NVDA.ES + Resmî mağaza entegrasyonu
* Yeni durum göstergeleri
* Yerel eklenti yönetimi
* Çok katmanlı önbellek
* Çevrimdışı mod
* Yedekleme / geri yükleme
* Paketleyici
* Sessiz kurulum
* Akıllı yeniden başlatma
* Çeviri önbelleği
* Özel sunucu desteği
* Ayrıntılı bildirimler

### Önceki sürümler

Eski **NVDA.ES Mağazası** sürümleri (0.1–0.10), bu depoda commit geçmişi üzerinden incelenebilir.

GitHub geçmişine giderek eski commit’leri görüntüleyebilirsiniz.

---

**NVDA Eklenti Mağazası’nın keyfini çıkarın!**

**Sevgiyle:** Héctor J. Benítez Corredera.
