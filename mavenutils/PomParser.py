#!/usr/bin/env python3

# https://docs.python.org/2/library/xml.dom.minidom.html
# https://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python
# https://stackoverflow.com/questions/2502758/update-element-values-using-xml-dom-minidom

from xml.dom import minidom


class PomParser:
    """This class contains functionality for interacting with pom.xml maven files.
    """

    def __init__(self, file_path):
        self.__file_path = file_path
        assert self.__file_path
        #print(self.__file_path)
        self.__xml_doc = minidom.parse(self.__file_path)

    def __get_version_item(self):
        item_list = self.__xml_doc.getElementsByTagName('version')
        return PomParser.__get_project_version_item(item_list)

    @staticmethod
    def __get_project_version_item(item_list):
        """
        In the pom file there are multiple version elements, but we are only interested in the one that set the version
        number of the project which is the one that is direct child of the project element, or in the case of a subproject,
        the version element that is a child of the element parent.

        Take into account that in an XML file, it does not matter the order of appearance of the elements. So the version
        element could be anywhere in the file, not necessarily at the beginning.

        :param item_list: A list of xml.dom.minidom elements tagged as version
        :return: The version element that represents the version number of the project.
        """
        version_item = None
        for version_node in item_list:
            parent_node = version_node.parentNode
            if parent_node.nodeName == "project":
                version_item = version_node
                break

        if version_item is None: # This means is a subproject
            for version_node in item_list:
                parent_node = version_node.parentNode
                if parent_node.nodeName == "parent":
                    version_item = version_node
                    break

        return version_item

    def get_version(self):
        item = self.__get_version_item()
        return item.firstChild.data

    def set_version(self, version):
        item = self.__get_version_item()
        item.firstChild.data = version

    def print_path_to_pom_file(self):
        print(self.__file_path)

    def print_pom(self):
        print(self.__xml_doc.toxml())

    def store_changes(self):
        file_handle = open(self.__file_path, "wt")
        #file_handle.write(self.__xml_doc.toxml())
        self.__xml_doc.writexml(file_handle)
        file_handle.close()

