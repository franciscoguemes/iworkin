#!/usr/bin/env python3

# .I\ work\ in.py BAC-146

import sys
import configparser
from pathlib import Path

import io
import os
import subprocess

from jirautils.JiraAmbassador import JiraAmbassador
from linux.DirectoryManager import DirectoryManager
from gitutils.GitManager import GitManager
from dockerutils.DockerManager import DockerManager

DEFAULT_CONFIG_FILE = "iworkin.conf"


def process_arguments(args):
    """
        This method expects to receive the arguments of the application in the format.
            I\ work\ in.py [--config=/path/to/the/config/file] TICKET
        Note that the configuration file is optional.
    :param args: The command line arguments.
    :return: A map containing all parameters that the application needs to run.
    """

    msg = """Please provide the arguments in the following way: 
            $> I\ work\ in.py [--config=/path/to/the/config/file] TICKET
            """

    # A dictionary for holding the arguments once they are processed
    parameters = {
        "ticket": "",
        "config_file": ""
    }

    if len(args) == 2:
        parameters["ticket"] = args[1]
        parameters["config_file"] = DEFAULT_CONFIG_FILE
    elif len(args) == 3:
        args.__delitem__(0)
        for arg in args:
            #print(f"Processing arg {arg} ...")
            chunks = str.split(arg, "=")
            if len(chunks)==1:
                parameters["ticket"] = arg
            elif len(chunks)==2:
                if str.lower(chunks[0]) == "--config":
                    parameters["config_file"] = chunks[1]
                else:
                    sys.exit(msg)
            else:
                sys.exit(msg)
    else:
        sys.exit(msg)

    return parameters


def check_config(config):
    if 'JIRA' not in config:
        msg = "The configuration file must have a section called [JIRA]." + "\n "
        msg += """Please have a look at the documentation of the project and edit the config file in the pertinent way.
        More info about config files on: https://docs.python.org/3/library/configparser.html
        """
        sys.exit(msg)
    if 'LOCAL' not in config:
        msg = "The configuration file must have a section called [LOCAL]." + "\n "
        msg += """Please have a look at the documentation of the project and edit the config file in the pertinent way.
        More info about config files on: https://docs.python.org/3/library/configparser.html
        """
        sys.exit(msg)
    #TODO: Check the resto of the configuration parameters here...

def check_ticket_nomenclature(jira_project_prefix, ticket_name):
    """
        Check that the ticket belongs to the configured project. It checks that the ticket name contains the
        ticket prefix for the given project.
    :param jira_project_prefix: The prefix that the tickets who belongs to the same project has in Jira.
    :param ticket_name: The full name of the ticket (Including prefix).
    :return: Nothing in case of the ticket belongs to the configured project.
    """
    if jira_project_prefix not in ticket_name:
        msg = "The given ticket does not contain the configured project prefix: " + jira_project_prefix + "\n"
        msg += """Please provide the arguments in the following way:
        $> I\ work\ in.py [--config=/path/to/the/config/file] TICKET
        """
        sys.exit(msg)


def create_directories(ticket, sprint_number, personal_notes_path):
    dm = DirectoryManager(personal_notes_path)
    dm.create_ticket_folder_structure(ticket, sprint_number)


def handle_braches(ticket, ticket_title, sprint_number, project_base_dir):
    gm = GitManager(project_base_dir)
    if gm.is_repo_dirty():
        # TODO: Print proper error message...
        print("Non commited files: ")
        print(gm.get_non_commited_files())
        return False

    active_branch = gm.get_active_branch_name()
    print(f"Active branch: {active_branch}")
    branch_name = GitManager.get_ticket_branch_name(ticket, ticket_title)
    if active_branch != branch_name:
        gm.change_to_sprint_branch(sprint_number)
        print(f"Active branch: {gm.get_active_branch_name()}")
        gm.change_to_ticket_branch(ticket, ticket_title)
        print(f"Active branch: {gm.get_active_branch_name()}")


def start_docker_container(ticket,sprint_number):
    dm = DockerManager(ticket, sprint_number)
    # List the containers...
    print(dm.list_containers())


# TODO: Handle error and corner cases...
def main():
    parameters = process_arguments(sys.argv)

    ticket = parameters["ticket"]
    config_file = parameters["config_file"]

    # print(f"The ticket is: {ticket}")
    # print(f"The config file is: {config_file}")

    #Check if the config file exists...
    cfile = Path(config_file)
    if not cfile.is_file():
        msg = "The configuration file: " + config_file + " does not exists. Please read the app documentation and fix the issue."
        sys.exit(msg)

    config = configparser.ConfigParser()
    config.read(config_file)
    check_config(config)

    jira_url = config['JIRA']['JIRA_URL']
    jira_user = config['JIRA']['JIRA_USER']
    jira_password = config['JIRA']['JIRA_PASSWORD']
    jira_project_prefix = config['JIRA']['JIRA_PROJECT_PREFIX']

    personal_notes_path = config['LOCAL']['PERSONAL_NOTES_PATH']
    project_base_dir = config['LOCAL']['PROJECT_BASE_DIR']

    # print(f"jira_url = {jira_url}")
    # print(f"jira_user = {jira_user}")
    # print(f"jira_password = {jira_password}")
    # print(f"jira_project_prefix = {jira_project_prefix}")
    #
    # print(f"personal_notes_path = {personal_notes_path}")
    # print(f"project_base_dir = {project_base_dir}")

    check_ticket_nomenclature(jira_project_prefix, ticket)

    ja = JiraAmbassador(jira_url, jira_user, jira_password)

    sprint_number = ja.get_sprint_number(ticket)
    ticket_title = ja.get_title(ticket)

    print(f"The Sprint number is: {sprint_number}")
    print(f"The Ticket title  is: {ticket_title}")

    create_directories(ticket, sprint_number, personal_notes_path)
    handle_braches(ticket, ticket_title, sprint_number, project_base_dir)
    # start_docker_container(ticket, sprint_number)



main()




######################################################################
#
# UC-1: I start working in a new task
#
# The user decides to invoke the app by calling the script and specify
# the ticket number he is working at.
#
# Expected output:
#	1.1- The app will create the support directories and files
#		1.1.1- Create the ticket directory
#		1.1.2- Create the notes file
#		1.1.3- Create the sprint directory (if it does not exist)
#		1.1.4- Create the link to the ticket directory in the sprint directory
#	1.2- The app will open a new browser window with the ticket number
#	1.3- The app will switch to the sprint branch (i.e. dev/sprint100)
#	     If the branch does not exist, it will create it and switch to it.
#	     1.3.1- In the new branch it will update the pom numbers to the new version
#	     1.3.2- It will commit and push the change with the comment "Update the pom numbers".
#	1.3- The app will generate a new branch for the new task and switch to it.
#
########################################################################

######################################################################
#
# UC-2: The user wants to continue working in a task he was working previously
#
# The user decides to invoque the app by calling the script and specify
# the ticket number he is working at.
#
# Expected output:
#	+ The app will open the support directories and files
#	+ The app will open a new browser window with the ticket number
#	+ The app will switch to the existing branch for the new task.
#
########################################################################











# # 1.1.1- Create the ticket folder
# TICKET_DIR=$TICKETS_PATH/$1
# mkdir $TICKET_DIR
# # 1.1.2- Create the notes file
# touch $TICKET_DIR/$NOTES_FILE
#
# #TODO: Autodetect Sprint from ticket number...
# SPRINT_NUM=100
#
# #TODO: Detect if sprint folder exists...
#
# #1.1.3- Create the sprint directory
# SPRINT_DIR=$SPRINT_PATH/$SPRINT_NUM
#
# #1.1.4- Create the link to the ticket directory in the sprint directory
# ln -s $TICKET_DIR $SPRINT_DIR/$1
#
#
# #1.2- Open a new browser window with the ticket number
# THIRD_MONITOR_LEFT_UPPER_CORNER_XPS=3900,0
# CHROMIUM_PROFILE_UNISCON=Profile\ 1
# JIRA_BASE_TICKET_URL=https://jira.uniscon-rnd.de/browse
# TICKET_URL=$JIRA_BASE_TICKET_URL/$1
#
# chromium --window-position=$THIRD_MONITOR_LEFT_UPPER_CORNER_XPS --profile-directory="$CHROMIUM_PROFILE_UNISCON" --new-window \
# 		$TICKET_URL &
#
# #1.3- The app will generate a new branch for the new task and switch to it.
# cd $PROJECT_BASE_DIR
# SPRINT_BRANCH_NAME=dev/sprint$SPRINT_NUM
# #TODO: Get the ticket title from the ticket  and replace empty spaces by underscores
# TICKET_TITLE=Bla_bla_bla
# TICKET_BRANCH_NAME=$1_$TICKET_TITLE
# gitutils pull
# gitutils checkout $SPRINT_BRANCH_NAME
# gitutils pull
# gitutils checkout -b $TICKET_BRANCH_NAME
# #gitutils push origin $TICKET_BRANCH_NAME
