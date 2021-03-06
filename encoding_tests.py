'''
Created on Oct 26, 2013

@author: Frank

NOTE: Line numbers are all general areas. Currently, numbers shown are about 4 lines before actual conditional
Counting number of Structured tests needed and line numbers of statements where:

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
import os
import string

import mock
from testify import *

import encoding

class BasisTests(TestCase):
    """
    Tests all conditionals
    """
    @class_setup
    def setUp(self):
    	self.blank = open("blank.txt", "w+")
        self.blank_encoder = encoding.Encoder(3, "blank.txt")
        self.blank.close()
        self.example = open("Input.txt", "w+")
        self.example.write("I came, I saw, I left.")
        self.example.close()

    def test_init(self):
        #init 12
        segment = encoding.Encoder(3, "Input.txt")
        assert_equals("Input.txt", segment.input_file)
        assert_equals(string.whitespace + string.punctuation, segment.delimiters)
        assert_equals("", segment.segment)

    def test_init_value_error(self):
        #if 16 and except 18 and baddata
        with assert_raises(ValueError):
            segment = encoding.Encoder(-3, "Input.txt")

    def test_init_type_error(self):
        #except 21 and baddata
        with assert_raises(TypeError):
            segment = encoding.Encoder('a', "Input.txt")

    def test_segment_normal(self):
        #segment_file 30
        segment = encoding.Encoder(3, "Input.txt")
        assert_equals("1 2 3 4 5 2 1 2 6 5 2 1 2 7 8 9 ", segment.segment_file())

    def test_segment_line_loop(self):
        #for 36 and for 37
        assert_equals("", self.blank_encoder.segment_file())

    def test_process_char(self):
        #process_char 43, if 55, dataflow
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        assert_equals("A", segment.segment)
        segment._process_char('P')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        assert_equals("AP", segment.segment)
        segment._process_char('I')
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'API\') ", str(segment.legend.legend))
        assert_equals("", segment.segment)

    def test_process_char_nondelimiter(self):
        #if 49 and dataflow
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        assert_equals("A", segment.segment)
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))

    def test_process_char_delimiter(self):
        #if 49 and dataflow
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('.')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'.\') ", str(segment.legend.legend))

    def test_process_char_full_segment(self):
        #if 55
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        segment._process_char('P')
        segment._process_char('I')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'API\') ", str(segment.legend.legend))

    def test_add_segment(self):
        #add_segment 71 if 80 if 83
        PDict = encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def test_ordered_dict_init(self):
        #init 65
        PDict = encoding.PriorityDict()
        assert_equals("", str(PDict.output))
        assert_equals("", str(PDict.numbered))
        assert_equals("", str(PDict.legend))
        assert_equals("", str(PDict.reorderable_legend))

    def test_add_segment_blank(self):
        #if 80
        PDict = encoding.PriorityDict()
        assert_equals(-1, PDict.add_segment(""))
        assert_equals("", str(PDict.output))
        assert_equals("", str(PDict.numbered))
        assert_equals("", str(PDict.legend))

    def test_add_segment_not_found(self):
        #if 83 and index's dataflow
        PDict = encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def test_add_segment_is_found(self):
        #if 83 and index's dataflow
        PDict = encoding.PriorityDict()
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
        PDict = encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hi"), (2, "Lt"), (3, "Dan")]
        assert_equals(1, PDict._lookup_segment(PDict.reorderable_legend, "Lt"))

    def test_lookup_no_match(self):
        #for 99 and gooddata
        PDict = encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hi"), (2, "Lt"), (3, "Dan")]
        assert_equals(len(PDict.reorderable_legend), PDict._lookup_segment(PDict.reorderable_legend, "IceCream"))

    def test_lookup_empty(self):
        #if 98 and baddata
        PDict = encoding.PriorityDict()
        assert_equals(len(PDict.reorderable_legend), PDict._lookup_segment(PDict.reorderable_legend, "Lt"))

    def test_prioritize(self):
        #_prioritize 104
        PDict = encoding.PriorityDict()
        PDict.reorderable_legend = [(1, "Hey"), (2, "Lt"), (3, "Dan")]
        PDict._prioritize("Dan")
        assert_equals((3, "Dan"), PDict.reorderable_legend[0])

    def test_spaced_list_str(self):
        #__str__ 121
        SList = encoding.SpacedList([1,2,3,4])
        assert_equals("1 2 3 4 ", str(SList))
        
    def tearDown(self):
        os.remove("blank.txt")
        os.remove("Input.txt")

class DataFlowTests(TestCase):
    """
    Stuff defined in one place and used in another
    """
    @class_setup
    def setUp(self):
        self.blank = open("blank.txt", "w+")
        self.blank.close()

    def test_process_char(self):
        #process_char 43, if 55, dataflow
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('A')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        assert_equals("A", segment.segment)
        segment._process_char('P')
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
        assert_equals("AP", segment.segment)
        segment._process_char('I')
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'API\') ", str(segment.legend.legend))
        assert_equals("", segment.segment)

    def test_process_char_delimiter(self):
        #if 49 and dataflow
        segment = encoding.Encoder(3, "blank.txt")
        segment._process_char('.')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'.\') ", str(segment.legend.legend))
    
    def test_add_segment_not_found(self):
        #if 83 and index's dataflow
        PDict = encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def test_add_segment_is_found(self):
        #if 83 and index's dataflow
        PDict = encoding.PriorityDict()
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 ", str(PDict.output))
        assert_equals("1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))
        assert_equals(0, PDict.add_segment("Hey"))
        assert_equals("0 0 ", str(PDict.output))
        assert_equals("1 1 ", str(PDict.numbered))
        assert_equals("(1, \'Hey\') ", str(PDict.legend))

    def tearDown(self):
        os.remove("blank.txt")

class BoundaryTests(TestCase):
    """
    Check for off-by-one errors: Just above, on and below max
    """
    @class_setup
    def setUp(self):
        self.blank = open("blank.txt", "w+")

    def test_process_char_short_segment(self):
        #If char processed when just too short for storing
        #Boundary Analysis
        segment = encoding.Encoder(3, "blank.txt")
        segment.segment = "A"
        segment._process_char('A')
        assert_equals("AA", segment.segment)
        assert_equals("", str(segment.legend.numbered))
        assert_equals("", str(segment.legend.output))
        assert_equals("", str(segment.legend.legend))
    
    def test_process_char_short_segment(self):
        #If char processed to exactly store
        #Boundary Analysis
        segment = encoding.Encoder(3, "blank.txt")
        segment.segment = "AA"
        segment._process_char('A')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'AAA\') ", str(segment.legend.legend))

    def test_process_char_short_segment(self):
        #If char processed to beyond store; shouldn't happen
        #Boundary Analysis
        segment = encoding.Encoder(3, "blank.txt")
        segment.segment = "AAA"
        segment._process_char('A')
        assert_equals("", segment.segment)
        assert_equals("1 ", str(segment.legend.numbered))
        assert_equals("0 ", str(segment.legend.output))
        assert_equals("(1, \'AAAA\') ", str(segment.legend.legend))

    def tearDown(self):
        os.remove("blank.txt")

class GoodDataTests(TestCase):
    """
    Min/max norm configuration
    Compatability with old Data
    Nominal cases / expected values
    Everything in here is a "good data" test in addition
        to anything else listed on each test 
    """
    @class_setup
    def setUp(self):
        self.blank = open("blank.txt", "w+")
        self.blank_encoder = encoding.Encoder(3, "blank.txt")
        self.blank.close()
        self.onechar = open("onechar.txt", "w+")
        self.onechar.write("A")
        self.onechar.close()
        self.newlines = open("newlines.txt", "w+")
        self.newlines.write("\n\n\n\n\n\n\n")
        self.newlines.close()
        self.example = open("Input.txt", "w+")
        self.example.write("I came, I saw, I left.")
        self.example.close()

    def test_regular_use(self):
        segment = encoding.Encoder(3, "Input.txt")
        assert_equals("1 2 3 4 5 2 1 2 6 5 2 1 2 7 8 9 ", segment.segment_file())

    def test_min_token_size(self):
        segment = encoding.Encoder(1, "Input.txt")
        assert_equals("1 2 3 4 5 6 7 2 1 2 8 4 9 7 2 1 2 10 6 11 12 13 ", segment.segment_file())

    def test_newlines_file(self):
        segment = encoding.Encoder(3, "newlines.txt")
        assert_equals("1 1 1 1 1 1 1 ", segment.segment_file())

    def test_empty_file(self):
        assert_equals("", self.blank_encoder.segment_file())
        
    def tearDown(self):
        os.remove("onechar.txt")
        os.remove("newlines.txt")
        os.remove("Input.txt")
        os.remove("blank.txt")

class BadDataTests(TestCase):
    """
    Every test in this class falls under the bad data category of tests
    in addition to what their individual comments state
    """
    @class_setup
    def setUp(self):
        self.example = open("Input.txt", "w+")
        self.example.write("I came, I saw, I left.")
        self.example.close()
        try:
            os.remove("Santa.txt") #ensure there's no Santa
        except OSError, e:
            pass

    def test_not_in_prioritize(self):
        with assert_raises(IndexError):
            PDict = encoding.PriorityDict()
            PDict.reorderable_legend = [(1, "Hey"), (2, "Lt"), (3, "Dan")]
            PDict._prioritize("Don")

    def test_lookup_empty(self):
        #if 98
        PDict = encoding.PriorityDict()
        assert_equals(len(PDict.reorderable_legend), PDict._lookup_segment(PDict.reorderable_legend, "Lt"))

    def test_init_value_error(self):
        #if 16 and except 18
        with assert_raises(ValueError):
            segment = encoding.Encoder(-3, "Input.txt")

    def test_init_type_error(self):
        #except 21
        with assert_raises(TypeError):
            segment = encoding.Encoder('a', "Input.txt")

    def test_no_file(self):
        with assert_raises(IOError):
            segment = encoding.Encoder(3, "Santa.txt")
            segment.segment_file()

    def tearDown(self):
        os.remove("Input.txt")

class StressTest(TestCase):
    """
    Tries to compress a the entirety of 'Heart of Darkness'
    """
    @suite('stress', reason="Time Intensive Stress Test not needed on every test run")
    def test_more_input(self):
    	segment = encoding.Encoder(3, "HEART OF DARKNESS.txt")
        test = segment.segment_file()
  
class ErrorGuessing(TestCase):
    """
    Other things I thought I'd test
    """

    def setUp(self):
        self.example = open("leftover.txt", "w+")
        self.example.write("I came, I saw, I left.Z")
        self.example.close()

    def test_non_ascii_file(self):
        #it just isn't equipped to handle this correctly, but possibly should
        segment = encoding.Encoder(3, "nonascii.txt")
        assert_equals("1 2 3 4 2 5 6 2 3 4 7 ", segment.segment_file())

    def test_leftover_segment(self):
        #Tests that any segments leftover at end of parsing are processed
        segment = encoding.Encoder(3, "leftover.txt")
        assert_equals("1 2 3 4 5 2 1 2 6 5 2 1 2 7 8 9 10 ", segment.segment_file())

    def tearDown(self):
        os.remove("leftover.txt")

if __name__ == "__main__":
    run()