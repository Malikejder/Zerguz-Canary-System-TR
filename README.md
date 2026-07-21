# 🐦 Zerguz Canary System

**Zerguz**, Cyber Deception (Siber Yanıltma) prensiplerine dayanan, Python tabanlı yerel bir Canary Token (Yem Belge) altyapısıdır. Bir SOC analisti veya blue team üyesinin, ağında yetkisiz erişim / lateral movement / insider threat gibi tehditleri **sıfır false-positive** ile anlık olarak tespit etmesini sağlar.

Sistem, cazip bir isim taşıyan sahte bir Word belgesi (`.doc`) üretir. Bu belge açıldığı an, içine gömülü görünmez bir izleme pikseli sessizce Zerguz sunucusuna bir HTTP isteği gönderir. Bu istek; saldırganın **IP adresi**, **User-Agent bilgisi** ve **zaman damgasını** anında ifşa eder ve olayı otomatik olarak **CEF (Common Event Format)** standardında SIEM'e hazır hale getirir.

---

## 🎯 Neden Kritik?

Bu belgeyi normal şartlarda hiç kimsenin açmaması gerekir. Bu yüzden `/track/` endpoint'ine gelen **her istek**, kesin bir ihlal göstergesidir:

- ✅ Sıfır false-positive — dosya sadece yetkisiz erişim durumunda tetiklenir
- ✅ CEF formatlı çıktı sayesinde Splunk, QRadar, ArcSight gibi kurumsal SIEM'lere doğrudan entegre edilebilir
- ✅ Saldırganın makinesine hiçbir zararlı kod bulaştırmadan, tamamen pasif ve yasal bir tespit yöntemi
- ✅ Belge, Microsoft Word tarafından hatasız render edilir; şüphe uyandırmaz

---

## 🗂️ Proje Yapısı

```
zerguz/
├── zerguz_server.py       # Flask tabanlı canary dinleyici sunucu
├── zerguz_generator.py    # Sahte .doc yem belgesi üretici
├── zerguz_siem.log        # (otomatik oluşur) CEF formatlı alarm kayıtları
└── README.md
```

---

## ⚙️ Gereksinimler

- Python 3.8+
- Flask

```bash
pip install flask
```

---

## 🚀 Kurulum ve Kullanım

### 1. Sunucuyu başlat

```bash
python3 zerguz_server.py
```

Sunucu `0.0.0.0:5000` adresinde dinlemeye başlar ve terminalde şu banner'ı gösterir:

```
==============================================================================
                     ZERGUZ CANARY SYSTEM - SERVER ONLINE
==============================================================================
[*] Listening on: 0.0.0.0:5000
[*] Endpoint: /track/<doc_name>
[*] SIEM Log File: /path/to/zerguz_siem.log
==============================================================================
```

### 2. Yem belgeyi üret

Ayrı bir terminalde:

```bash
python3 zerguz_generator.py
```

Bu komut çalıştığı makinenin **yerel ağ IP'sini otomatik tespit eder** (elle IP girmene gerek yoktur) ve `2026_Maas_Zamları_ve_Prim_Listesi.doc` adında, içine izleme pikseli gömülü bir belge üretir.

```
==============================================================================
                           ZERGUZ CANARY GENERATOR
==============================================================================
[+] Belge basariyla uretildi : 2026_Maas_Zamları_ve_Prim_Listesi.doc
[+] Otomatik tespit edilen IP: 192.168.1.35
[+] Gomulu izleme adresi     : http://192.168.1.35:5000/track/zerguz_maas_listesi
[+] Sunucu Port              : 5000
==============================================================================
```

### 3. Belgeyi konumlandır

Üretilen `.doc` dosyasını, tespit edilmesini istediğin bir paylaşım klasörüne, masaüstüne veya test cihazına bırak.

### 4. Tetikleme

Belge Microsoft Word ile açıldığında (veya test amaçlı doğrudan tarayıcıdan `http://<IP>:5000/track/zerguz_maas_listesi` adresine gidildiğinde), sunucu terminalinde anında alarm tetiklenir:

```
##############################################################################
#                   ZERGUZ CANARY DETECTOR - CRITICAL ALERT                 #
##############################################################################
[!] STATUS         : CANARY TOKEN TRIGGERED
[!] TIMESTAMP      : 2026-07-21 14:32:10
[!] SOURCE IP      : 192.168.1.87
[!] USER AGENT     : Mozilla/5.0 (Windows NT 10.0; Win64; x64)
[!] DOCUMENT NAME  : zerguz_maas_listesi
[!] REQUEST METHOD : GET
------------------------------------------------------------------------------
[SIEM] CEF FORMATTED EVENT:
CEF:0|Zerguz|CanarySystem|1.0|100|Canary Token Triggered|10|src=192.168.1.87 ...
##############################################################################
```

Aynı olay, `zerguz_siem.log` dosyasına da otomatik olarak append edilir:

```bash
cat zerguz_siem.log
```

---

## 🧩 Mimari Detaylar

| Bileşen | Açıklama |
|---|---|
| `zerguz_server.py` | Flask üzerinde `/track/<doc_name>` endpoint'i sunar, gelen isteği yakalar, CEF'e çevirir, loglar ve şeffaf 1x1 PNG döner |
| `zerguz_generator.py` | HTML tabanlı, Word uyumlu `.doc` belgesi üretir; `socket` ile makinenin gerçek yerel IP'sini otomatik bulur |
| CEF Formatı | `CEF:0|Zerguz|CanarySystem|1.0|100|Canary Token Triggered|10|src=...` yapısında, kurumsal SIEM standartlarına uygun |
| Görünmezlik | `<img>` etiketi `display:none`, `width=1`, `height=1` ile tamamen gizlenmiştir; Word'de görsel olarak fark edilmez |

---

## ⚠️ Sorumluluk Reddi

Bu proje **yalnızca eğitim, portfolyo ve yetkili güvenlik testleri** amacıyla geliştirilmiştir. Kendi sahip olduğun veya test için yazılı izin aldığın ortamlar dışında kullanılması yasal sorumluluk doğurabilir.

---

## 📌 Etiketler

`#CyberDeception` `#CanaryToken` `#BlueTeam` `#SOC` `#ThreatDetection` `#SIEM` `#CEF` `#Python` `#Flask`
