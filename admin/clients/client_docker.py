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

    def _create_container_obj_list(self, cntrlist):
        container_list = []
        for container in cntrlist:
            container_list.append({
                'name': container.name,
                'spec': container.attrs
            })

        return container_list
    
    def get_active_containers(self):
        active_containers = self.client.containers.list()
        return self._create_container_obj_list(active_containers)

    def get_all_containers(self):
        all_containers = self.client.containers.list(all=True)
        return self._create_container_obj_list(all_containers)


def main():
    config = admin_config[ENV]()
    cld = ClientDocker(config.docker_url)
    print(cld.get_active_containers())


if __name__ == '__main__':
    main()