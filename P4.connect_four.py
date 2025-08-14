#minor improvement: does not account for tie (full board)

class ConnectFour:
    def __init__(self):
        self.grid = [[" . ", " . ", " . ", " . ", " . ", " . ", " . "] for i in range(6)]
        self.row = 0

    def place_x(self, column: int):
        index = 0
        for row in self.grid:
            if row[column] == " . ":
                row[column] = " X "
                self.row = index
                break
            index += 1
                

    def place_o(self, column: int):
        index = 0
        for row in self.grid:
            if row[column] == " . ":
                row[column] = " O "
                self.row = index
                break
            index += 1

    def print_grid(self):
        print("   1  2  3  4  5  6  7")
        print("+ - - - - - - - - - - - +")
        index = -1
        while index >= len(self.grid)*-1:
            print(f"| {"".join(self.grid[index])} |")
            index -= 1
        print("+ - - - - - - - - - - - +")
        print("")
    
    def check_horizontal_win(self, symbol: str):
        for row in self.grid:
            row = "".join([item.strip() for item in row])
            if f"{symbol*4}" in row:
                return True
        return False
    
    def check_vertical_win(self, symbol: str, column: int):
        column_check = "".join([row[column].strip() for row in self.grid])
        return f"{symbol*4}" in column_check
    
    def check_diag_left_win(self, symbol: str, row: int, col: int):
        cells = []
        #find lowest cell
        while row > 0 and col > 0:
            row -= 1
            col -= 1
        #add all diag cells
        while row <= 5 and col <= 6:
            cells.append(self.grid[row][col])
            row += 1
            col += 1

        if f"{symbol*4}" in "".join([item.strip() for item in cells]):
            return True
        return False
    
    def check_diag_right_win(self, symbol: str, row: int, col: int):
        cells = []
        #find lowest right cell
        while row > 0 and col < 6:
            row -= 1
            col += 1
        #add all diag cells
        while row <= 5 and col >= 0:
            cells.append(self.grid[row][col])
            row += 1
            col -= 1

        if f"{symbol*4}" in "".join([item.strip() for item in cells]):
           return True
        return False


class Main:
    def __init__(self):
        self.game = ConnectFour()

    def check_input(self, input: str):
        try:
            input = int(input)
            if input in range(1, 8):
                return True
            print("Invalid input")
            return False
        except ValueError:
            print("Invalid input")
            print("")
            return False
        
    def p1_turn(self):
        print("")
        print("Type in Column 1-7")
        p1_col = (input("Player 1: "))
        while not self.check_input(p1_col):
            p1_col = (input("Player 1: "))
        p1_col = int(p1_col) - 1
        self.game.place_x(p1_col)
        self.game.print_grid()
        if self.check_win("X", p1_col):
            print("Player 1 wins!")
            return True
    
    def p2_turn(self):
        print("")
        print("Type in Column 1-7")
        p2_col = (input("Player 2: "))
        while not self.check_input(p2_col):
            p2_col = (input("Player 2: "))
        p2_col = int(p2_col) - 1
        self.game.place_o(p2_col)
        self.game.print_grid()
        if self.check_win("O", p2_col):
            print("Player 2 wins!")
            return True

    def check_win(self, symbol: str, column: int):
        if self.game.check_horizontal_win(symbol) or self.game.check_vertical_win(symbol, column) or self.game.check_diag_left_win(symbol, self.game.row, column) or self.game.check_diag_right_win(symbol, self.game.row, column):
            return True
        return False

    def run(self):
        self.game.print_grid()
        while True:
            if self.p1_turn():
                break

            if self.p2_turn():
                break


Main().run()