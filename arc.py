# first subproblem: call function on the first row
        if y_to != 0 and y_from == 0:
          self.divconq_search(value, x_from, x_to, 0, 0)

        # base case: if the value is not found in the final subproblem, return None
        if y_to == self.height or x_to == self.width:
          print("not found")
          return None

        # check if value is in this subproblem
        # loop over cells in this subproblem
        for i in range(y_from, self.height):
          for j in range(x_from, self.width):
            if self.loc_grid[i][j] == value:
              print("found")
              print(i,j)
              return (i,j)
            
        # if value is not in this subproblem, move onto the next subproblem
        self.divconq_search(value, x_from, x_to, y_from+1, y_to+1)