import re
from base64 import b64encode
from typing import NamedTuple, Optional

import requests

from src.configreader import config
from src.services.enums import Endpoint, Pattern, Payload


class Device(NamedTuple):
    mac_address: str
    hostname: str
    ip_address: Optional[str] = None
    device_id: Optional[str] = None


class Session:
    def __init__(self, host: str, port: str, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.headers = {}
        self.headers["Referer"] = f"http://{host}:{port}/mainFrame.htm"
        self.headers["Cookies"] = f"Authorization=Basic {self.basic_token_auth}"

    @property
    def basic_token_auth(self) -> str:
        raw_string = "{}:{}".format(self.username, self.password)
        return b64encode(raw_string.encode("ascii")).decode("ascii")

    @property
    def base_url(self) -> str:
        return "http://{}:{}".format(self.host, self.port)

    def page_url(self, endpoint: str) -> str:
        return "{}/{}".format(self.base_url, endpoint)

    def parse_string(self, string: str, pattern: str) -> list[str]:
        return re.findall(pattern, string, re.MULTILINE)

    def get_device_data(
        self, string: str, patterns: list[str]
    ) -> list[list[str]]:
        return [self.parse_string(string, pattern) for pattern in patterns]

    def send(self, endpoint: str, payload: str) -> str:
        page = self.page_url(endpoint)
        response = requests.post(url=page, headers=self.headers, data=payload)
        return response.text

    def get_wireless_connected_devices(self) -> list[Device]:
        string = self.send(Endpoint.DEVICES.value, Payload.DEVICES.value)
        patterns = (
            Pattern.MAC_ADDRESS.value,
            Pattern.HOSTNAME.value,
            Pattern.IP_ADDRESS.value,
        )
        data = self.get_device_data(string, patterns)

        devices = []
        for mac_address, hostname, ip_address in zip(*data):
            devices.append(
                Device(
                    mac_address=mac_address,
                    hostname=hostname,
                    ip_address=ip_address,
                )
            )
        return devices

    def get_blacklisted_devices(self) -> list[Device]:
        string = self.send(Endpoint.BLACK_LIST.value, Payload.BLACK_LIST.value)
        patterns = (
            Pattern.MAC_ADDRESS.value,
            Pattern.HOSTNAME.value,
            Pattern.DEVICE_ID.value,
        )
        data = self.get_device_data(string, patterns)

        devices = []
        for mac_address, hostname, device_id in zip(*data):
            devices.append(
                Device(
                    mac_address=mac_address,
                    hostname=hostname,
                    device_id=device_id,
                )
            )
        return devices

    def add_device_to_blacklist(self, mac_address: str) -> None:
        payload = Payload.ADD_FILTER.value.format(mac_address)
        self.send(Endpoint.ADD_FILTER.value, payload)

    def get_device_id(self, mac_address: str) -> Optional[str]:
        devices = self.get_blacklisted_devices()
        device_id = None
        for device in devices:
            if device.mac_address == mac_address and isinstance(
                device.device_id, str
            ):
                device_id = device.device_id[1:-1]
        return device_id

    def removed_device_from_blacklist(self, mac_address: str) -> None:
        device_id = self.get_device_id(mac_address)
        if device_id:
            payload = Payload.REMOVE_FILTER.value.format(device_id)
            self.send(Endpoint.REMOVE_FILTER.value, payload)
        else:
            print("MAC-address not blacklisted")

    def reboot(self) -> None:
        self.send(Endpoint.REBOOT.value, Payload.REBOOT.value)


session: Session = Session(
    host=config.host,
    port=config.port,
    username=config.username,
    password=config.password,
)
