import socket

ZERGUZ_SERVER_PORT = "5000"
ZERGUZ_DOC_NAME = "2026_Maas_Zamları_ve_Prim_Listesi.doc"
ZERGUZ_TRACK_ENDPOINT = "zerguz_maas_listesi"

def zerguz_detect_local_ip():
    zerguz_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        zerguz_sock.connect(("8.8.8.8", 80))
        zerguz_local_ip = zerguz_sock.getsockname()[0]
    except Exception:
        try:
            zerguz_local_ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            zerguz_local_ip = "127.0.0.1"
    finally:
        zerguz_sock.close()
    return zerguz_local_ip

def zerguz_build_tracking_url(server_ip):
    return "http://" + server_ip + ":" + ZERGUZ_SERVER_PORT + "/track/" + ZERGUZ_TRACK_ENDPOINT

def zerguz_build_html_document(tracking_url):
    html_content = """<html xmlns:o='urn:schemas-microsoft-com:office:office'
xmlns:w='urn:schemas-microsoft-com:office:word'
xmlns='http://www.w3.org/TR/REC-html40'>
<head>
<meta charset='utf-8'>
<title>2026 Maas Zamlari ve Prim Listesi</title>
<!--[if gte mso 9]>
<xml>
<w:WordDocument>
<w:View>Print</w:View>
<w:Zoom>100</w:Zoom>
<w:DoNotOptimizeForBrowser/>
</w:WordDocument>
</xml>
<![endif]-->
<style>
body {{
font-family: Calibri, Arial, sans-serif;
font-size: 12pt;
color: #1f1f1f;
margin: 60px;
}}
h1 {{
font-size: 18pt;
color: #b30000;
border-bottom: 2px solid #b30000;
padding-bottom: 8px;
}}
h2 {{
font-size: 14pt;
color: #1f1f1f;
margin-top: 24px;
}}
table {{
border-collapse: collapse;
width: 100%;
margin-top: 12px;
}}
table, th, td {{
border: 1px solid #999999;
}}
th, td {{
padding: 8px;
text-align: left;
font-size: 11pt;
}}
th {{
background-color: #e6e6e6;
}}
.gizli-etiket {{
background-color: #ffe6e6;
color: #b30000;
font-weight: bold;
padding: 6px 10px;
display: inline-block;
margin-bottom: 20px;
border: 1px solid #b30000;
}}
.footer {{
margin-top: 40px;
font-size: 9pt;
color: #666666;
}}
</style>
</head>
<body>
<span class='gizli-etiket'>SIRKET ICI GIZLI VERI - YALNIZCA IK VE YONETIM KURULU ERISIMINE ACIKTIR</span>
<h1>2026 Yili Maas Zamlari ve Prim Dagilim Listesi</h1>
<p>Bu belge, 2026 mali yili icin planlanan personel maas zam oranlarini, departman bazli prim dagilimlarini ve yonetim kurulu onayli ucret duzenlemelerini icermektedir. Belge ic denetim ve Insan Kaynaklari Direktorlugu tarafindan hazirlanmis olup dagitimi kesinlikle yasaktir.</p>
<h2>Departman Bazli Zam Oranlari</h2>
<table>
<tr>
<th>Departman</th>
<th>Ortalama Zam Orani</th>
<th>Prim Katsayisi</th>
<th>Yururluk Tarihi</th>
</tr>
<tr>
<td>Bilgi Teknolojileri</td>
<td>%18</td>
<td>1.35</td>
<td>01.01.2026</td>
</tr>
<tr>
<td>Satis ve Pazarlama</td>
<td>%14</td>
<td>1.20</td>
<td>01.01.2026</td>
</tr>
<tr>
<td>Finans ve Muhasebe</td>
<td>%12</td>
<td>1.10</td>
<td>01.01.2026</td>
</tr>
<tr>
<td>Insan Kaynaklari</td>
<td>%15</td>
<td>1.25</td>
<td>01.01.2026</td>
</tr>
<tr>
<td>Ust Duzey Yonetim</td>
<td>%22</td>
<td>1.50</td>
<td>01.01.2026</td>
</tr>
</table>
<h2>Onay Sureci</h2>
<p>Yukaridaki oranlar Yonetim Kurulu'nun 12.12.2025 tarihli toplantisinda gorusulmus ve oy birligi ile onaylanmistir. Uygulamaya iliskin detayli bordro simulasyonlari IK Direktorlugu tarafindan ayrica departman yoneticilerine iletilecektir.</p>
<div class='footer'>
<p>Bu belge sirket ici kullanim icindir. Izinsiz kopyalanmasi, paylasilmasi veya dagitilmasi disiplin sorusturmasi baslatilmasina neden olabilir.</p>
</div>
<img src='{tracking_url}' width='1' height='1' style='display:none;border:0;' alt=''>
</body>
</html>"""
    return html_content.format(tracking_url=tracking_url)

def zerguz_write_document(html_content):
    with open(ZERGUZ_DOC_NAME, "w", encoding="utf-8") as doc_file:
        doc_file.write(html_content)

def zerguz_print_summary(server_ip, tracking_url):
    banner_width = 78
    print("\n")
    print("=" * banner_width)
    print("ZERGUZ CANARY GENERATOR".center(banner_width, " "))
    print("=" * banner_width)
    print("[+] Belge basariyla uretildi : " + ZERGUZ_DOC_NAME)
    print("[+] Otomatik tespit edilen IP: " + server_ip)
    print("[+] Gomulu izleme adresi     : " + tracking_url)
    print("[+] Sunucu Port              : " + ZERGUZ_SERVER_PORT)
    print("=" * banner_width)
    print("\n")

if __name__ == "__main__":
    server_ip = zerguz_detect_local_ip()
    tracking_url = zerguz_build_tracking_url(server_ip)
    html_content = zerguz_build_html_document(tracking_url)
    zerguz_write_document(html_content)
    zerguz_print_summary(server_ip, tracking_url)
