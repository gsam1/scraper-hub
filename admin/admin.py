from flask import Flask
from flask import jsonify
from clients import ClientDocker
from config import admin_config

ENV = 'development'
admin = Flask(__name__)
config = admin_config[ENV]()
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


if __name__ == '__main__':
    admin.run(debug=True)