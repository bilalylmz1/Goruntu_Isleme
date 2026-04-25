# 🖼️ Görüntü İşleme Tabanlı Belge Tarayıcı ve İyileştirme Sistemi

> **Görüntü İşleme Dersi — Proje Ara Raporu**
> Abdurrahman Karadağ · Hayri Talha Özkan · Umut Can · Bilal Yılmaz

---

## 📌 Proje Özeti

Bu proje, temel görüntü işleme algoritmalarını **hazır kütüphane fonksiyonları kullanmadan**, tamamen **matris/piksel düzeyinde** sıfırdan geliştirerek uygulamayı hedeflemektedir. Kullanıcının kamera veya telefonuyla çektiği belge/doküman fotoğrafları üzerinde çeşitli görüntü işleme adımları uygulanarak okunabilir, temiz ve düzgün bir çıktı üretilmesi amaçlanmaktadır.

---

## 🎯 Temel Yaklaşım

- **Matris düzeyinde programlama:** Tüm algoritmalar NumPy dizileri, döngüler ve matematiksel formüller ile sıfırdan kodlanmaktadır. OpenCV, Pillow vb. kütüphanelerin hazır işleme fonksiyonları **kesinlikle kullanılmayacaktır**.
- **Basit arayüz:** Algoritmalar, sade bir Python arayüzü (Tkinter veya benzeri) ile kullanıcıya sunulacaktır.
- **Anlamadan kod yazmama:** Her algoritmanın matematiği ve mantığı önce ekip tarafından kavranmakta, ardından kodlanmaktadır.

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|-----------|---------------|
| **Python** | Ana programlama dili |
| **NumPy** | Matris/dizi temsili ve piksel düzeyinde matematiksel işlemler |
| **OpenCV** | *Yalnızca* görüntü okuma (`imread`), yazma (`imwrite`) ve gösterme (`imshow`) — işleme fonksiyonları kullanılmıyor |
| **Matplotlib** | Histogram görselleştirme, işlem öncesi/sonrası karşılaştırmalar |

---

## 🔬 Uygulanacak Algoritmalar

Aşağıdaki tüm algoritmalar **hazır fonksiyon çağrısı olmadan, formül ve matris işlemleriyle** gerçekleştirilecektir:

### Temel Dönüşümler
- **Gri Dönüşüm** — Ağırlıklı ortalama: `0.299·R + 0.587·G + 0.114·B`
- **Binary Dönüşüm** — Tek eşikleme yöntemi
- **Görüntü Döndürme** — En yakın komşu interpolasyonu
- **Görüntü Kırpma**
- **Yakınlaştırma / Uzaklaştırma** — En yakın komşu interpolasyonu ile ölçekleme
- **Renk Uzayı Dönüşümleri**

### Histogram İşlemleri
- **Histogram Analizi** — Giriş görüntüsüne ait histogram hesabı
- **Histogram Germe / Genişletme** — Min-max normalizasyonu

### Kontrast & Filtre İşlemleri
- **Kontrast Artırma**
- **Konvolüsyon İşlemi** — 3×3 ortalama (mean) çekirdeği
- **Unsharp Maskeleme Filtresi** — Görüntü keskinleştirme

### Gürültü İşlemleri
- **Tuz-Biber (Salt & Pepper) Gürültü Ekleme** — Sentetik gürültü üretimi
- **Ortalama (Mean) Filtre** — Gürültü temizleme
- **Medyan (Median) Filtre** — Gürültü temizleme

### Kenar & Morfolojik İşlemler
- **Kenar Bulma** — Prewitt operatörü
- **Eşikleme** — Tek eşikleme
- **İki Görüntü Arasında Aritmetik İşlemler** — Toplama, bölme
- **Morfolojik İşlemler (Temel)** — Genişleme (Dilation), Aşınma (Erosion)
- **Morfolojik İşlemler (Bileşik)** — Açma (Opening), Kapama (Closing)

---

## 🔄 Uygulama Çalışma Prensibi

```
1. Görüntü Yükleme    → cv2.imread ile belge fotoğrafı alınır
2. Ön İnceleme        → Boyut, kanal sayısı, piksel aralığı incelenir
3. İşleme Adımları    → Seçilen algoritmalar matris düzeyinde uygulanır
4. Görselleştirme     → Matplotlib ile öncesi/sonrası karşılaştırılır
5. Çıktı              → Temiz, okunabilir belge görüntüsü elde edilir
```

---

## 📅 Proje Takvimi

| Tarih | Hedef |
|-------|-------|
| 25 Nisan 2026 | Başlangıç toplantısı — ön yüz planlaması |
| 2 Mayıs 2026 | Ara kontrol |
| 3 Mayıs 2026 | Kalan ön yüz + algoritmaların bir kısmı tamamlanır |
| 9–10 Mayıs 2026 | Tüm algoritmaların tamamlanması ve son testler |

---

## 📚 Referanslar

1. R. C. Gonzalez & R. E. Woods — *Digital Image Processing*
2. W. Burger & M. J. Burge — *Digital Image Processing: An Algorithmic Introduction*
3. Kamboj & Gupta — Sobel, Prewitt, Roberts ve Canny kenar bulma karşılaştırması
4. Kaur & Kaur — Histogram tabanlı kontrast iyileştirme teknikleri
5. Jayaraman vd. — Morfolojik işlemlerin gürültü ve şekil düzeltmedeki etkisi
6. Davies — Unsharp maskeleme ile görüntü keskinleştirme
7. Pitas — Tuz-biber gürültüsü ve filtre performansları
