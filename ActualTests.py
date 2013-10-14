'''
Created on Sep 8, 2013

@author: Frank
'''
import os

from testify import *

import Encoding

class DefaultInput(TestCase):
    """
    Tests the input given in the assignment
    """
    @class_setup
    def setUp(self):
    	try: #remove old output files if found
        	os.remove("./DefaultOutput1.txt")
        	os.remove("./DefaultOutput2.txt")
        	os.remove("./DefaultOutput3.txt")
        except OSError:
        	pass

    def test_regular_use(self):
        segment = Encoding.Encoder(3, "Input1.txt")
        segment.segment()
        segment.write_results("DefaultOutput1.txt")

    def test_decimal_length(self):
        segment = Encoding.Encoder(2.5, "Input1.txt")
        segment.segment()
        segment.write_results("DefaultOutput2.txt")

    def test_long_length(self):
        segment = Encoding.Encoder(35, "Input1.txt")
        segment.segment()
        segment.write_results("DefaultOutput3.txt")

    def test_invalid_length(self):
        assert_raises(ValueError, Encoding.Encoder, -3, "Input1.txt")
        assert_raises(TypeError, Encoding.Encoder, 'a', "Input1.txt")

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
        try: #remove old output files if found
        	os.remove("./MoreOutput.txt")
        except OSError:
        	pass

    def test_more_input(self):
    	segment = Encoding.Encoder(35, "Input2.txt")
        segment.segment()
        segment.write_results("MoreOutput.txt")

    def tearDown(self):
        pass

class MuchInput(TestCase):
    """
    Tries to compress the first book of 'Heart of Darkness'
    """
    @class_setup
    def setUp(self):
        os.remove("./HeartOutput.txt")

    def tearDown(self):
        pass
  
if __name__ == "__main__":
    run()