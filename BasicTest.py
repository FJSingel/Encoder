#import regexes and cmd inputs
import fileinput
import re
import sys

import Encoding

dictio = Encoding.PriorityDict()

#Makes segment object with 2 cmd line args
segment = Encoding.Encoder(3, "Input", "Output")
segment.segment() #Sets