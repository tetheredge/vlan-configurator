import os

class Credentials(object):
    def __init__(self):
        pass

    def get_db_name(self):
        return os.environ.get('DB_NAME', 'vlan_config_db')

    def get_db_password(self):
        return os.environ.get('DB_PASSWORD', 'vlan_config_db_password')

    def get_db_user(self):
        return os.environ.get('DB_USER', 'vlan_config_db_user')

    def get_db_hostname(self):
        return os.environ.get('DB_HOST', '127.0.0.1')

    def get_db_port(self):
        return os.environ.get('DB_PORT', 5432)