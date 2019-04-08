# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:17:34 2018

@author: lenovo
"""

import codecs
import os
import sys


def ListFilesToTxt(dir, filelist, wildcard, recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        fullname = os.path.join(dir, name)
        if(os.path.isdir(fullname) & recursion):
            ListFilesToTxt(fullname, filelist, wildcard, recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    filelist.append(dir+"\\"+name)
                    #filelist.write(dir+name+"\n")
                    break

def GetAllFileList(mydir):
    global allFileList
    wildcard = ".log"
    ListFilesToTxt(mydir, allFileList, wildcard, 1)
    #print allFileList
