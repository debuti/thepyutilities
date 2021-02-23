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
import sys, os
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "src")))
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
        
        
        # Call software under test
        shellutils.touch(self.path)
        
        # Verify results
        self.assert_(shellutils.fileExists(self.path))
        
        # Tear down parameters
        shellutils.rm(self.path)


    def testwrite(self):
        ''' Test for write method
        '''
        #Types and variables for this test
        self.path = "delete.me" 
        text = "this is a test"
        
        # Call software under test
        shellutils.write(self.path, text)
        
        # Verify results
        self.assertEqual(shellutils.cat(self.path), text)
        
        # Tear down parameters
        shellutils.rm(self.path)


    def testappend(self):
        ''' Test for append method
        '''
        #Types and variables for this test
        self.path = "delete.me" 
        text = "this is a test"
        appendedText = "This is another test"

        # Set up parameters
        shellutils.write(self.path, text)
        
        # Call software under test
        shellutils.append(self.path, appendedText)
        
        # Verify results
        self.assertEqual(shellutils.cat(self.path), text + appendedText)
        
        # Tear down parameters
        shellutils.rm(self.path)


    def testcat(self):
        ''' Test for cat method
        '''
        #Types and variables for this test
        self.path = "delete.me" 
        text = "this is a test"

        # Set up parameters
        shellutils.write(self.path, text)
        
        # Call software under test
        result = shellutils.cat(self.path)
        
        # Verify results
        self.assertEqual(result, text)
        
        # Tear down parameters
        shellutils.rm(self.path)


    def testisDriveConnected(self):
        ''' Test for isDriveConnected method
        '''
         # Call software under test
        result = shellutils.isDriveConnected("naranjito")
        
        # Verify results
        self.assertTrue(result)
        
         # Call software under test
        result = shellutils.isDriveConnected("emulatron")
        
        # Verify results
        self.assertTrue(not result)


    def testrm(self):
        ''' Test for rm method
        '''
        #Types and variables for this test
        self.path = os.path.realpath(os.path.join(os.path.dirname(__file__), "delete.me"))
        
        # Set up parameters
        shellutils.touch(self.path)
        
        # Call software under test
        firstTest = shellutils.rm(self.path)
        
        # Verify results
        self.assert_((firstTest == 0) and not shellutils.fileExists(self.path))

        #Types and variables for this test
        myfile = "delete.me"
        mydirectory = "hello"
        
        # Set up parameters
        shellutils.mkdir(mydirectory)
        shellutils.touch(os.path.join(mydirectory, myfile))
        
        # Call software under test
        secondTest = shellutils.rm(mydirectory, recurse = True)
        
        # Verify results
        self.assert_((secondTest == 0) and not shellutils.fileExists(self.path))


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
        self.assertEqual(firstTest, shellutils.runBash(["uname", "-n"]).split("\n")[0])


    def testpwd(self):
        ''' Test for pwd method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.pwd()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash(["pwd"]).split("\n")[0])


    def testls(self):
        ''' Test for ls method
        '''
        #Skipping this test because of incompatibilities of unixls
        return 0

        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.ls()
        
        # Verify results
        self.assertEqual(set(firstTest), set(shellutils.runBash(["ls", "--almost-all"]).split("\n")[:-1]))

        # Types and variables for this test
        file1 = "thisisatest"
        
        # Set up parameters
        if not shellutils.exists(file1):
            shellutils.mkdir(file1)
            
        if not shellutils.exists(os.path.join(file1, file1)):
            shellutils.mkdir(os.path.join(file1, file1))
        
        # Call software under test
        secondTest = shellutils.ls(recurse=True)
        
        # Verify results
        self.assertEqual(set(secondTest), set(shellutils.runBash(["find", ".", "-exec", "basename", "{}", ";"]).split("\n")[1:-1]))

        # Call software under test
        thirdTest = shellutils.ls(fullPath=True, recurse=True)
        
        # Verify results
        expectedValue = set(shellutils.runBash(["find", ".", "-exec", "readlink", "-f", "{}", ";"]).split("\n")[1:-1])
        self.assertEqual(set(thirdTest), expectedValue)

        # Tear down parameters
        shellutils.rm(file1, recurse = True)


    def testmv(self): #TODO
        ''' Test for mv method
            # Steps:
             1.- mv one file to an unknown location (absolute and relative path)
             2.- mv one dir to an unknown location (absolute and relative path)
             3.- mv several files to an unknown location
             4.- mv one file to a file (absolute and relative path)
             5.- mv one dir to a file
             6.- mv several files and folders to a file
             7.- mv one file to a dir (absolute and relative path)
             8.- mv a dir to a dir (absolute and relative path)
             9.- mv several files and folder to a dir (absolute and relative path)
        '''
        # 1.- mv one file to an unknown location (absolute and relative path)
        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.touch(oldname)
        
        # Call software under test
        shellutils.mv(oldname, os.path.join(shellutils.pwd(), newname))
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())

        # Tear down parameters
        shellutils.rm(newname, recurse = True)

        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.touch(oldname)
        
        # Call software under test
        shellutils.mv(oldname, newname)
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())

        # Tear down parameters
        shellutils.rm(newname, recurse = True)


        # 2.- mv one dir to an unknown location (absolute and relative path)
        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.mkdir(oldname)
        
        # Call software under test
        shellutils.mv(oldname, os.path.join(shellutils.pwd(), newname))
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())

        # Tear down parameters
        shellutils.rm(newname, recurse = True)

        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.mkdir(oldname)
        
        # Call software under test
        shellutils.mv(oldname, newname)
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())

        # Tear down parameters
        shellutils.rm(newname, recurse = True)


        # 3.- mv several files to an unknown location
        # Types and variables for this test
        oldnames = ["test.deleteme", "test2.deleteme", "test3.deleteme"]
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        for oldname in oldnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
            shellutils.touch(oldname)
            
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        
        beforeLs = shellutils.ls()
        # Call software under test
        print
        print "This error is expected"
        exitValue = shellutils.mv(oldnames, newname)
        
        # Verify results
        afterLs = shellutils.ls()
        self.assertTrue(beforeLs == afterLs and exitValue != 0)

        # Tear down parameters
        for oldname in oldnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)


        # 4.- mv one file to a file (absolute and relative path)
        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.write(oldname, "oldname")
        shellutils.write(newname, "newname")
        
        # Call software under test
        shellutils.mv(oldname, os.path.join(shellutils.pwd(), newname))
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())
        self.assertEqual(shellutils.cat(newname), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)

        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.write(oldname, "oldname")
        shellutils.write(newname, "newname")
             
        # Call software under test
        shellutils.mv(oldname, newname)
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and newname in shellutils.ls())
        self.assertEqual(shellutils.cat(newname), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)
     
     
        #  5.- mv one dir to a file
        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.mkdir(oldname)
        shellutils.touch(newname)
        
        beforeLs = shellutils.ls()
        # Call software under test
        print
        print "This error is expected"
        exitValue = shellutils.mv(oldname, newname)
        
        # Verify results
        afterLs = shellutils.ls()
        self.assertTrue(beforeLs == afterLs and exitValue != 0)

        # Tear down parameters
        shellutils.rm(oldname, recurse = True)     
        shellutils.rm(newname, recurse = True)     
                
                
        # 6.- mv several files and folders to a file
        # Types and variables for this test
        oldnames = ["test.deleteme", "test2.deleteme", "test3.deleteme"]
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        for oldname in oldnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
            shellutils.touch(oldname)
            
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        shellutils.touch(newname)
        
        beforeLs = shellutils.ls()
        # Call software under test
        print
        print "This error is expected"
        exitValue = shellutils.mv(oldnames, newname)
        
        # Verify results
        afterLs = shellutils.ls()
        self.assertTrue(beforeLs == afterLs and exitValue != 0)

        # Tear down parameters
        for oldname in oldnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
        shellutils.rm(newname)


        # 7.- mv one file to a dir (absolute and relative path)
        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.write(oldname, "oldname")
        shellutils.mkdir(newname)
        
        # Call software under test
        shellutils.mv(oldname, os.path.join(shellutils.pwd(), newname))
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and oldname in shellutils.ls(newname))
        self.assertEqual(shellutils.cat(os.path.join(newname, oldname)), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)

        # Types and variables for this test
        oldname = "test.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.write(oldname, "oldname")
        shellutils.mkdir(newname)
             
        # Call software under test
        shellutils.mv(oldname, newname)
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and oldname in shellutils.ls(newname))
        self.assertEqual(shellutils.cat(os.path.join(newname, oldname)), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)
        
        
        # 8.- mv a dir to a dir (absolute and relative path)
        # Types and variables for this test
        oldname = "test.deleteme"
        oldnameinside = "anothertest.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldnameinside):
            shellutils.rm(oldnameinside, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.mkdir(oldname)
        shellutils.write(os.path.join(oldname, oldnameinside), "oldname")
        shellutils.mkdir(newname)
        
        # Call software under test
        shellutils.mv(oldname, os.path.join(shellutils.pwd(), newname))
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and oldname in shellutils.ls(newname))
        self.assertEqual(shellutils.cat(os.path.join(newname, oldname, oldnameinside)), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)

        # Types and variables for this test
        oldname = "test.deleteme"
        oldnameinside = "anothertest.deleteme"
        newname = "NEWtest.deleteme"
        
        # Set up parameters
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        if shellutils.exists(oldnameinside):
            shellutils.rm(oldnameinside, recurse = True)
        if shellutils.exists(oldname):
            shellutils.rm(oldname, recurse = True)
        shellutils.mkdir(oldname)
        shellutils.write(os.path.join(oldname, oldnameinside), "oldname")
        shellutils.mkdir(newname)
             
        # Call software under test
        shellutils.mv(oldname, newname)
        
        # Verify results
        self.assertTrue(oldname not in shellutils.ls() and oldname in shellutils.ls(newname))
        self.assertEqual(shellutils.cat(os.path.join(newname, oldname, oldnameinside)), "oldname")

        # Tear down parameters
        shellutils.rm(newname, recurse = True)
        
        
        # 9.- mv several files and folder to a dir (absolute and relative path)
        # Types and variables for this test
        olddirnames = ["a", os.path.join("a", "b"), os.path.join("a", "b" ,"c"), os.path.join("a", "f")]
        oldfilenames = [os.path.join("a","1"), os.path.join("a","2"), os.path.join("a", "3"), os.path.join("a", "b", "4"), os.path.join("a", "b", "5"),  os.path.join("a",  "b", "6"),  os.path.join("a", "b", "c", "7") , os.path.join("a", "b", "c", "8"), os.path.join("a", "b", "c", "9") , os.path.join("a", "e")]
        newname = "NEWdirectory"
        
        # Set up parameters
        for oldname in olddirnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
            shellutils.mkdir(oldname)
        for oldname in oldfilenames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
            shellutils.write(oldname, oldname)
            
        if shellutils.exists(newname):
            shellutils.rm(newname, recurse = True)
        shellutils.mkdir(newname)
        
        beforeLs = shellutils.ls()
        # Call software under test
        exitValue = shellutils.mv("a", newname)
        
        # Verify results
        afterLs = shellutils.ls()
        afterLs2 = shellutils.ls(newname)
        self.assertTrue(exitValue == 0)
        self.assertTrue("a" in beforeLs and "a"  not in afterLs and "a" in afterLs2)

        # Tear down parameters
        for oldname in olddirnames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
        for oldname in oldfilenames:
            if shellutils.exists(oldname):
                shellutils.rm(oldname, recurse = True)
        shellutils.rm(newname, recurse = True)

             
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=3).run(suite)

    
