__author__ = 'User'

import re

result = re.match('\d*', '123123sdfjsdfs1312sjdfiosdj1231231')
print "match:", result.group()

# result = re.findall('\d*', '123123sdf1312sj1231231')
# print "findall:", result
