#!/usr/bin/env python3

# https://pbpython.com/pathlib-intro.html
# https://realpython.com/python-pathlib/#creating-paths
# https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir

from pathlib import Path
import subprocess


class DirectoryManager:
    """This class represent an abstraction of the OS file system in order to make the code more readable.
    """

    def __init__(self, cwd):
        self.__cwd = Path(cwd)
        self.__tickets = self.__cwd.joinpath("Tickets")
        self.__sprints = self.__cwd.joinpath("Sprints")
        # Check that pwd exists and if not throw exception
        # Check that tickets and sprints exists and if not create them

    def create_ticket_folder_structure(self, ticket, sprint_number):
        ticket_path = self.__create_ticket_directory(ticket)
        notes_path = self.__create_notes_file(ticket_path, ticket)
        sprint_path = self.__create_sprint_directory(sprint_number)
        self.__create_symbolic_link(sprint_path, ticket, ticket_path)
        self.open_explorer_window(str(ticket_path))
        self.open_file_in_gedit(str(notes_path))

    def __create_ticket_directory(self, ticket):
        ticket_path = self.__tickets.joinpath(ticket)
        if not ticket_path.exists():
            # https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
            ticket_path.mkdir()

        return ticket_path

    def __create_notes_file(self, ticket_path, ticket):
        notes_name = DirectoryManager.get_notes_file_name(ticket)
        notes_path = ticket_path.joinpath(notes_name)
        if not notes_path.exists():
            notes_path.touch()
        return notes_path

    @staticmethod
    def get_notes_file_name(ticket):
        return "Notes_" + ticket + ".txt"

    def __create_sprint_directory(self, sprint_number):
        sprint_path = self.__sprints.joinpath(sprint_number)
        if not sprint_path.exists():
            sprint_path.mkdir()
        return sprint_path

    def __create_symbolic_link(self, sprint_path, ticket, ticket_path):
        link_path = sprint_path.joinpath(ticket)
        if not link_path.exists():
            link_path.symlink_to(ticket_path)
        return link_path

    # https://stackoverflow.com/questions/21518476/python-path-as-a-string
    def open_explorer_window(self, path):
        """
        Open the given path in  Nautilus
        :param path: The path to a directory as String.
        :return: The subprocess handler
        """
        # return subprocess.Popen(["xdg-open", path])
        return subprocess.Popen(["nautilus", path])

    # https://stackoverflow.com/questions/5990366/opening-file-from-python
    def open_file_in_gedit(self, file):
        """
        Open the given file in Gedit
        :param file: The path to the file as String.
        :return: The subprocess handler
        """
        return subprocess.Popen(['gedit', file])
