import json
import argparse


def read_config():
    with open("config/config.json") as config_file:
        data = json.load(config_file)

    config = argparse.Namespace()

    config.locker_app_ip = data["locker_app"]["ip"]
    config.locker_app_port = data["locker_app"]["port"]

    config.locker_service_ip = data["locker_service"]["ip"]
    config.locker_service_port = data["locker_service"]["port"]

    config.user_service_ip = data["user_service"]["ip"]
    config.user_service_port = data["user_service"]["port"]

    config.rabbitmq_username = data["rabbitmq"]["username"]
    config.rabbitmq_password = data["rabbitmq"]["password"]

    print(config)
    return config


if __name__ == '__main__':
    read_config()
