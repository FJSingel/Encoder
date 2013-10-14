"""
Created on Oct 12, 2013

@author: Frank Singel
FJS52@case.edu

This Module segments and stores a string in a custom ordered dictionary
"""
from math import ceil
import re

class Encoder(object):
    
    def __init__(self, length, input):
        
        try:
            self.l = int(ceil(length)) #Length arg cast into an int
            if (self.l < 1):
                raise ValueError
        except ValueError:
            print "Error: Invalid segment length specified. Exiting"
            raise ValueError
        except TypeError:
            print "Error: Invalid segment length specified. Exiting"
            raise TypeError

        self.legend = PriorityDict() #stores all processed data

        try:
            f = open(input)
            self.raw = f.read() #Raw, unparsed data read from file
        except IOError, e:
            print "Error: File not found. Exiting\n", e
            raise e
        
    def segment(self):
        """
        Decided to handle reading the file in the constructor
        Each Encoder handles one input file and tokenizes the input by non-alphanumeric characters
        """

        #splits raw input by non-unicode words using regex
        tokens = re.split('(\W)', self.raw)
        
        #count and remove blank values left over by regex
        tokens = filter(lambda a: a != "", tokens)
        
        '''
        Read tokens
            If token is small enough
                add token to dict
            else 
                slice token into smaller tokens and add them to legend
        '''
        for token in tokens:
            if len(token) < self.l: #If token is small enough
                self.legend.add_segment(token)
            else:
                while len(token) >= self.l:
                    self.legend.add_segment(token[:self.l]) #append multiple of l
                    token = token[self.l:]
                    if len(token) < self.l:
                        if len(token) != 0: #ignore empty slices
                            self.legend.add_segment(token)
        '''
        --MOVED INTO SEPERATE METHOD--
        --Why make file writing mandatory?--
        Produce output here
        For each tuple in legend
            Write tuple to output
        endfor

        self._write_results(self.legend)
        '''

    def write_results(self, output_file):
        """
        Given PriorityDict, it writes the legend and encoded string to an output file

        Write Output
        Write Legend
        For each tuple in legend
            Write tuple to output
        endfor
        """
        try:
            target = open(output_file, 'w')
            target.write("Input:  ")
            for value in self.legend.numbered:
                target.write(str(value) + " ")

            target.write("\nOutput: ")
            for value in self.legend.output:
                target.write(str(value) + " ")

            target.write("\n\nLegend\n")
            for pair in self.legend.legend:
                target.write(str(pair) + "\n")
        except IOError, e:
            print "IOError while writing output."
            raise e
        else:
            target.close()

class PriorityDict(object):
    """
    This class maintains a list of tuples mapping (int: segment)
    Whenever any tuple in here is referenced, move it to the front of the list for earlier access
    """

    def __init__(self):
        self.legend = [] #Don't reorder this one. It's our original legend
        self.numbered = [] #This holds the number conversion of the string
        self.reorderable_legend = [] #This will be the reordering list used to construct the output
        self.output = []    #This will represent the output string of ints
    
    def add_segment(self, segment):
        """
        Integer AddSegment(string segment)
        Search in tuple list for segment from front of list to back and return key
        If not found, append it as a new (int, string) tuple to the end of legend
        Then add the index of whatever was just found (or not found) to the self.numbered
        Move whatever was accessed to the front of reorderable_legend
        """

        index = self._lookup(self.legend, segment)

        if(index == len(self.reorderable_legend)): #if it's not in there, add it
            self.legend.append((index+1, segment))
            self.reorderable_legend.append((index+1, segment))

        self.output.append(self._lookup(self.reorderable_legend, segment))
        self._prioritize(segment) #move tuple to front of list
        self.numbered.append(index+1)
        
        return index

    def _lookup(self, tuple_list, target):
        """
        lookup index of the target in a tuple in the list, return it's index,
        then move it to the front of the list

        Returns the index it was found at. Returns len(legend) if not found
        """
        index = 0

        for key, segment in tuple_list:
            if target == tuple_list[index][0]:
                return index
            if target == tuple_list[index][1]:
                return index
            index += 1

        return index

    def _prioritize(self, segment):
        """
        move the selected segment to the front of the list
        """
        self.reorderable_legend.insert(0, self.reorderable_legend.pop(self._lookup(self.reorderable_legend, segment)))
