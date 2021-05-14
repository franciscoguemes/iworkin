#!/usr/bin/env bash
####################################################################################################
#Script Name	: I\ work\ in.sh
#Description	: Copy this script in any directory in the PATH of your OS so the "I work in" will be
#               available at any time in the system and it will use always the same configuration file.
#Args         :
#               $1 - The ticket number you are working on
#
#Author       : Francisco Güemes
#Email        : francisco@franciscoguemes.com
#See also	    :
#
####################################################################################################

# Configuration file
CONF_FILE=/home/$USER/.config/iworkin/iworkin.conf

# Directory where the project is located (Adapt accordingly to your computer)
PROJECT_DIR=/home/$USER/git/$USER/github/iworkin

$PROJECT_DIR/I\ work\ in.py --config=$CONF_FILE "$@"
