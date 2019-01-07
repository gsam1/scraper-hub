import os, sys
import docker
# Hacky imports to test inital functionallity,
# later on will be removed as everything 
# will be imported by the parent admin api
config_path = os.path.abspath(os.pardir) + '/config'
sys.path.append(config_path)
from config import admin_config

# Setting a temp Global
ENV = 'development'

class ClientDocker(object):
    def __init__(self, url):
        self.client = docker.DockerClient(base_url=url)
    
    def get_active_containers(self):
        return self.client.containers.list()

    def get_all_containers(self):
        container_list = self.client.containers.list(all=True)
        all_containers = []
        for container in container_list:
            all_containers.append(container.name)
        
        return all_containers


def main():
    config = admin_config[ENV]()
    cld = ClientDocker(config.docker_url)
    print(cld.get_all_containers())


if __name__ == '__main__':
    main()