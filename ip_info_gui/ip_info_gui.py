from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# --- IP APIs ---
API_ENDPOINTS = {
    "ipapi": "https://ipapi.co/json/",
    "ipify_ipv4": "https://api.ipify.org?format=json",
    "ipify_ipv6": "https://api64.ipify.org?format=json",
    "ipwhois": "https://ipwho.is/",  # Append IP later
    "asn_lookup": "https://api.hackertarget.com/aslookup/?q="  # Append IP
}

# --- Helper Functions ---
def fetch_from_api(url):
    """Fetch JSON data from an API with error handling."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except:
        return {}

def fetch_asn_fallback(ip):
    """Fetch ASN from hackertarget API (plain text fallback)."""
    if not ip:
        return {}
    try:
        resp = requests.get(API_ENDPOINTS["asn_lookup"] + ip, timeout=5)
        resp.raise_for_status()
        text = resp.text.strip()
        if text:
            parts = text.split(" ", 1)
            asn = parts[0] if len(parts) > 0 else None
            org = parts[1] if len(parts) > 1 else None
            return {"asn": asn, "org": org}
    except:
        return {}
    return {}

def merge_ip_data(*data_sources):
    """Merge multiple API responses into one, filtering duplicates."""
    merged = {}
    for data in data_sources:
        if not isinstance(data, dict):
            continue
        for key, value in data.items():
            if value and key not in merged:
                merged[key] = value
    return merged

def fetch_ip_data():
    """Fetch IP info with fallback defaults."""
    try:
        ipv4_data = fetch_from_api(API_ENDPOINTS["ipify_ipv4"])
        ipv6_data = fetch_from_api(API_ENDPOINTS["ipify_ipv6"])
        ip_address = ipv4_data.get("ip", None)
        ipapi_data = fetch_from_api(API_ENDPOINTS["ipapi"])
        ipwhois_data = fetch_from_api(API_ENDPOINTS["ipwhois"] + (ip_address or "")) if ip_address else {}
        asn_data = fetch_asn_fallback(ip_address)
        merged_data = merge_ip_data(ipv4_data, ipv6_data, ipapi_data, ipwhois_data, asn_data)

        # --- Fallback defaults ---
        default_data = {
            "IPv4 Address": merged_data.get("ip") or "0.0.0.0",
            "IPv6 Address": merged_data.get("ip6") or "::",
            "City": merged_data.get("city") or "Unknown",
            "Region": merged_data.get("region") or merged_data.get("regionName") or "Unknown",
            "Country": merged_data.get("country_name") or merged_data.get("country") or "Unknown",
            "Country Code": merged_data.get("country_code") or merged_data.get("country_code_iso3") or "XX",
            "Postal": merged_data.get("postal") or "N/A",
            "Latitude": merged_data.get("latitude") or merged_data.get("lat") or 0.0,
            "Longitude": merged_data.get("longitude") or merged_data.get("lon") or 0.0,
            "Timezone": merged_data.get("timezone") or "UTC",
            "Organization": merged_data.get("org") or "N/A",
            "ASN": merged_data.get("asn") or "N/A"
        }

        return default_data

    except Exception as e:
        # If everything fails, return minimal static defaults
        return {
            "IPv4 Address": "0.0.0.0",
            "IPv6 Address": "::",
            "City": "Unknown",
            "Region": "Unknown",
            "Country": "Unknown",
            "Country Code": "XX",
            "Postal": "N/A",
            "Latitude": 0.0,
            "Longitude": 0.0,
            "Timezone": "UTC",
            "Organization": "N/A",
            "ASN": "N/A"
        }

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ipinfo")
def ipinfo():
    data = fetch_ip_data()
    return jsonify(data)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)

    //jobndjwendjnewkocnjweoij