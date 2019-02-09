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

# client
class ClientDocker(object):
    def __init__(self, url):
        self.client = docker.DockerClient(base_url=url)

    def _create_container_obj_list(self, cntrlist):
        container_list = []
        for container in cntrlist:
            container_list.append({
                'name': container.name,
                'image': container.image.tags[0],
                'id': container.id,
                'status': container.status,
                'ports': container.attrs['NetworkSettings']['Ports']
            })

        return container_list

    def _get_host_port_list(self, container_list):
        # containers = self.get_all_containers
        external_ports_dict = []
        combined_ports_list = []
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
                combined_ports_list.append(external_port)
            external_ports_dict.append({
                'name': container['name'],
                'image': container['image'],
                'external-port-lists': external_port_list
            })
        self.combined_ports_list_ = combined_ports_list
        return external_ports_dict
    
    def _generate_random_port(self):
        generated_port_number = 5000 + random.randint(1, 4000)
        return str(generated_port_number)

    def _search_for_port(self, port):
        #container_image_port_list = 
        self.get_all_container_ports()
        if port in self.combined_ports_list_:
            return True
        else:
            return False
    
    def _check_port_availability(self, port):
        return_port = port
        port_taken = True
        while port_taken == True:
            if self._search_for_port(return_port):
                return_port = self._generate_random_port()
            else:
                port_taken = False
        
        return return_port

    def _handle_ports(self, port_list):
        final_ports = {}
        for port in port_list:
            internal_port = f'{port}/tcp'
            external_port = self._check_port_availability(port)
            # TODO: handle multiple ports
            final_ports[internal_port] = external_port
        
        return final_ports
    
    def _get_last_container_of_type(self, container_list):
        list_split = [item.split('-') for item in container_list]
        max_val = 0
        for item in list_split:
            # check whether the item contains two items, as its supposed to
            if len(item) == 2:
                try:
                    if int(item[1]) > max_val:
                        max_val = int(item[1])
                except ValueError: # handle if there is no int
                    pass
        
        return max_val

    def _generate_new_name(self, image):
        all_containers = self.get_all_containers()
        container_names = [container['name'] for container in all_containers]
        same_image_containers = list(filter(lambda name: image in name, container_names))
        new_container_id = self._get_last_container_of_type(same_image_containers) + 1
        # don't suppose there is going to be more than 99 container
        new_name = image + '-' + str(new_container_id).zfill(2)

        return new_name
        
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
    
    def get_container(self, query_name):
        all_containers = self.get_all_containers()
        return_obj = {}
        # only 1 item in the filtered dict list
        result = list(filter(lambda cntr: cntr['name'] == query_name, all_containers))
        if len(result) > 0:
            return_obj['exists'] = True
            return_obj['name'] = result[0]['name']
            return_obj['id'] = result[0]['id']
            return_obj['ports'] = result[0]['ports']
            return_obj['status'] = result[0]['status']
        else:
            return_obj['exists'] = False

        return return_obj

    def start_container(self, container_id):
        container = self.client.containers.get(container_id)
        container.start()
        response = {
            'name': container.name,
            'id': container.id,
            'port': container.attrs['HostConfig']['PortBindings']
        }

        return response
    
    def provision_container(self, image, port, volume=None, env_vars=None):
        restart_policy = {'Name':'always'}
        
        ports = self._handle_ports(port)
        name = self._generate_new_name(image)

        if volume is not None:
            volume = {'/home/vagrant/' + name + '/data': {'bind': volume, 'mode': 'rw'}}

        container = self.client.containers.run(image, restart_policy=restart_policy,
                                                name=name, environment=env_vars,
                                                volumes=volume,
                                                ports=ports, detach=True)
        
        return {
            'name': name,
            'id':container.id,
            'port': ports
        }


def main():
    config = admin_config[ENV]()
    cld = ClientDocker(config.docker_url)
    print(cld.get_active_containers())


if __name__ == '__main__':
    main()