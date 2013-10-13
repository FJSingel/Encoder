"""
Class Encoder
    //K is max segment length, other args are file you read from and file you write to

    Void Encode(integer k, string InputFile, string OutputFile)

        Open a FileInputStream and FileOutputStream to read and write from using filename arguments

        segment ← “”

        inputChar ← ''

        Legend ← new OrderedDictionary

        Assert k != 0


        While FileInputStream is not empty

            inputChar ← Read char from FileInputStream

            If inputChar = whitespace

                key ← Legend.AddSegment(segment)

                segment ← “”

                key ← Legend.AddSegment(inputChar)

            Endif

            Append inputChar to segment

            if segment.length() = k

                key ← Legend.AddSegment(segment)

                segment ← “”

            Endif

            if nextChar = EOF

                key ← Legend.AddSegment(segment)

                segment ← “”

            Endif

        EndWhile

        Write (“\nDictionary\n”)

        For each tuple in Legend from front of list to back

            Write (tuple.toString() + “\n”)

        endfor

    string output(list input)
        Use the input list to produce output similar to the output table in example
        This will require reordering that is no longer used in adding to the legend
"""


class Priority_Dict(object):
    """
    This class maintains a list of tuples mapping (int: segment)
    Whenever any tuple in here is referenced, move it to the front of the list for earlier access
    """

    def __init__(self):
        self.legend = [] #Don't reorder this one. It's our original legend
        self.numbered = "" #This holds the number conversion of the string
    
    def add_segment(self, segment):
        """
        Integer AddSegment(string segment)
        Search in tuple list for segment from front of list to back and return key
        If not found, append it as a new (int, string) tuple to the end of legend
        Then add the index of whatever was just found (or not found) to the self.numbered
        """

        for pair in self.legend:
            try: #See if it's already in our dictionary. Exception if it's not.
                index = self.legend.index(pair)
            except ValueError: #If not in dictionary, add it
                self.legend.append(pair)
                
            self.numbered.append(legend.index(pair)) + 1)
        

    def lookup(self, key):
        """
        lookup key value, return it's index, then move it to the front of the list
        """

    def move_index_to_front(self, index):
        """
        helper for lookup()
        Moves tuple with index to front of list
        """
