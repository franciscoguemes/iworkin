#!/usr/bin/env python3


from pathlib import Path
from mavenutils.PomParser import PomParser


class MavenProject:
    """This class represent an abstraction for interacting with maven projects.
    """

    def __init__(self, project_directory):
        self.__basedir = project_directory
        assert self.__basedir
        pom_files = self.get_pom_files()
        self.__parsers = MavenProject.__generate_pom_parsers(pom_files)

    def get_pom_files(self):
        files = []
        for filename in Path(self.__basedir).glob('**/pom.xml'):
            if "/target/" not in filename.__str__():
                files.append(filename)
        return files

    @staticmethod
    def __generate_pom_parsers(files):
        parsers = []
        for f in files:
            parsers.append(PomParser(f.absolute().__str__()))
        return parsers

    @staticmethod
    def generate_version_number(sprint_number):
        return "1." + str(sprint_number) + "-SNAPSHOT"

    def get_version_number(self):
        return self.__parsers[0].get_version()

    def change_version(self, version):
        for parser in self.__parsers:
            parser.print_path_to_pom_file()
            parser.set_version(version)

    def print_poms(self):
        for parser in self.__parsers:
            parser.print_path_to_pom_file()
            parser.print_pom()

    def store_changes(self):
        for parser in self.__parsers:
            parser.store_changes()
