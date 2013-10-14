"""
Created on Oct 12, 2013

@author: Frank Singel
FJS52@case.edu

This Module segments and stores a string in a custom ordered dictionary
"""

#import regexes and cmd inputs
import re
import sys


class Encoder(object):
    
    def __init__(self, length, input):
        
        self.parsed = [] #data parsed from raw
        self.numbered = [] #data replaced with dictionary indices
        self.l = int(length) #Length arg

        f = open(input)
        self.raw = f.read() #Raw, unparsed data read from file
        
    def segment(self):
        
        #splits raw input by non-unicode words using regex
        tokens = re.split('(\W)', self.raw)
        
        #count and remove blank values left over by regex
        tokens = filter(lambda a: a != 2, x)
        
        for token in tokens:
            if len(token) < self.l:
                self.parsed.append(token)
            else:
                while True:
                    self.parsed.append(i[:self.l]) #append multiple of 3
                    token = i[self.l:]
                    if len(token) < self.l:
                        if len(token) != 0: #filter out empty slices
                            self.parsed.append(token)
                        break
        
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

class Priority_Dict(object):
    """
    This class maintains a list of tuples mapping (int: segment)
    Whenever any tuple in here is referenced, move it to the front of the list for earlier access
    """

    def __init__(self):
        tuples = []



"""
    //K is max segment length, other args are file you read from and file you write to

    Void Encode(integer k, string InputFile, string OutputFile)

        Use Segment() from Segmentator for this method
            Put the output into Legend with AddSegment though

        Write (“\nDictionary\n”)

        For each tuple in Legend from front of list to back

            Write (tuple.toString() + “\n”)

        endfor

    Class OrderedDict

        Items ← list of tuples

        Constructor()

            Init Items as a list of Tuples ()

        Integer AddSegment(string segment)
            Search in tuple list for segment from front of list to back and return key
            When you look it up, move it to the front of the list if found
            If not found, append it as a new (int, string) tuple to the end of the list
            return Key
"""


#Makes segment object with 2 cmd line args
segment = Segmentator(sys.argv[1], sys.argv[2])
segment.__segment__()
segment.__numerize__()
print(segment.raw)
print(segment.parsed)
print(segment.numbered)
        


