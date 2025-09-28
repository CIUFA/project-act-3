import requests
import sys

API_URL = "https://ipapi.co/json/"

def fetch_ip_info():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error fetching IP info: {e}", file=sys.stderr)
        return None

def main():
    print("Fetching current public IP information …")
    info = fetch_ip_info()
    if not info:
        print("Failed to retrieve IP info.")
        return
    
    print("=== Public IP Info ===")
    print(f"IP Address: {info.get('ip')}")
    print(f"City: {info.get('city')}")
    print(f"Region: {info.get('region')}")
    print(f"Country: {info.get('country_name')} ({info.get('country')})")
    print(f"Postal: {info.get('postal')}")
    print(f"Latitude/Longitude: {info.get('latitude')}, {info.get('longitude')}")
    print(f"Timezone: {info.get('timezone')}")
    print(f"Org/ISP: {info.get('org')}")
    print(f"ASN: {info.get('asn')}")

if __name__ == "__main__":
    main()
