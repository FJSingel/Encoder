'''
Created on Sep 8, 2013

@author: Frank
'''
import os

from testify import *

import Encoding

'''
Counting number of tests needed:

Init 12
If 16               4
Except 18
Except 21

Segment_file 30
For 36              3
For 37

_process_char 43
if 49               3
if 55

init 65             1

add_segment 71
if 80               3
if 83

lookup_segment 92
for 98              3
if 99

_prioritize 104     1

str 114             1

str 121             2
for 123

            Total:  21 cases
'''
class BasisTests(TestCase):
    """
    Tests the input given in the assignment
    """
    @class_setup
    def setUp(self):
    	pass

    def test_regular_use(self):
        pass
        
    def tearDown(self):
        pass

class DataFlowTests(TestCase):
    """
    Do I have any?
    """
    @class_setup
    def setUp(self):
        pass

    def test_regular_use(self):
        pass
        
    def tearDown(self):
        pass

class BoundaryTests(TestCase):
    """
    Check for off-by-one errors: Just above, on and below max
    
    if 16
    if 55
    if 83?
    if 99?
    """
    @class_setup
    def setUp(self):
        pass

    def test_regular_use(self):
        pass
        
    def tearDown(self):
        pass

class GoodDataTests():
    """
    Min/max norm configuration
    Compatability with old Data
    Nominal cases / expected values
    """
    @class_setup
    def setUp(self):
        pass

    def test_regular_use(self):
        pass
        
    def tearDown(self):
        pass

class BadDataTests():
    @class_setup
    def setUp(self):
        pass

    def test_regular_use(self):
        pass
        
    def tearDown(self):
        pass


class StressTest(TestCase):
    """
    #Tries to compress a large excerpt from 'Heart of Darkness'
    """
    @class_setup
    def setUp(self):
        pass

    @suite('disabled', reason="Time Intensive Stress Test not needed for debug purposes")
    def test_more_input(self):
    	segment = Encoding.Encoder(3, "Excerpt.txt")
        test = segment.segment_file()

    def tearDown(self):
        pass

  
if __name__ == "__main__":
    run()