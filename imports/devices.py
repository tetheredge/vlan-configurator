import db
import models
import logging

from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

class DeviceImporter():
    def __init__(self):
        pass

    def get_file_name(self):
        data_folder = Path(__file__).parents[1]
        filename = data_folder / 'imports/devices_to_import.txt'

        return filename

    def save_file_contents_to_db(self):
        contents = open(self.get_file_name(), 'r')
        for device in contents:
            device = device.strip()
            item = db.session \
                .query(models.Device) \
                .filter_by(hostname=device) \
                .first()

            if item is not None:
                logging.debug(f'The device, {device}, already exists in the db')
            else:
                with db.session_scope() as session:
                    model = models.Device(hostname=device)
                    session.add(model)
                logging.debug(f'The device, {device}, was added to the db')
        contents.close()


