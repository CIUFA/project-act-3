from app import fetch_ip_data

def test_fetch_ip_data():
    data = fetch_ip_data()
    assert "ip" in data
    assert any(k in data for k in ["asn", "org", "country_name"])
