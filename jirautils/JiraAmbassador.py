#!/usr/bin/env python3

# See: https://softwareengineering.stackexchange.com/questions/308972/python-file-naming-convention

from jira import JIRA
import re


class JiraAmbassador:
    """This class represent the Ambassador Pattern with the Jira functionality in such a way that the Ambassador
        provides extra functionality for its clients in a transparent way.
    """

    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__jira = self.__login(username,password,url)

    def __login(self, username, password, url):
        jira = JIRA(basic_auth=(username, password), options={'server': url})
        return jira

    def get_sprint_number(self, ticket):
        issue = self.__jira.issue(ticket)

        # custom field_10100 is the sprint field
        sprint_name = re.findall(r"name=[^,]*", str(issue.fields.customfield_10100[0]))
        words = str.split(sprint_name[0])

        # Sprint number is the last one (eg. Sprint 100)
        return words[len(words) - 1]

    def get_title(self, ticket):
        issue = self.__jira.issue(ticket)

        return issue.fields.summary