#import regexes and cmd inputs
import re

import Encoding

segment = Encoding.Encoder(3, "Input", "Output")
segment.segment()

bad_segment = Encoding.Encoder('a', "aklfda", "Output2")
bad_segment.segment()