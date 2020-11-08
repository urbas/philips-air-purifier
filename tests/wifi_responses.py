UNCONFIGURED_WIFI = {
    "ssid": "PHILIPS Setup",
    "password": "",
    "protection": "open",
    "ipaddress": "192.168.1.1",
    "netmask": "255.255.255.0",
    "gateway": "192.168.1.1",
    "dhcp": True,
    "macaddress": "e8:c1:d7:07:c3:20",
    "cppid": "e8c1d7fffe07c320",
}


def configured_wifi(ssid):
    return {
        "ssid": ssid,
        "password": "",  # the purifier seems to actually hide the password
        "protection": "wpa-2",
        "ipaddress": "192.168.1.105",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "dhcp": True,
        "macaddress": "e8:c1:d7:07:c3:20",
        "cppid": "e8c1d7fffe07c320",
    }
