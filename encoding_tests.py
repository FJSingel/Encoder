'''
Created on Sep 8, 2013

@author: Frank
'''
import os
import string

import mock
from testify import *

import Encoding

'''
Counting number of tests needed and line numbers of statements where:

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

            Total:  ~21 cases
'''
class BasisTests(TestCase):
    """
    Tests the input given in the assignment
    """
    @class_setup
    def setUp(self):
    	self.blank = open("blank.txt", "w+")
        self.blank_encoder = Encoding.Encoder(3, "blank.txt")

    def test_init(self):
        #init 12
        segment = Encoding.Encoder(3, "Input.txt")
        assert_equals("Input.txt", segment.input_file)
        assert_equals(string.whitespace + string.punctuation, segment.delimiters)
        assert_equals("", segment.segment)

    def test_init_value_error(self):
        #if 16 and except 18
        with assert_raises(ValueError):
            segment = Encoding.Encoder(-3, "Input.txt")

    def test_init_type_error(self):
        #except 21
        with assert_raises(TypeError):
            segment = Encoding.Encoder('a', "Input.txt")

    def test_segment_normal(self):
        #segment_file 30
        segment = Encoding.Encoder(3, "Input.txt")
        assert_equals("1 2 3 4 5 2 1 2 6 5 2 1 2 7 8 9 ", segment.segment_file())
        
    def test_segment_line_loop(self):
        #for 36 and for 37
        assert_equals("", self.blank_encoder.segment_file())

    def test_process_char(self):
        #process_char 43 and if 55
        segment = Encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        segment._process_char('P')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        segment._process_char('I')
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'API\') ", str(segment.legend.legend))

    def test_process_char_nondelimiter(self):
        #if 49 
        #probably dataflow too
        segment = Encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        assert_equals("A", segment.segment)
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))

    def test_process_char_delimiter(self):
        #if 49 
        #probably dataflow too
        segment = Encoding.Encoder(3, "blank.txt")
        segment._process_char('.')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'.\') ", str(segment.legend.legend))

    def test_process_char_full_segment(self):
        #if 55
        segment = Encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        segment._process_char('P')
        segment._process_char('I')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'API\') ", str(segment.legend.legend))

    def test_add_segment(self):
        #add_segment 71 if 80 if 83
        PDict = Encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def test_ordered_dict_init(self):
        #init 65
        PDict = Encoding.PriorityDict()
        assert_equals("", str(PDict.output))
        assert_equals("", str(PDict.numbered))
        assert_equals("", str(PDict.legend))
        assert_equals("", str(PDict.reorderable_legend))

    def test_add_segment_blank(self):
        #if 80
        PDict = Encoding.PriorityDict()
        assert_equals(-1, PDict.add_segment(""))
        assert_equals("", str(PDict.output))
        assert_equals("", str(PDict.numbered))
        assert_equals("", str(PDict.legend))

    def test_add_segment_not_found(self):
        #if 83
        PDict = Encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def test_add_segment_is_found(self):
        #if 83
        PDict = Encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 0 ", str(PDict.output))
        assert_equals("1 1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))


    def test_lookup_default(self):
        #_lookup_segment 92 and if 99
        PDict = Encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hi"), (2, "Lt"), (3, "Dan")]
        assert_equals(1, PDict._lookup_segment(PDict.reorderable_legend, "Lt"))

    def test_lookup_no_match(self):
        #for 99
        PDict = Encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hi"), (2, "Lt"), (3, "Dan")]
        assert_equals(len(PDict.reorderable_legend), PDict._lookup_segment(PDict.reorderable_legend, "IceCream"))

    def test_lookup_empty(self):
        #if 98
        PDict = Encoding.PriorityDict()
        assert_equals(len(PDict.reorderable_legend), PDict._lookup_segment(PDict.reorderable_legend, "Lt"))

    def test_prioritize(self):
        #_prioritize 104
        PDict = Encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hey"), (2, "Lt"), (3, "Dan")]
        PDict._prioritize("Dan")
        assert_equals((3, "Dan"), PDict.reorderable_legend[0])

    def test_spaced_list_str(self):
        #__str__ 121
        SList = Encoding.SpacedList([1,2,3,4])
        assert_equals("1 2 3 4 ", str(SList))
        
    def tearDown(self):
        os.remove("blank.txt")

class DataFlowTests(TestCase):
    """
    Stuff defined in one place and used in another
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

class GoodDataTests(TestCase):
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

class BadDataTests(TestCase):
    @class_setup
    def setUp(self):
        pass

    def test_not_in_prioritize(self):
        with assert_raises(IndexError):
            PDict = Encoding.PriorityDict()
            PDict.reorderable_legend = [(1, "Hey"), (2, "Lt"), (3, "Dan")]
            PDict._prioritize("Don")

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
class ErrorGuessing(TestCase):
    """
    For tests that aren't required under other cases
    """
    @class_setup
    def setUp(self):
        pass

    def test_more_input(self):
        pass

    def tearDown(self):
        pass
  
if __name__ == "__main__":
    run()