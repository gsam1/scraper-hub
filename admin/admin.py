from flask import Flask
from clients import ClientDocker
from config import admin_config

ENV = 'development'
admin = Flask(__name__)

@admin.route('/')
def index():
    return 'Hello World!'

@admin.route('/get_all_containers')
def get_all_containers():
    config = admin_config[ENV]()
    cld = ClientDocker(config.docker_url)
    containers_list = str(cld.get_all_containers())
    return containers_list


if __name__ == '__main__':
    admin.run(debug=True)