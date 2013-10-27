"""
Created on Oct 12, 2013

@author: Frank Singel
FJS52@case.edu

This Module segments and stores a string in a custom ordered dictionary
"""
from math import ceil
import string

class Encoder(object):
    
    def __init__(self, length, reading_file):
        
        try:
            self.length = int(ceil(length)) #Length arg cast into an int
            if (self.length < 1):
                raise ValueError
        except ValueError:
            print "Error: Invalid segment length specified. Exiting"
            raise ValueError
        except TypeError:
            print "Error: Invalid segment length specified. Exiting"
            raise TypeError

        self.legend = PriorityDict() #stores all processed data
        self.input_file = reading_file
        self.delimiters = string.whitespace + string.punctuation
        self.segment = ""
        self.encoded_string = ""
        self.reordered_string = ""
        self.legend_string = ""
        
    def segment_file(self):
        """
        Decided to handle reading the file in the constructor
        Each Encoder handles one input file and tokenizes the input by non-alphanumeric characters
        """
        with open(self.input_file) as f:
            for line in f:
                for char in line:
                    self._process_char(char)
        #Handles case where there's an unprinted segment leftover.
        self.legend.add_segment(self.segment)
        return str(self.legend.numbered)

    def _process_char(self, character):
        """
        If character is a delimiter, add the segment and character to the legend
        If it's not, then append the char to the segment and add the segment
         to legend if it's long enough
        """
        if character in self.delimiters:
            self.legend.add_segment(self.segment)
            self.legend.add_segment(character)
            self.segment = ""
        else:
            self.segment += character
            if len(self.segment) >= self.length:
                self.legend.add_segment(self.segment)
                self.segment = ""
    
class PriorityDict(object):
    """
    This class maintains a list of tuples mapping (int: segment)
    Whenever any tuple in here is referenced, move it to the front of the list for earlier access
    """

    def __init__(self):
        self.legend = SpacedList() #Don't reorder this one. It's our original legend
        self.numbered = SpacedList() #This holds the number conversion of the string
        self.reorderable_legend = SpacedList() #This will be the reordering list used to construct the output
        self.output = SpacedList() #This will represent the output string of ints
    
    def add_segment(self, segment):
        """
        Integer AddSegment(string segment)
        Search in tuple list for segment from front of list to back and return key
        If not found, append it as a new (int, string) tuple to the end of legend
        Then add the index of whatever was just found (or not found) to the self.numbered
        Move whatever was accessed to the front of reorderable_legend
        """

        if segment == "":
            return -1

        index = self._lookup_segment(self.legend, segment)

        if(index == len(self.reorderable_legend)): #if it's not in there, add it
            self.legend.append((index+1, segment))
            self.reorderable_legend.append((index+1, segment))

        self.output.append(self._lookup_segment(self.reorderable_legend, segment))
        self._prioritize(segment) #move tuple to front of list
        self.numbered.append(index+1)
        
        return index

    def _lookup_segment(self, tuple_list, target):
        """
        Returns the index target is found at. Returns len(legend) if not found
        Legend contains tuples of (int value, string segment)
        """
        index = 0

        for key, segment in tuple_list:
            if target == segment:
                return index
            index += 1
        return index

    def _prioritize(self, segment):
        """
        move the selected segment to the front of the list
        """
        self.reorderable_legend.insert(0, self.reorderable_legend.pop(self._lookup_segment(self.reorderable_legend, segment)))

    def __str__(self):
        legend_string = ("Encoded:\t\t" + str(self.numbered) +
                         "\nReordered encoded:\t" + str(self.output) +
                         "\nLegend: " + str(self.legend))
        return legend_string

class SpacedList(list):
    def __str__(self):
        output = ""
        for value in self:
            output += (str(value) + " ")
        return output
'''
TODO List:

Create a makefile
Look into stringIO
check empty input
Write to stdio instead of to a file (makes testing easier) and maybe use a wrapper to print
Get clarification of requirements for ANY QUESTIONS
    Like Writing from pseudocode vs reusing segmentator if they don't agree
    What form output should be in, like file output vs STDIO
whitespace problems
Finally where I have else
Just put segment to a string
'''