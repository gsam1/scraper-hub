import os, sys
import docker
import random
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
                'image': container.image.tags[0],
                'ports': container.attrs['NetworkSettings']['Ports']
            })

        return container_list

    def _get_host_port_list(self, container_list):
        # containers = self.get_all_containers
        external_ports = []
        for container in container_list:
            # get the ports in the container list
            container_ports = container['ports'].keys()
            external_port_list = []
            # loop over the container ports
            for port in container_ports:
                try:
                    external_port = container['ports'][port][0]['HostPort']
                except TypeError:
                    external_port = port.split('/')[0]
                # add external port to list
                external_port_list.append(external_port)
            external_ports.append({
                'name': container['name'],
                'image': container['image'],
                'external-port-lists': external_port_list
            })

        return external_ports
    
    def _generate_random_port(self):
        generated_port_number = 5000 + random.randint(1, 4000)
        return str(generated_port_number)

    def _search_for_port(self, port):
        container_image_port_list = self.get_all_container_ports()

        for container in container_image_port_list:
            if container['port'] == port:
                return True
        
        return False
    
    def 

    def get_active_containers(self):
        active_containers = self.client.containers.list()
        return self._create_container_obj_list(active_containers)

    def get_active_container_ports(self):
        active_containers = self.get_active_containers()
        return self._get_host_port_list(active_containers)
        
    def get_all_containers(self):
        all_containers = self.client.containers.list(all=True)
        return self._create_container_obj_list(all_containers)
    
    def get_all_container_ports(self):
        all_containers = self.get_all_containers()
        return self._get_host_port_list(all_containers)
    
    def run_container(self, image, port, volume=None, env_vars=None):
        restart_policy = {'Name':'always', 'MaximumRetryCount':5}
        if volume is not None:
            volume = {'/home/vagrant/' + image + '/data': kwargs['volume'] }
        
        # {'2222/tcp': 3333}
        ports = {''}
        # TODO: Handle ports
        # 1. Check if container is needed
        # 2. Check if port is taken - TRUE -> assign a new random one 5000+
        # 3. Return container



        container = self.client.containers.run(image, restart_policy=restart_policy,
                                                port={}, detach=True)
        
        return image


def main():
    config = admin_config[ENV]()
    cld = ClientDocker(config.docker_url)
    print(cld.get_active_containers())


if __name__ == '__main__':
    main()