'''
Author: Zeta
Date: 2020-09-24 23:34:04
LastEditTime: 2020-09-24 23:55:12
'''
import re

reg = '<div id="(.*?)" class="row listw tc clearfix" linetype=".*?" state=".*?" trycount=".*?">'
pattern = re.compile(reg)

with open('./guid.html', 'r') as fd:
    r = pattern.findall(fd.read())
    print(r)
    print(len(r))