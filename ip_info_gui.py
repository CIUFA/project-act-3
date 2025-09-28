import tkinter as tk
import requests

API_URL = "https://ipapi.co/json/"

def fetch_ip_info():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def show_ip_info():
    data = fetch_ip_info()
    text_box.delete("1.0", tk.END)  # clear previous content

    if "error" in data:
        text_box.insert(tk.END, f"Error: {data['error']}")
        return
    
    lines = [
        f"IP Address: {data.get('ip')}",
        f"City: {data.get('city')}",
        f"Region: {data.get('region')}",
        f"Country: {data.get('country_name')} ({data.get('country')})",
        f"Postal: {data.get('postal')}",
        f"Latitude/Longitude: {data.get('latitude')}, {data.get('longitude')}",
        f"Timezone: {data.get('timezone')}",
        f"Org/ISP: {data.get('org')}",
        f"ASN: {data.get('asn')}"
    ]

    text_box.insert(tk.END, "\n".join([line for line in lines if line]))

# Build GUI
root = tk.Tk()
root.title("Public IP Information")
root.geometry("400x300")

btn = tk.Button(root, text="Get IP Info", command=show_ip_info)
btn.pack(pady=10)

text_box = tk.Text(root, wrap="word", height=12, width=45)
text_box.pack(padx=10, pady=10)

root.mainloop()
