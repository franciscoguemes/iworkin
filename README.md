This project is the basis for the "I work in" methodology which will help you automate
all those tedious operations we do when we develop in a project such as:
    Get the ticket information from JIRA
    Commit your current changes
    Change to the ticket branch
    Create a spring branch if necessary
    Update the version number in the pom.xml files and commit those changes in the sprint branch.
    Create a directory and a notes file for the ticket in your personal notes directory
    And many more...

The application must be call in the form:
    $> I\ work\ in.py [--config=/path/to/the/config/file] TICKET
    
If no configuration file is supplied then the application expects to have a file called 
iworkin.conf in the installation directory.
Please have a look to the supplied file iworkin.conf.example to find out which parameters
does the application expect to find. 


TODO:
    Add proper error handling through exceptions
    
    
Error cases to handle gracefully:
    The user inputs a ticket that do not exists
        Wrong ticket prefix
        Wrong ticket number
    The user decides to work in a ticket that is not assigned to any sprint
    