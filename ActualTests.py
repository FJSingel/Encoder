'''
Created on Sep 8, 2013

@author: Frank
'''
import os

from testify import *

import Encoding #the mazes class I made



class DefaultInput(TestCase):
	"""
	Tests the input given in the assignment
	"""
	
	@class_setup
    def setUp(self):
    	os.remove("./Output1.txt")

    def test_regular_use(self):
    	segment = Encoding.Encoder(3, "Input1.txt")
		segment.segment()
		segment.write_results("Output1.txt")

	def test_decimal_length(self):
		segment = Encoding.Encoder(3.5, "Input1.txt")
		segment.segment()
		segment.write_results("Output1.txt")

	def test_long_length(self):
		segment = Encoding.Encoder(35, "Input1.txt")
		segment.segment()
		segment.write_results("Output1.txt")

    def test_invalid_length(self):
    	assert_raises(ValueError, Encoding.Encoder, -3, "Input1.txt")
    	assert_raises(ValueError, Encoding.Encoder, 'a', "Input1.txt")

    def test_invalid_file(self):
    	assert_raises(IOError, Encoding.Encoder, 3, "FooBar.txt")

    def tearDown(self):
    	pass

class MoreInput(TestCase):
	"""
	Tests the input given in the assignment repeated several lines
	"""
	
	@class_setup
    def setUp(self):
    	pass

    def test_invalid_length(self):
    	pass 

class MuchInput(TestCase):
	"""
	Tries to compress the first book of 'Heart of Darkness'
	"""
	
	@class_setup
    def setUp(self):
    	pass

    def test_capacity(self):
    	pass 
  

"""
segment = Encoding.Encoder(3, "Input", "Output")
segment.segment()

bad_segment = Encoding.Encoder('a', "aklfda", "Output2")
bad_segment.segment()
"""