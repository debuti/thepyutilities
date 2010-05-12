#!/usr/bin/env bash
################################################################################
#  Author: <a href="mailto:debuti@gmail.com">Borja Garcia</a>
# Program: 
# Descrip: 
# Version: 0.0.0
#    Date: YYYY-MM-DD:HH:mm:SS
# License: This script doesn't require any license since it's not intended to be
#          redistributed. In such case, unless stated otherwise, the purpose of
#          the author is to follow GPLv3.
# Version: 0.0.0 (YYYY-MM-DD:HH:mm:SS)
#           - Initial release
################################################################################

# Parameters
DATE=`date +%Y%m%d`
LOG_PATH=""

# Constants


# Global variables
log="$LOG_PATH"
NAME=$1
VERSION=$2
    
# Error declaration


# Usage function

  function usage() {
    # Tell the user how to use me
    echo "$0 <libname> <libversion>"
  }
  

# Input validation function (getopts)

  function checkInput() {
    # Check input and store params in global variables to use them from main or call usage()
    if [ $# -ne 2 ]; then
      usage $0
      exit -1
    else
      NAME=$1
      VERSION=$2
    fi
  }

  
# Main function

  function main() {
    if [ ! -e `which 7z` ]; then
      echo "7zip needed"
      exit -1
    fi;

    mkdir dist 2>/dev/null
    cd src
    7z a -r ../dist/$NAME"-"$VERSION".zip" *.py
    cd ../dist
    rm $NAME".zip" 2> /dev/null
    ln -s $NAME"-"$VERSION".zip" $NAME".zip"
  }


# Entry point
  checkInput $@
  main

