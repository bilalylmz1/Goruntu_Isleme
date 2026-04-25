# 🖼️ Görüntü İşleme Tekniklerini Görselleştirme


---

## 📌 Proje Özeti

Bu proje, görüntü işlemenin **15 farklı temel konusunu** etkileşimli bir arayüz aracılığıyla kullanıcıya sunan bir uygulama geliştirmeyi hedeflemektedir.

Kullanıcı bir resim yükler, ilgili işlem modülünü seçer ve sonucu anında görür. Arayüz olabildiğince sade tutulmuştur; yalnızca işlemi başlatacak kontroller ve işlem sonucu görüntü bulunur.

> **Kritik Kural:** Tüm görüntü işleme adımları, hazır kütüphane fonksiyonları kullanılmadan, algoritmaların matematiksel altyapısı **sıfırdan** uygulanarak geliştirilecektir.

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|-----------|---------------|
| **Python** | Ana programlama dili |
| **NumPy** | Matris/dizi temsili ve piksel düzeyinde matematiksel işlemler |
| **OpenCV** | *Yalnızca* görüntü okuma/yazma/gösterme — işleme fonksiyonları kullanılmıyor |
| **Matplotlib** | Histogram görselleştirme ve karşılaştırmalı gösterim |
| **Tkinter** | Basit ve sade kullanıcı arayüzü |

---

## 🔬 Modüller ve Algoritmalar

Her modül, ilgili algoritmayı tamamen matris düzeyinde uygular. Parametreler metin kutusu ile girilir, buton ile işlem başlatılır.

| # | Modül | Arayüz Kontrolü |
|---|-------|----------------|
| 1 | **Gri Dönüşüm** | Buton |
| 2 | **Binary Dönüşüm** | Eşik değeri girişi + Buton |
| 3 | **Görüntü Döndürme** | Açı girişi + Buton |
| 4 | **Görüntü Kırpma** | 4 koordinat girişi + Buton |
| 5 | **Yakınlaştırma / Uzaklaştırma** | Ölçek girişi + Buton |
| 6 | **Renk Uzayı Dönüşümleri** | HSV / YCbCr butonları |
| 7 | **Histogram Analizi ve Germe** | Buton |
| 8 | **Aritmetik İşlemler** | Mod + α değeri girişi + Buton |
| 9 | **Kontrast Artırma** | α ve β girişi + Buton |
| 10 | **Konvolüsyon (Mean)** | Çekirdek boyutu girişi + Buton |
| 11 | **Tek Eşikleme** | Eşik değeri girişi + Buton |
| 12 | **Kenar Bulma (Prewitt)** | Buton |
| 13 | **Gürültü Ekleme & Filtreleme** | Oran girişi + Filtre seçim butonu |
| 14 | **Unsharp Maskeleme** | k değeri girişi + Buton |
| 15 | **Morfolojik İşlemler** | 4 işlem butonu |

---

## 🖥️ Uygulama Çalışma Akışı

```
1. Görüntü Yükleme   → Kullanıcı bir resim seçer
2. Modül Seçimi      → İstediği işlem modülüne tıklar
3. Parametre Girişi  → Gerekli değer metin kutusuna yazılır
4. Sonuç             → İşlenmiş görüntü gösterilir
```

---

