from flask import Flask, request, send_file
import io
import datetime
import os

app = Flask(__name__)

SIEM_LOG_FILE = "zerguz_siem.log"

def zerguz_get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def zerguz_build_cef(src_ip, user_agent, doc_name, timestamp):
    safe_ua = user_agent.replace("|", "-").replace("=", "-") if user_agent else "Unknown"
    cef_message = (
        "CEF:0|Zerguz|CanarySystem|1.0|100|Canary Token Triggered|10|"
        "src=" + str(src_ip) +
        " suser=Unknown" +
        " request=/track/" + str(doc_name) +
        " requestMethod=" + str(request.method) +
        " cs1Label=UserAgent cs1=" + safe_ua +
        " cs2Label=DocumentName cs2=" + str(doc_name) +
        " rt=" + str(timestamp)
    )
    return cef_message

def zerguz_write_siem_log(cef_message, timestamp):
    with open(SIEM_LOG_FILE, "a", encoding="utf-8") as siem_file:
        siem_file.write("[" + timestamp + "] " + cef_message + "\n")

def zerguz_print_alert_banner(src_ip, user_agent, doc_name, timestamp, cef_message):
    banner_width = 78
    print("\n")
    print("#" * banner_width)
    print("#" + " ZERGUZ CANARY DETECTOR - CRITICAL ALERT ".center(banner_width - 2, " ") + "#")
    print("#" * banner_width)
    print("[!] STATUS         : CANARY TOKEN TRIGGERED")
    print("[!] TIMESTAMP      : " + timestamp)
    print("[!] SOURCE IP      : " + str(src_ip))
    print("[!] USER AGENT     : " + str(user_agent))
    print("[!] DOCUMENT NAME  : " + str(doc_name))
    print("[!] REQUEST METHOD : " + str(request.method))
    print("-" * banner_width)
    print("[SIEM] CEF FORMATTED EVENT:")
    print(cef_message)
    print("#" * banner_width)
    print("\n")

def zerguz_get_transparent_png_bytes():
    return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

@app.route("/track/<doc_name>", methods=["GET"])
def zerguz_track_endpoint(doc_name):
    src_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Unknown")
    timestamp = zerguz_get_timestamp()

    cef_message = zerguz_build_cef(src_ip, user_agent, doc_name, timestamp)
    zerguz_write_siem_log(cef_message, timestamp)
    zerguz_print_alert_banner(src_ip, user_agent, doc_name, timestamp, cef_message)

    png_bytes = zerguz_get_transparent_png_bytes()
    return send_file(
        io.BytesIO(png_bytes),
        mimetype="image/png",
        as_attachment=False,
        download_name="pixel.png"
    )

if __name__ == "__main__":
    print("\n")
    print("=" * 78)
    print("ZERGUZ CANARY SYSTEM - SERVER ONLINE".center(78, " "))
    print("=" * 78)
    print("[*] Listening on: 0.0.0.0:5000")
    print("[*] Endpoint: /track/<doc_name>")
    print("[*] SIEM Log File: " + os.path.abspath(SIEM_LOG_FILE))
    print("=" * 78)
    print("\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
