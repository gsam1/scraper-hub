from flask import Flask, request
from flask import jsonify
from clients import ClientDocker
from config import admin_config

ENV = 'development'
admin = Flask(__name__)
config = admin_config[ENV]()
image_map = config.image_map
cld = ClientDocker(config.docker_url)

@admin.route('/')
def index():
    return 'Hello World!'

@admin.route('/get_all_containers')
def get_all_containers():
    # containers_list = str(cld.get_all_containers())
    return jsonify(cld.get_all_containers())

@admin.route('/get_active_containers')
def get_active_containers():
    # containers_list = str(cld.get_active_containers())
    return jsonify(cld.get_active_containers())

@admin.route('/get_active_container_ports')
def get_active_container_ports():
    return jsonify(cld.get_active_container_ports())

@admin.route('/get_all_container_ports')
def get_all_container_ports():
    return jsonify(cld.get_all_container_ports())

@admin.route('/run_container', methods=['POST'])
def run_container():
    req_json = request.get_json()
    image = image_map[req_json['type']][req_json['distribution']]['image']
    port = image_map[req_json['type']][req_json['distribution']]['default_port']
    volume = image_map[req_json['type']][req_json['distribution']]['data_location']
    env_vars = image_map[req_json['type']][req_json['distribution']]['env_vars']
    cntr_id = cld.run_container(image, port, volume, env_vars)
    
    return f'{cntr_id}'

if __name__ == '__main__':
    admin.run(debug=True)