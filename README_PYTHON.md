## Pomodoro Timer (Python Masaüstü Uygulaması)

Modern tasarımlı, odaklı çalışmayı destekleyen bir **Pomodoro zamanlayıcı**. Uygulama hem şık bir **Tkinter masaüstü arayüzü** hem de hafif bir **terminal sürümü** içerir. Windows için **ikonlu .exe masaüstü uygulaması** olarak da kullanılabilir.

---

## Özellikler

- **Modern GUI arayüzü**
  - Koyu tema, turuncu vurgu rengi
  - Büyük ve okunabilir süre göstergesi
  - İlerleme çubuğu ile anlık durum
  - Özel tasarlanmış turuncu saat ikonlu masaüstü uygulaması

- **Esnek zaman ayarları**
  - Çalışma süresi (1–60 dakika arası)
  - Mola süresi (1–30 dakika arası)
  - Set sayısı (1–10 arası)

- **Akıllı çalışma / mola akışı**
  - Bir set bittiğinde otomatik veya manuel mola başlatma
  - Mola bitince otomatik veya manuel bir sonraki sete geçiş
  - Her aşamada bilgilendirici uyarı pencereleri

- **Melodili ses uyarıları**
  - 3 farklı kısa melodi seçeneği
  - Set / mola bitiminde seçilen melodi çalar

- **Ayarlar penceresi**
  - Özel dropdown (açılır liste) bileşenleri
  - Pencereyi sürüklerken dropdown konumu otomatik güncellenir
  - Otomatik mola / manuel mola seçimi
  - Ses seçimi (3 farklı melodi)

- **Terminal sürümü**
  - Klavye kısayolları ile hızlı kullanım
  - Hafif, kurulum gerektirmeyen deneyim

---

## Dosyalar

- `pomodoro_gui.py`  
  Modern Tkinter arayüzlü masaüstü Pomodoro uygulaması.

- `pomodoro_terminal.py`  
  Komut satırından çalışan terminal sürümü.

- `pomodoro_icon.ico` (opsiyonel)  
  Windows masaüstü uygulaması için turuncu saat uygulama ikonu.

---

## Kurulum

### 1. Gereksinimler

- **Python 3.11+** (3.6 ve üzeri de çalışır, önerilen 3.11)
- Windows, Linux veya macOS (GUI için Tkinter yüklü olmalı – Windows kurulumlarında varsayılan gelir)

### 2. Depoyu / Projeyi Çekme

Projeyi bir klasöre alın (örneğin `C:\Users\User\Desktop\pomodoro_python`).

İsteğe bağlı olarak sanal ortam kullanabilirsiniz:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

Gerekirse bağımlılıkları kurun (çoğu sistemde ekstra paket gerekmez):

```bash
pip install -r requirements.txt
```

---

## GUI Sürümünü Çalıştırma (Önerilen)

```bash
python pomodoro_gui.py
```

Çalıştırdığınızda:
- Ana pencerede büyük süre göstergesi, set bilgisi ve ilerleme çubuğu görünür.
- **Başlat / Duraklat / Sıfırla** butonları ile zamanlayıcıyı kontrol edersiniz.
- **Ayarlar** butonundan tüm süreleri, set sayısını, otomatik mola davranışını ve sesi değiştirebilirsiniz.

---

## Terminal Sürümünü Çalıştırma

```bash
python pomodoro_terminal.py
```

Temel kontroller:

- **ENTER** → Başlat / Duraklat
- **R** → Sıfırla
- **S** → Ayarlar menüsü
- **Q** → Çıkış

Terminal sürümü, grafik arayüz istemeyen veya uzak sunucuda çalışan kullanıcılar için uygundur.

---

## Windows İçin İkonlu .EXE Oluşturma

GUI sürümünü Windows’ta bağımsız bir masaüstü uygulaması olarak kullanmak için **PyInstaller** ile paketleyebilirsiniz.

1. Proje klasörüne geçin:

```powershell
cd "C:\Users\User\Desktop\pomodoro_python"
```

2. PyInstaller kurulumu (bir kez yeterli):

```powershell
pip install pyinstaller
```

3. `pomodoro_icon.ico` dosyasını bu klasöre koyun (turuncu saat ikonunuz).

4. .exe oluşturun:

```powershell
python -m PyInstaller --noconsole --onefile --icon pomodoro_icon.ico pomodoro_gui.py
```

5. Oluşan dosya:

- `dist\pomodoro_gui.exe`
- Bu dosyayı masaüstüne kopyalayabilir veya kısayol oluşturabilirsiniz.

Artık uygulama, kendine ait turuncu saat simgesiyle sıradan bir Windows uygulaması gibi açılıp kapanır.

---

## Ayarlar Ekranı

GUI içindeki **Ayarlar** penceresinden şunları yönetebilirsiniz:

- **Çalışma Süresi (dakika)**: 1–60 arası değerler.
- **Mola Süresi (dakika)**: 1–30 arası değerler.
- **Set Sayısı**: 1–10 arası.
- **Mola Başlatma**: Otomatik veya Manuel.
- **Ses Seçeneği**: 3 farklı kısa melodi.

Açılır listeler özel bir dropdown bileşeni ile yapılmıştır; pencereyi sürüklediğinizde dropdown da konumunu otomatik günceller.

---

## Kullanılan Teknolojiler

- **Python** 3.x
- **Tkinter** – GUI arayüzü (pencere, butonlar, etiketler, açılır menüler)
- **threading** – Arka planda çalışan zamanlayıcı iş parçacığı
- **winsound** (Windows) – Beep tabanlı melodiler
- **PyInstaller** – Windows için tek dosyalı `.exe` paketleme
- **Standart Python kütüphaneleri** – `time`, `threading`, vb.

Bu proje, pomodoro tekniğini günlük çalışma rutinine şık ve kullanımı kolay bir masaüstü aracı olarak eklemek isteyen kullanıcılar için tasarlanmıştır.