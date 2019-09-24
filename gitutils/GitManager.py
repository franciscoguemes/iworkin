#!/usr/bin/env python3


# https://gitpython.readthedocs.io/en/stable/tutorial.html#meet-the-repo-type
# https://stackoverflow.com/questions/47872070/how-to-check-out-a-branch-with-gitpython
# https://stackoverflow.com/questions/37845888/use-gitpython-to-checkout-a-new-branch-and-push-to-remote
# https://stackoverflow.com/questions/2473035/checkout-or-list-remote-branches-in-gitpython
# https://gist.github.com/igniteflow/1760854


from git import Repo
from mavenutils.MavenProject import MavenProject
import re


class GitManager:
    """This class represent an abstraction of the git source control in order to make the code more readable.
    """
    def __init__(self, repository_directory):
        self.__repository_directory = repository_directory
        assert self.__repository_directory
        self.__repo = Repo(repository_directory)
        assert not self.__repo.bare

    def is_repo_dirty(self):
        return self.__repo.is_dirty()

    def get_untracked_files(self):
        return self.__repo.index.diff(None)

    def get_staged_files(self):
        return self.__repo.index.diff("HEAD")

    def __get_active_branch(self):
        return self.__repo.active_branch

    def get_active_branch_name(self):
        branch = self.__get_active_branch()
        return branch.name

    def change_to_sprint_branch(self, sprint_number):
        branch_name = GitManager.get_sprint_branch_name(sprint_number)
        if not self.__exists_branch(branch_name):
            # TODO: The sprint branch does not exists, that means is the first ticket in the new sprint therefore the
            #  docker image for the new sprint must be created...
            branch = self.__create_branch(branch_name)

            # Change here the version numbers in the pom.xml files
            mp = MavenProject(self.__repository_directory)
            version = mp.generate_version_number(sprint_number)
            mp.change_version(version)
            mp.store_changes()

            # Stage changes
            self.__repo.git.add(update=True)

            # Commit changes
            comment = "Change version numbers in pom.xml files for version " + str(sprint_number)
            self.__repo.index.commit(comment)

            # Push changes...
            self.push()
        else:
            branch = self._get_branch(branch_name)
            self.pull()

    def change_to_ticket_branch(self, ticket, ticket_title):
        branch_name = GitManager.get_ticket_branch_name(ticket,ticket_title)
        if not self.__exists_branch(branch_name):
            # branch = self.__repo.git.checkout('-b', branch_name)
            branch = self.__create_branch(branch_name)
            # self.__push(branch)
            self.__repo.git.push("origin", branch)
        else:
            branch = self._get_branch(branch_name)
            # TODO: Before doing a pull check that the branch exists in the remote repository
            self.pull()

    @staticmethod
    def get_sprint_branch_name(sprint_number):
        return "dev/sprint" + sprint_number

    @staticmethod
    def get_ticket_branch_name(ticket, ticket_title):
        title = GitManager.format_branch_name(ticket_title)
        return ticket + "_" + ticket_title.replace(" ", "_")

    @staticmethod
    def format_branch_name(branch_name):
        # TODO: Do this with regex and handle all these cases: https://stackoverflow.com/a/3651867

        # Replaces spaces by underscores
        formatted_name = branch_name.replace(" ", "_")

        # Replaces two consecutive dots by one single dot
        formatted_name = re.sub('\\.\\.', '', formatted_name)

        # Replaces a dot at the end of the branch_name
        # --> https://stackoverflow.com/questions/3675318/how-to-replace-the-some-characters-from-the-end-of-a-string
        formatted_name = re.sub('\\.$', '', formatted_name)

        return formatted_name;

    def __exists_branch(self, branch_name):
        exists = False
        heads = self.__repo.heads
        if branch_name in heads:
            exists = True
        return exists

    def __create_branch(self, branch_name):
        print(f"Creating branch: {branch_name}")
        branch = self.__repo.create_head(path=branch_name, commit='HEAD', force=False)
        branch.checkout()
        return branch

    def _get_branch(self, branch_name):
        return self.__repo.git.checkout(branch_name)

    def pull(self):
        branch = self.__get_active_branch()
        self.__pull(branch)

    def __pull(self, branch):
        self.__repo.git.pull('origin', branch)

    def push(self):
        branch = self.__get_active_branch()
        self.__push(branch)

    def __push(self, branch):
        self.__repo.git.push('--set-upstream', 'origin', branch)
