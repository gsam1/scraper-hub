from flask import Flask, request
from flask import jsonify
from clients import ClientDocker
from config import admin_config

ENV = 'development'
admin = Flask(__name__)
config = admin_config[ENV]()
image_map = config.image_map
cld = ClientDocker(config.docker_url)

# helper functions
def request_image_mapper(request):
    image = image_map[request['type']][request['distribution']]['image']
    port = image_map[request['type']][request['distribution']]['default_port']
    volume = image_map[request['type']][request['distribution']]['data_location']
    env_vars = image_map[request['type']][request['distribution']]['env_vars']

    return image, port, volume, env_vars

def handle_port_response(port_dict, default_port, found):
    default_port = default_port[0] + '/tcp'
    if found:
        port = port_dict[default_port][0]['HostPort']
    else:
        port = port_dict[default_port]
    
    return port

# Routes
@admin.route('/')
def index():
    return 'Hello World!'

@admin.route('/get_all_containers')
def get_all_containers():
    return jsonify(cld.get_all_containers())

@admin.route('/get_active_containers')
def get_active_containers():
    return jsonify(cld.get_active_containers())

@admin.route('/get_active_container_ports')
def get_active_container_ports():
    return jsonify(cld.get_active_container_ports())

@admin.route('/get_all_container_ports')
def get_all_container_ports():
    return jsonify(cld.get_all_container_ports())

@admin.route('/provision_container', methods=['POST'])
def provision_container():
    req_json = request.get_json()
    image, port, volume, env_vars = request_image_mapper(req_json)
    cntr_id = cld.provision_container(image, port, volume, env_vars)

    return f'{cntr_id}'

@admin.route('/provide_db', methods=['POST'])
def provide_db():
    req_json = request.get_json()
    image, port, volume, env_vars = request_image_mapper(req_json)
    # check whether a new instance is required
    new = True if req_json['new'] == 'yes' else False
    if new:
        # provision container and return name, container, ports
        cntr_resp = cld.provision_container(image, port, volume, env_vars)
        resp_obj = cntr_resp
        resp_obj['port'] = handle_port_response(resp_obj['port'], port, False)
    else:
        query_name = req_json['distribution'] + '-' + req_json['instance'].zfill(2)
        container_query_result = cld.get_container(query_name)

        if bool(container_query_result['exists']):
            # check status
            if container_query_result['status'] == 'running':
                resp_obj = {
                    'name': container_query_result['name'],
                    'id': container_query_result['id'],
                    'port': handle_port_response(container_query_result['ports'], port, True)
                }
            elif container_query_result['status'] == 'exited':
                # pass the container id
                container_resp = cld.start_container(container_query_result['id'])
                # return the response object
                resp_obj = container_resp
                resp_obj['port'] = handle_port_response(resp_obj['port'], port, True)
            else:
                raise ValueError('Unknow container status')
        else:
            # provision newl container and return name, container, ports
            cntr_resp = cld.provision_container(image, port, volume, env_vars)
            resp_obj = cntr_resp
            resp_obj['port'] = handle_port_response(resp_obj['port'], port, False)

    return jsonify(resp_obj)

if __name__ == '__main__':
    admin.run(debug=True)