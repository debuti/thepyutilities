#!/usr/bin/env python
###############################################################################################
#  Author:
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program:
_name = 'shellutils'
# Descrip:
_description = '''Library for common utilities.'''
# Version:
_version = '0.0.1'
#    Date: 
_date = '2009-03-09:12:15:00'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 0.0.1 (2009-03-09:12:15:00)
#            -Initial release
###############################################################################################

import subprocess
import os
import socket
import logging
import string
import sys
import re
import shutil
import stringutils


def fileExists(path):    
    '''This function returns if a file exists in current working directory
    '''

    return os.path.exists(path)

def rm(pathList):
    '''This function deletes a list of files
    '''

    try:
        if type(pathList).__name__!='list':
            pathList = [pathList]
        
        for file in pathList:
            os.remove(file)
            
        return 0

    except OSError as (errno, strerror):
        logging.error("OS error({0}): {1}: {2}".format(errno, strerror, file))
        return -1
    
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise

def touch(file_name):
    '''Touches the file
    '''

    f = open(file_name, "w")
    f.close()

def executableExists(execName):
    '''This function returns true if there is an executable like the parameter in the
       path (like unix which)
    '''

    assert not os.path.dirname(execName)

    extensions = os.environ.get("PATHEXT", "").split(os.pathsep)
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        base = os.path.join(directory, execName)
        options = [base] + [(base + ext) for ext in extensions]
        for filename in options:
            if os.path.exists(filename):
                return True
    return False


def mkdir(path):
    '''Makes a new directory or returns an error if its currently there
    '''

    os.mkdir(path)

def findNReplaceRegExp(file_name, regexp, replaceString, verbose=False, confirmationNeeded=False, surroundingLines = 1):
    '''Replaces the oldString with the replaceString in the file given,\
       returns the number of replaces
    '''
    # initialize local variables
    cregexp = re.compile(regexp, re.MULTILINE | re.DOTALL)
    somethingReplaced = True
    ocurrences = 0
    isAborted = False

    # open file for read
    file_in = open(file_name, 'r')
    file_in_string = file_in.read()
    file_in.close()

    while somethingReplaced:
        somethingReplaced = False
        # if the regexp is found
        if cregexp.search(file_in_string):
            # make the substitution
            replaced_text = re.sub(cregexp, replaceString, file_in_string, 1)
            if verbose == True:
                # calculate the segment of text in which the resolution will be done
                coincidence = cregexp.search(file_in_string)
                from_index = stringutils.extendedRFind(file_in_string, "\n", 0, coincidence.start(), surroundingLines + 1)
                to_index = stringutils.extendedFind(file_in_string, "\n", coincidence.end(), len(file_in_string), surroundingLines + 1)
                print_file_in_string = file_in_string[from_index:to_index]
                print_replaced_text = re.sub(cregexp, replaceString, print_file_in_string, 1)
                # print the old string and the new string
                print '- ' + print_file_in_string
                print '+ ' + print_replaced_text
                if confirmationNeeded:
                    # ask user if this should be done
                    question = raw_input('Accept changes? [Yes (Y), Abort (a)] ')
                    question = str.lower(question)
                    if question == 'a':
                        isAborted = True
                        print "Aborted"
                        break
                    else:
                        file_in_string = replaced_text
                        somethingReplaced = True
                        ocurrences = ocurrences + 1
            else:
                file_in_string = replaced_text
                somethingReplaced = True
                ocurrences = ocurrences + 1

    # if some text was replaced, overwrite the original file
    if ocurrences > 0 and not isAborted:
        # open the file for overwritting
        file_out = open(file_name, 'w')
        file_out.write(file_in_string)
        file_out.close()
        if verbose: print "File " + file_name + " written"

    return ocurrences

def findNReplace(file_name, oldString, replaceString, verbose=False, confirmationNeeded=False):
    '''Replaces the oldString with the replaceString in the file given,\
       returns the number of lines changed
    '''

    return findNReplaceRegExp(file_name, regexp, replaceString, verbose, confirmationNeeded)

def findNReplaceInFiles(file_name_list, oldString, replaceString, verbose=False, confirmationNeeded=False):
    '''Search and replace in all the files given, returns an array \
       with the number of times replaced in each file
    '''
    output = []
    if verbose == True: print '\nReplaced (verbose):\n'
    # loop on all files
    for file_name in file_name_list:
        print 'Processing: ' + file_name
        output.append(findNReplace(file_name, oldString, replaceString, verbose, confirmationNeeded))
    return output

def findNReplaceRegExpInFiles(file_name_list, regexp, replaceString, verbose=False, confirmationNeeded=False):
    '''Search and replace in all the files given, returns an array \
       with the number of times replaced in each file
    '''
    output = []
    if verbose == True: print '\nReplaced (verbose):\n'
    # loop on all files
    for file in file_name_list:
        print 'Processing: ' + file
        output.append(findNReplaceRegExp(file, regexp, replaceString, verbose, confirmationNeeded))
    return output

def runBash(cmd):
    '''This function takes Bash commands and returns them
    '''
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = process.stdout.read().strip()
    
    #This is the stdout from the shell command
    return out

def getSystemName():
    '''This function returns the name of the system (like uname -n)
    '''
    if socket.gethostname() is None:
        if os.getenv('HOSTNAME') is None:
            if os.getenv('COMPUTERNAME') is None:
                logging.error('Computer name not fetched')
                return None
    			
            else:
                return os.getenv('COMPUTERNAME')
    			
        else:
            return os.getenv('HOSTNAME')
    else:
        return socket.gethostname()

def cp(pathList, path):
    '''This function takes a list of files and directories and copies them to a destination
    '''
    try:
        if type(pathList).__name__!='list':
            pathList = [pathList]
        
        for file in pathList:
            shutil.copy(file, path)
            
        return 0

    except OSError as (errno, strerror):
        logging.error("OS error({0}): {1}: {2}".format(errno, strerror, file))
        return -1
    
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise

def mv(pathList, path): 
    '''This function takes a list of files and directories and moves them to a destination
    '''
    try:
        if type(pathList).__name__!='list':
            pathList = [pathList]
        
        for file in pathList:
            shutil.move(file, path)
            
        return 0

    except OSError as (errno, strerror):
        logging.error("OS error({0}): {1}: {2}".format(errno, strerror, file))
        return -1
    
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise
    
def pwd(): 
    '''This function returns the current working directory
    '''
    return os.getcwd()
    
def ls(path = pwd()): 
    '''This function returns a list of files and directories under the path passed as parameter
       NOTE: Do not include . and .. but it shows all hidden files
    '''
    return os.listdir(path)

def isDirEmpty(path, emptyOfFilesOnly = False):
    '''This function returns true if a directory is empty, accepts an argument that querys
       if its empty or empty of files (only directories inside)
	'''
    if (emptyOfFilesOnly == True):
        #TODO
	    pass
	
    else:
        if os.listdir(path) == []:
            return True
			
        else:
            return False

def rm_rf(pathList):
    '''This function deletes recursively a list of directories or files
    '''
    try:
        if type(pathList).__name__!='list':
            pathList = [pathList]
        
        for file in pathList:
            shutil.rmtree(file)            
            
        return 0

    except OSError as (errno, strerror):
        logging.error("OS error({0}): {1}: {2}".format(errno, strerror, file))
        return -1
    
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise

def getSystemVariable(name):
    '''This function returns the system variable or None if not found
    '''
    if os.getenv(name) is None:
        logging.error('Computer name not fetched')

    return os.getenv(name)

