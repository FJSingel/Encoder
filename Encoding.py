#import regexes and cmd inputs
import fileinput
import re
import sys

class Encoder(object):
    
    def __init__(self, length, input):
        
        self.parsed = [] #data parsed from raw
        self.numbered = [] #data replaced with dictionary indices
        self.l = int(length) #Length arg
        self.legend = PriorityDict()

        f = open(input)
        self.raw = f.read() #Raw, unparsed data read from file
        
    def segment(self):
        """
        Decided to handle reading the file in the constructor
        Each Encoder handles one input file
        This varies from initial pseudocode since Segmentator doesn't quite match it
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
                self.parsed.append(token)
                self.legend.add_segment(token)
            else:
                while len(token) >= self.l:
                    self.parsed.append(token[:self.l]) #append multiple of l
                    self.legend.add_segment(token[:self.l])
                    token = token[self.l:]
                    if len(token) < self.l:
                        if len(token) != 0: #ignore empty slices
                            self.parsed.append(token)
                            self.legend.add_segment(token)
        
        print self.legend.legend
        print self.legend.numbered
        print self.legend.output
        print self.legend.reorderable_legend
        return self.parsed
    
    def encode(self):
        
        dictionary = []
        
        for e in self.parsed:
            try: #See if it's already in our dictionary. Exception if it's not
                index = dictionary.index(e)
            except ValueError: #If not in dictionary, add it
                dictionary.append(e)
                
            self.numbered.append(dictionary.index(e) + 1)
        
        return self.numbered

"""
    string output(list input)
        Use the input list to produce output similar to the output table in example
        This will require reordering that is no longer used in adding to the legend
"""


class PriorityDict(object):
    """
    This class maintains a list of tuples mapping (int: segment)
    Whenever any tuple in here is referenced, move it to the front of the list for earlier access
    """

    def __init__(self):
        self.legend = [] #Don't reorder this one. It's our original legend
        self.numbered = [] #This holds the number conversion of the string
        self.reorderable_legend = [] #This will be the reordering list used to construct the 
        self.output = []    #This will represent the output string of ints
    
    def add_segment(self, segment):
        """
        Integer AddSegment(string segment)
        Search in tuple list for segment from front of list to back and return key
        If not found, append it as a new (int, string) tuple to the end of legend
        Then add the index of whatever was just found (or not found) to the self.numbered
        """

        index = self.lookup(self.legend, segment)

        if(index == len(self.legend)): #if it's not in there, add it
            self.legend.append((index+1, segment))
            self.reorderable_legend.append((index+1, segment))

        self.output.append(self.lookup(self.reorderable_legend, segment))
        self.reorderable_legend.insert(0, self.reorderable_legend.pop(self.lookup(self.reorderable_legend, segment))) #move tuple to front of dict
        print ("{}:{}".format(segment, self.reorderable_legend))
        self.numbered.append(index+1)
        
        return index

    def lookup(self, tuple_list, target):
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