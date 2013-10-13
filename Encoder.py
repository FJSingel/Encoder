"""
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

                Write (key.toString() + “ ”)

                segment ← “”

                key ← Legend.AddSegment(inputChar)

                Write (key.toString() + “ ”)

            Endif

            Append inputChar to segment

            if segment.length() = k

                key ← Legend.AddSegment(segment)

                Write (key.toString() + “ ”)

                segment ← “”

            Endif

        EndWhile

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