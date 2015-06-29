__author__ = 'User'

import re

#match 1 continuous number
def tc1():
    result = re.match('\d*', '123123sdfjsdfs1312sjdfiosdj1231231')
    print "match:", result.group()

#find all numbers
def tc2():
    result = re.findall('\d*', '123123sdf1312sj1231231')
    print "findall:", result

#find all words
def tc3():
    str = ('name            time             size\n'
           'file1           2015             10086\n'
           'file1           2015             10086\n')
    result = re.findall('\w*', str)
    print "match:", result

if __name__ == "__main__":
    tc3()