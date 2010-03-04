#!/usr/bin/env python
###############################################################################################
#  Author:
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program:
_name = 'shellutils test'
# Descrip:
_description = '''Shell Utils Test'''
# Version:
_version = '0.0.1'
#    Date: 
_date = '2009-03-09:12:15:00'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 0.0.1 (2009-03-09:12:15:00)
#            -Initial release
###############################################################################################


import unittest
import sys
sys.path.append("..")
import shellutils

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        ''' This code is executed before each test
        '''
        ##Crea una secuencia de numeros en este objeto
        ##self.seq = range(10)
        #print "Hi setUp"

    def tearDown(self):
        ''' This code is executed after each test
        '''
        #print "Hi tearDown"

    def testfileExists(self):
        ''' Test for fileExists method
        '''
        #Types and variables for this test
        self.path = "delete.me" 
        
        # Set up parameters
        shellutils.rm(self.path)
        
        # Call software under test
        firstTest = shellutils.fileExists(self.path)
        
        # Set up parameters
        shellutils.touch(self.path)
        
        # Call software under test
        secondTest = shellutils.fileExists(self.path)
        
        # Verify results
        self.assert_(not firstTest and secondTest)
        
        # Clean up
        shellutils.rm(self.path)

    def testtouch(self):
        ''' Test for touch method
        '''
        #Types and variables for this test
        self.path = "delete.me" 
        
        # Set up parameters
        shellutils.rm(self.path)
        
        # Call software under test
        shellutils.touch(self.path)
        
        # Verify results
        self.assert_(shellutils.fileExists(self.path))


    def testrm(self):
        ''' Test for rm method
        '''
        #Types and variables for this test
        self.path = "delete.me"
        
        # Set up parameters
        shellutils.touch(self.path)
        
        # Call software under test
        firstTest = shellutils.rm(self.path)
        
        # Verify results
        self.assert_((firstTest == 0) and not shellutils.fileExists(self.path))

    def testexecutableExists(self):
        ''' Test for executableExists method
        '''
        #Types and variables for this test
        self.exists = "rm"
        self.notExists = "borjash"
        
        # Call software under test
        firstTest = shellutils.executableExists(self.exists)
        secondTest = shellutils.executableExists(self.notExists)
        
        # Verify results
        self.assert_(firstTest and not secondTest)

    def testgetSystemName(self):
        ''' Test for getSystemName method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.getSystemName()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash("uname -n"))

    def testpwd(self):
        ''' Test for pwd method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.pwd()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash("pwd"))

    def testls(self):
        ''' Test for ls method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.ls()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash("ls --almost-all").split("\n"))

if __name__ == '__main__':
    unittest.main()
    