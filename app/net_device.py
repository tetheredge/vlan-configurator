from netmiko import ConnectHandler, redispatch

import app.vault_client
import logging

logging.basicConfig(level=logging.DEBUG)

class NetDevice():
    def __init__(self, device, config_file=None):
        if config_file is not None:
            self.config_file = config_file
        else:
            self.config_file = '~/.ssh/config'

        self.device = list(device.keys())[0]
        self.device_details = device[self.device]

    def connection_params(self):
        return {
            'device_type': 'linux_ssh',
            'host': self.device,
            'username': self.device_details['username'],
            'password': self.device_details['password'],
            'conn_timeout': 35,
            'banner_timeout': 60,
            'use_keys': False,
            'verbose': True,
            'ssh_config_file': self.config_file,
            'allow_agent': False,
            'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
            'session_log': 'output.txt'
        }

    def network_conn(self):
        return ConnectHandler(**self.connection_params())

    def get_vlan_brief(self):
        conn = self.network_conn()
        conn.find_prompt()
        logging.debug(f"logged into {self.device_details['username']}")
        conn.write_channel(f"{self.device_details['password']}\n")

        conn.read_until_prompt_or_pattern(pattern="#")
        logging.debug(f"\n{'*'*10} Connected to net device: {self.device_details['username']} {'*'*10}\n")

        redispatch(conn, device_type=self.device_details['type'])
        conn.find_prompt()
        vlan_data = conn.send_command("show vlan brief", use_textfsm=True)
        conn.disconnect()

        return vlan_data
