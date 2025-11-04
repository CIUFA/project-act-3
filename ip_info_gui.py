from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# --- IP APIs ---
API_ENDPOINTS = {
    "ipapi": "https://ipapi.co/json/",
    "ipify": "https://api64.ipify.org?format=json",
    "ipwhois": "https://ipwho.is/"
}

# --- Helper Functions ---
def fetch_from_api(url):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def merge_ip_data(*data_sources):
    merged = {}
    for data in data_sources:
        if not isinstance(data, dict):
            continue
        for key, value in data.items():
            if value and key not in merged:
                merged[key] = value
    return merged

def fetch_ip_data():
    ipify_data = fetch_from_api(API_ENDPOINTS["ipify"])
    ip_address = ipify_data.get("ip")

    ipapi_data = fetch_from_api(API_ENDPOINTS["ipapi"])
    ipwhois_data = fetch_from_api(API_ENDPOINTS["ipwhois"] + (ip_address or ""))

    merged_data = merge_ip_data(ipify_data, ipapi_data, ipwhois_data)
    return merged_data

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ipinfo")
def ipinfo():
    data = fetch_ip_data()
    # Filter important keys for display
    important_keys = {
        "IP Address": data.get("ip"),
        "City": data.get("city"),
        "Region": data.get("region") or data.get("regionName"),
        "Country": f"{data.get('country_name') or data.get('country')} ({data.get('country_code') or data.get('country_code_iso3')})",
        "Postal": data.get("postal"),
        "Latitude/Longitude": f"{data.get('latitude') or data.get('lat')}, {data.get('longitude') or data.get('lon')}",
        "Timezone": data.get("timezone"),
        "Organization": data.get("org"),
        "ASN": data.get("asn"),
        "IP Version": "IPv6" if ":" in str(data.get("ip")) else "IPv4",
    }
    # Remove empty values
    filtered_data = {k: v for k, v in important_keys.items() if v}
    return jsonify(filtered_data)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
