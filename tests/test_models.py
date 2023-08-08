import models
import pytest

@pytest.fixture()
def vlan():
    vlans = models.Vlan()
    vlans.vlan_id = 10
    vlans.name = 'test'
    vlans.description = 'test_vlan'

    return vlans

@pytest.fixture()
def device():
    device = models.Device()
    device.hostname = 'test.dfw1'

    return device

class TestDevices:
    def test_get_all_devices(self, fake_db, device):
        fake_db.add(device)
        fake_db.commit()
        model = models.Device()
        result = model.get_devices()
        expected_result = 'test.dfw1'

        assert result[0].hostname == expected_result
        assert len(result) == 1

    def test_get_devices_count(self, fake_db, device):
        fake_db.add(device)
        fake_db.commit()
        model = models.Device()
        result = model.get_devices_count()
        expected_result = 1

        assert result == expected_result

    def test_get_device_vlans(self, fake_db, vlan, device):
        device.vlans.append(vlan)
        fake_db.add(device)
        fake_db.add(vlan)
        fake_db.commit()
        model = models.Device()
        result = model.get_device_vlans(device.hostname)

        assert isinstance(result[0], models.Vlan)
        assert result[0].vlan_id == 10

class TestVlans():
    def test_get_vlans(self, fake_db, vlan):
        fake_db.add(vlan)
        fake_db.commit()
        model = models.Vlan()
        result = model.get_vlans()
        expected_result = 10

        assert result[0].vlan_id == expected_result

    def test_get_vlans_count(self, fake_db, vlan):
        fake_db.add(vlan)
        fake_db.commit()
        model = models.Vlan()
        result = model.get_vlans_count()
        expected_result = 1

        assert result == expected_result

    def test_get_vlans_on_devices(self, fake_db, vlan, device):
        vlan.devices.append(device)
        fake_db.add(vlan)
        fake_db.add(device)
        fake_db.commit()
        model =  models.Vlan()
        result = model.get_vlans_on_devices(vlan.vlan_id)

        assert isinstance(result[0], models.Device)
        assert result[0].hostname == device.hostname


