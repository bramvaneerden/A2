import numpy as np
import typing

class IntelDevice:
    def __init__(self, width:int, height:int, enc_locations: typing.List[str], enc_codes:typing.List[str], caesar_shift: int):
        """
        The IntelDevice object, containing all information and functions required for encoding and decoding messages,
        processing raw encoded locations, efficiently searching for locations based on codes and returning encoded
        answers.  

        :param width: The width (number of columns) of the 2D distance/location grid (self.loc_grid) that we have to fill in
        :param height: The height (number of rows) of the 2D distance/location grid (self.loc_grid) that we have to fill in
        :param enc_locations: A list of encoded location names that correspond to the locations in self.loc_grid
        :param enc_codes: A list of encoded codes (ints) that have to be entered into self.loc_grid
        :param caesar_shift: The caesar shift constant used to encode messages. You may assume this will always be in the set 
                             {0,1,...,26}. We do NOT use modulo calculations for our caesar cipher. 

        You do not need to change this function
        """

        self.width = width
        self.height = height
        self.enc_locations = enc_locations
        self.enc_codes = enc_codes
        self.caesar_shift = caesar_shift

        self.loc_grid = np.zeros((height, width))
        self.coordinate_to_location = dict() # maps locations (y,x) to their names 


    def encode_message(self, msg:str) -> str:
        """
        A function that encodes a given string using a simplified form of caesar cipher (without using modulo). Every character of the string will be 
        transformed into the ordinal/numerical representation and encoded by shifting the number with self.caesar_shift 
        (through addition). Afterward, the shifted numbers are transformed into bitstring representation.

        For example, suppose we want to encode the message 'hello' with a caesar shift of 5. 
        The corresponding encoded message (output of this function) would be '1101101 1101010 1110001 1110001 1110100'. Note that the 
        number of bitstrings separated by spaces is equal to the number of characters of the string 'hello'. 
        Let's look at the first character 'h'. Its ordinal representation is 104. We shift its representation by 5, giving us 109. 
        109 is then transformed into a bitstring, which gives us 1101101 (the first bitstring in the encoded message). 

        Hints: the following built-in Python functions may be of use
          - ord(x): takes a character x as input and returns the ordinal representation
          - '{0:b}'.format(x): transforms a number x into a bitstring

        :param msg: The input message (string) that should be encoded
        
        Returns: the encoded message
        """
        # print(msg)
        
        # transform all characters in msg into their ordinal representation
        ordinals = [ord(x) for x in msg]
        # print(ordinals)

        # print("self.caesar_shift" + self.caesar_shift)

        # shift the ordinal representation by self.caesar_shift
        shifted_ordinals = [x + self.caesar_shift for x in ordinals]
        # print(shifted_ordinals)

        # transform the shifted ordinals into bitstrings and separate them by spaces
        bitstrings = ['{0:b}'.format(x) for x in shifted_ordinals]
        # print(bitstrings)

        #separate the bitstrings by spaces
        encoded_msg = ' '.join(bitstrings)
        # print(encoded_msg)

        return encoded_msg

    def decode_message(self, msg: str) -> str:
        """
        A function that decodes an encoded message (the reverse of the function above). For example, given the encoded message 
        '1101101 1101010 1110001 1110001 1110100' (with the caesar shift self.caeser_shift=5), this function should return the decoded 
        message, which is 'hello'. 

        :param msg: The encoded message (string) that should be decoded
        
        Returns: the decoded message
        """
        # print(msg)
        # transform the encoded message into a list of bitstrings
        bitstrings = msg.split(' ')
        # print(bitstrings)

        # transform the bitstrings into their ordinal representation
        ordinals = [int(x, 2) for x in bitstrings]
        # print(ordinals)

        # shift the ordinal representation by -self.caesar_shift
        shifted_ordinals = [x - self.caesar_shift for x in ordinals]
        # print(shifted_ordinals)

        # transform the shifted ordinals into characters
        decoded_msg = ''.join([chr(x) for x in shifted_ordinals])
        # print(decoded_msg)

        return decoded_msg


    def fill_coordinate_to_loc(self):
        """
        Function that fills the data structure self.coordinate_to_location. It maps every (y,x) tuple in self.loc_grid
        to the corresponding decoded location (determined from self.enc_locations). The list of encoded locations wrap
        around the rows of self.loc_grid from left to right and top to bottom. For example, if we have a 2x2 loc_grid and 
        self.enc_locations = [self.encode_message('a'), self.encode_message('b'), self.encode_message('c'), self.encode_message('d')], 
        then the mapping should be:
          (0,0) -> 'a'
          (0,1) -> 'b'
          (1,0) -> 'c'
          (1,1) -> 'd'

        The function does not return anything. It simply fills the self.coordinate_to_location data structure with the right mapping.
        """

        # print(self.enc_locations)

        # decode the encoded locations
        decoded_locations = [self.decode_message(x) for x in self.enc_locations]
        # print(decoded_locations)

        # fill the self.coordinate_to_location data structure
        for i in range(self.height):
            for j in range(self.width):
                self.coordinate_to_location[(i,j)] = decoded_locations[i*self.width + j]
        
        # print(self.coordinate_to_location)
        


    def fill_loc_grid(self):
        """
        Function that fills the data structure self.loc_grid with the codes found in self.enc_codes. Note that
        these codes have to be decoded using self.decode_message(). The encoded codes wrap around self.loc_grid 
        from left to right, and from top to bottom. For example, if we have 
        self.enc_codes = [self.encode_message('10'), self.encode_message('15'), self.encode_message('11'), self.encode_message('16')],
        the following loc_grid should be created/filled in:
          [[10,15],
           [11,16]]

        The function does not return anything. It simply fills the self.loc_grid data structure with the decoded codes.
        """

        # print (self.enc_codes)

        # decode the encoded codes
        decoded_codes = [self.decode_message(x) for x in self.enc_codes]
        # print(decoded_codes)

        # fill the self.loc_grid data structure
        for i in range(self.height):
            for j in range(self.width):
                self.loc_grid[i][j] = decoded_codes[i*self.width + j]

        # print(self.loc_grid)


    def divconq_search(self, value: int, x_from: int, x_to: int, y_from: int, y_to: int) -> typing.Tuple[int, int]:
        """
        The divide and conquer search function. The function searches for value in a subset of self.loc_grid.
        More specifically, we only search in the x-region from x_from up to (and including) x_to and the y-region
        from y_from up to (and including) y_to. At the initial function call, x_from=0, x_to=self.width-1, y_from=0, y_to=self.height-1 ,
        meaning that we search over the entire 2d grid self.loc. 
        This function recursively calls itself on smaller subproblems (subsets/subrectangles of the 2d grid) and combines the solutions
        to these subproblems in order to find the solution to the complete initial problem.

        Note: this function should be more efficient than a naive search that iterates over every cell until the value is found. 
        Thus, make sure design a proper divide and conquer strategy for this. A too simplistic strategy (search over every cell in the grid) 
        will not lead to a passing grade. Please consult the TAs before handing in the assignment whether your approach is good. 

        :param value: The value that we are searching for in the subrectangle specified by (x_from, x_to, y_from, y_to)
        :param x_from: The leftmost x coordinate of the subrectangle that we are searching over
        :param x_to: The rightmost x coordinate of the subrectangle we are searching over
        :param y_from: The topmost y coordinate of the subrectangle we are searching over
        :param y_to: The bottom y coordinate of the subrectangle we are searching over

        Note that the following two constraints hold:
          1. x_from <= x_to
          2. y_from <= y_to

        Returns:
          None if the value does not occur in the subrectangle we are searching over
          A tuple (y,x) specifying the location where the value was found (if the value occurs in the subrectangle)

        """
        print(value, x_from, x_to, y_from, y_to)

        # print the subrectangle that we are searching over
        for i in range(y_from, y_to+1):
            print(self.loc_grid[i][x_from:x_to+1])

        # check if value is in the subrectangle we are searching over
        # loop over cells in this subproblem
        for i in range(y_from, y_to+1):
          for j in range(x_from, x_to+1):
            if self.loc_grid[i][j] == value:
              print("found")
              print(i,j)
              return (i,j)
            
        


        # find middle location in the subrectangle
        x_mid = (x_from + x_to) // 2
        y_mid = (y_from + y_to) // 2

        # print(x_mid, y_mid)

        # check if the value is in the middle location
        if self.loc_grid[y_mid][x_mid] == value:
            return (y_mid, x_mid)
        

        if self.loc_grid[y_mid][x_mid] < value:
          print("less than")  
          # search top right subrectangle
          if x_mid != x_to and y_mid != y_from:
            self.divconq_search(value, x_mid, x_to, y_mid, y_to)

          # top right done
          if x_from >= x_mid and y_from >= y_mid:
              self.divconq_search(value, x_mid+1, x_to, y_from, y_to)
            
        if self.loc_grid[y_mid][x_mid] > value:
          print("greater than")     

          # search top right subrectangle
          if x_mid != x_to and y_mid != y_from:
            self.divconq_search(value, x_mid, x_to, y_from, y_mid)

          # top right done -> search left vertical
          if x_from >= x_mid and y_from >= y_mid:
              self.divconq_search(value, x_from, x_to, y_from, y_mid-1)

    
            

    def start_search(self, value) -> str:
        """
        Non-recursive function that starts the recursive divide and conquer search function above. You can assume
        that self.coordinate_to_location and self.loc_grid have already been filled before this function is called (so 
        make sure not to call them again in this function). 
        
        :param value: The value that we are searching for in self.loc_grid

        Returns:
          None if the value does not occur in self.loc_grid
          The encoded location of where the value was found. Note that the location is not the (y,x) tuple but the
          corresponding name of the location (encoded with self.encode_message). 
        """

        # process raw locations with caesar shift, 
        # construct the loc_grid and start the search
        result = self.divconq_search(value, x_from=0, x_to=self.loc_grid.shape[1]-1, y_from=0, y_to=self.loc_grid.shape[0]-1)

        if result is None:
            return result
        else:
            return self.encode_message(self.coordinate_to_location[result])
        