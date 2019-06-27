# https://github.com/docker/docker-py
# https://github.com/docker/docker-py/blob/master/README.md
# https://docker-py.readthedocs.io/en/stable/containers.html
# https://stackoverflow.com/questions/47433576/starting-docker-container-using-python-script/47433716

# Stop the running dockerutils container
# Check which containers exists
# Take the image from the current sprint
# Run a container from the image of the current sprint --> Ticket container
# Inside the ticket container:
#   1- Start MySQL
#   2- Run the Flyway to run the corresponding migration scripts



#
# /***********************************************************************************/
# Recreate dockerutils container BAC-146:   	(from image: mysql/enterpriseschema --> 0.100)
# 	sudo dockerutils run --name BAC-146 -it -v ~/.m2:/root/.m2/ -p 3306:3306 58741c1b4dc4 /bin/bash
#
# /***********************************************************************************/
# Start the MySQL server:
# 	service mysql start
#
# /***********************************************************************************/
# Baseline with version 101:
# 	flyway -baselineVersion=101 baseline
#
# /***********************************************************************************/
# Build the latest version of backoffice-persistence:
# 	cd ~/git/Uniscon/backoffice-aggregator/backoffice-sealed-cloud/backoffice-persistence
# 	mvn clean install -DskipTests
#
# /***********************************************************************************/
#
# flyway info -locations=classpath:db.migration.prod -jarDirs=/home/francisco/git/Uniscon/backoffice-aggregator/backoffice-sealed-cloud/backoffice-persistence/target
#
# /***********************************************************************************/
#
# flyway migrate -locations=classpath:db.migration.prod -jarDirs=/home/francisco/git/Uniscon/backoffice-aggregator/backoffice-sealed-cloud/backoffice-persistence/target