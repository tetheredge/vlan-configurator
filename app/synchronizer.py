import app.net_device
import app.vault_client
import models
import db

class Synchronizer():
    def __init__(self):
        self.vault_client = app.vault_client.Vault()
        self.response = self.vault_client.get_response()

    def get_vlans_from_net_devices(self):
        all_devices_with_vlans = []
        device_details = {}
        devices = models.Device().get_devices()
        for device in devices:
            device_details[device.hostname] = self.response[device.hostname]
            net = app.net_device.NetDevice(device_details)
            vlans = net.get_vlan_brief()
            device_with_vlans = {device.hostname: vlans}
            all_devices_with_vlans.append(device_with_vlans)

        return all_devices_with_vlans

    def add_vlans_to_devices(self, vlans):
        devices = models.Device().get_devices()
        for device in devices:
            for vlan in vlans:
                if vlan['vlan_id'] in device.vlans:
                    continue
                else:
                    v = models.Vlan()
                    v.vlan_id = vlan['vlan_id']
                    v.name = vlan['name']

                    db.session.add(v)
                    device.vlans.append(v)
                    db.session.add(device)
                    db.session.commit()
            print(device.vlans)

