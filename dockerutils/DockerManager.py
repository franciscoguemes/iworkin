#!/usr/bin/env python3

# https://github.com/docker/docker-py
# https://github.com/docker/docker-py/blob/master/README.md
# https://docker-py.readthedocs.io/en/stable/containers.html
# https://stackoverflow.com/questions/47433576/starting-docker-container-using-python-script/47433716

import docker


class DockerManager:
    """

    """
    def __init__(self, ticket, sprint_number):
        self.__client = docker.from_env()
        self.__ticket = ticket
        self.__sprint_number = sprint_number


    def list_containers(self):
        return  self.__client.containers.list()

