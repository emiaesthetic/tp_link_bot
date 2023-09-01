from enum import Enum


class Endpoint(Enum):
    ADD_FILTER = "cgi?3"
    REMOVE_FILTER = "cgi?4"
    DEVICES = "cgi?5"
    BLACK_LIST = "cgi?6"
    REBOOT = "cgi?7"


class Payload(Enum):
    ADD_FILTER = (
        "[LAN_WLAN_MACTABLEENTRY#0,0,0,0,0,0#1,1,0,0,0,0]0,4\r\n"
        "Enabled=1\r\n"
        "Description=black\r\n"
        "MACAddress={}\r\n"
        "HostName=wlan0\r\n "
    )

    REMOVE_FILTER = "[LAN_WLAN_MACTABLEENTRY#{}#0,0,0,0,0,0]0,0\r\n"

    DEVICES = (
        "[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,4\r\n"
        "leaseTimeRemaining\r\n"
        "MACAddress\r\n"
        "hostName\r\n"
        "IPAddress\r\n"
    )

    BLACK_LIST = (
        "[LAN_WLAN_MACTABLEENTRY#0,0,0,0,0,0#1,1,0,0,0,0]0,4\r\n"
        "Enabled\r\n"
        "MACAddress=\r\n"
        "Description=\r\nHostName\r\n "
    )

    REBOOT = "[ACT_REBOOT#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n"


class Pattern(Enum):
    MAC_ADDRESS = r"MACAddress=(?P<MACAddress>.*)\n"
    HOSTNAME = r"hostName=(?P<hostName>.*)\n"
    IP_ADDRESS = r"IPAddress=(?P<IPAddress>.*)\n"
    DEVICE_ID = r"(?i)(?P<id>\[[\d,]+]).*\n"
