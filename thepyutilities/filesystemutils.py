#!/usr/bin/env python
###############################################################################################
#  Author:
__author__ = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program:
__name__ = 'filesystemutils'
# Descrip:
__description__ = '''Library for file system utilities.'''
# Version:
__version__ = '0.0.1'
#    Date:
__date__ = '2012-04-28'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History:
#          0.0.1 (2012-04-28)
#            -Initial release
###############################################################################################


def removeLine(filename, lineno):
    '''This function returns one line of a file and removes it
    '''
    fro = open(filename, "rb")

    current_line = 0
    while current_line < lineno:
        fro.readline()
        current_line += 1

    seekpoint = fro.tell()
    frw = open(filename, "r+b")
    frw.seek(seekpoint, 0)

    # read the line we want to discard
    readedLine = fro.readline()

    # now move the rest of the lines in the file
    # one line back
    chars = fro.readline()
    while chars:
        frw.writelines(chars)
        chars = fro.readline()

    fro.close()
    frw.truncate()
    frw.close()

    return readedLine
