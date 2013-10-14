#import regexes and cmd inputs
import fileinput
import re
import sys

import Encoding

dictio = Encoding.PriorityDict()

#Makes segment object with 2 cmd line args
segment = Encoding.Encoder(3, "Input")
segment.segment() #Sets 



#segment.encode()
print(segment.raw)
print(segment.parsed)
print(segment.numbered)