# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:22:41 2018

@author: lenovo
"""

import codecs
import os
import sys

option = []

for  name in ['0315']:
    option[0] = codecs.open('E:/Pycharm/log/data/2018'+ name +'/Option.csv')

print(option[0])
 