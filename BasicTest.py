'''
Created on Sep 8, 2013

@author: Frank
'''
import Encoding

segment = Encoding.Encoder(3, "Input.txt")
segment.segment()
segment.write_results("Output.txt")

#bad_segment = Encoding.Encoder('a', "aklfda", "Output2")
#bad_segment.segment()
