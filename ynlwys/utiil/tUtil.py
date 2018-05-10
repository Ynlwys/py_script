#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    author：Ynlwys


功能介绍：
    用于测试 基本语法
"""

# import time

# print "hello world";

# print time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()));

import xlrd;
import xlwt;
import datetime;
import  time;
import sys
import random
import re


name = re.sub("-|[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]","","张张2017-12-01");

print name;