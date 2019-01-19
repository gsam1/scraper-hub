import os
import json


class Config(object):
    def __init__(self):
        self.host_config = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/config.json'))
        self.image_map = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/image_type_map.json'))

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.api_port = self.host_config['dev']['api-port']
        self.docker_url = self.host_config['dev']['docker-host-url']

class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.api_port = self.host_config['dev']['api-port']
        self.docker_url = self.host_config['dev']['docker-host-url']

class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.api_port = self.host_config['dev']['api-port']
        self.docker_url = self.host_config['dev']['docker-host-url']

admin_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
