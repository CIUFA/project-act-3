# tests/test_ip_info_gui.py

from ip_info_gui.ip_info_gui import fetch_ip_data

def test_fetch_ip_data_returns_dict():
    data = fetch_ip_data()
    assert isinstance(data, dict)

def test_fetch_ip_data_has_required_keys():
    data = fetch_ip_data()
    required_keys = ["IPv4 Address", "IPv6 Address", "City", "Region", "Country"]
    for key in required_keys:
        assert key in data
