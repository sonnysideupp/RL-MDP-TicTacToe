import json
import turtle


class TicTacToeGUI:
    def __init__(self, agent = "ValueIteration"):
        self.current_player = "X"
        self.board = (0,) * 9
        self.is_vs_computer = False  # Flag to check if playing against the computer
        self.computer_symbol = "O"   # Symbol for the computer player
        self.agent = agent
        self.policy = {}
        if self.agent == "ValueIteration":
            path = "value_iteration/policy.json"
        elif self.agent == "PolicyIteration":
            path = "policy_iteration/policy.json"
        with open(path, 'r') as json_file:
                # open json file as dictionary
                self.policy = json.load(json_file)

        # Calculate the window position to center it on the screen
        screen = turtle.Screen()
        screen.setup(800,800)
        screen.setworldcoordinates(-500,-500,500,500)
        screen.title("Tic Tac Toe")
        turtle.speed(0)
        turtle.hideturtle()
        screen.tracer(0,0)
        score = turtle.Turtle()
        score.up()
        score.hideturtle()
        self.screen = screen
        self.ROWS = self.COLS = 3
        self.STARTX = self.STARTY = -450
        self.WIDTH = -2*self.STARTX
        self.HEIGHT = -2*self.STARTY
        self.turn=1
        self.working=False
        print("init successful")
    def draw_rectangle(self, x,y,w,h,color):
        turtle.up()
        turtle.goto(x,y)
        turtle.seth(0)
        turtle.down()
        turtle.fd(w)
        turtle.left(90)
        turtle.fd(h)
        turtle.left(90)
        turtle.fd(w)
        turtle.left(90)
        turtle.fd(h)
        turtle.left(90)
        row_gap = self.HEIGHT/self.ROWS
        col_gap = self.WIDTH/self.COLS

        for col in range(self.COLS - 1):
            turtle.up()
            turtle.goto(x + (col + 1) * col_gap, y)
            turtle.seth(90)
            turtle.down()
            turtle.fd(h)
        for row in range(self.ROWS - 1):
            turtle.up()
            turtle.goto(x, y + (row + 1) * row_gap)
            turtle.seth(0)
            turtle.down()
            turtle.fd(w)        
  
    def draw_circle(self,x,y,r,color):
        turtle.up()
        turtle.goto(x,y-r)
        turtle.seth(0)
        turtle.down()
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.circle(r,360,150)
        turtle.end_fill()
    def draw_X( self, x,y):
        turtle.up()
        turtle.goto(x - 40,y - 40)
        turtle.seth(0)
        turtle.left(45)
        turtle.down()
        turtle.forward(150)
        turtle.back(75)
        turtle.left(90)
        turtle.forward(75)
        turtle.backward(150)
        # turtle.done()
    def init_board(self):
        board = []
        for _ in range(self.ROWS):
            # row = []
            for _ in range(self.COLS):
                board.append(0)
            # board.append(row)
        self.board = board
    def draw_pieces(self):
 
        row_gap = self.HEIGHT/self.ROWS
        col_gap = self.WIDTH/self.COLS
        
        for i in range(self.ROWS):
            Y = self.STARTY + row_gap / 2 + (self.ROWS - 1 - i) * row_gap
            for j in range(self.COLS):
                X = self.STARTX + col_gap/2 + j * col_gap
                if self.board[i * self.ROWS + j] == 0:
                    pass
                elif self.board[i * self.ROWS + j] == 1:
                    self.draw_circle(X,Y,row_gap/3,'black')
                else:
                    self.draw_X(X,Y)

    def draw_board(self):
        self.draw_rectangle(self.STARTX,self.STARTY,self.WIDTH,self.HEIGHT,'light blue')
    def draw(self):
        self.init_board()
        self.draw_board()
        # self.draw_pieces()
        self.screen.update()

    def coordiate_to_index(self, x, y):
        row_gap = self.HEIGHT/self.ROWS
        col_gap = self.WIDTH/self.COLS
        col = 0
        col_threshold = self.STARTX + col_gap
        while col_threshold < x:
            col += 1
            col_threshold += col_gap
        row = self.ROWS - 1
        row_threshold = self.STARTY + row_gap
        while row_threshold < y:
            row -= 1
            row_threshold += row_gap
        
        return (row, col)
    
    def play(self, x,y):
        # if self.working: return
        # self.working = True
        print("clicking", x, y)
        (row, col) = self.coordiate_to_index(x,y)
        self.board[row * self.ROWS + col] = 2
        self.draw_pieces()
        self.make_computer_move()
        self.draw_pieces()
        self.screen.update()
        if self.check_win() or self.check_tie():
            self.end_game()



    def make_move(self, idx):
        if idx == None:
            pass
        elif self.board[idx] == 0:
            self.board[idx] = 1

            


    def make_computer_move(self):
        # Get the current state of the board
        state = tuple(self.board)
        # ivert X and O if computer is O
        # if self.computer_symbol == "O":
        #     state = tuple(3-x if x!= 0 else 0 for x in state)
        self.make_move(self.policy[str(state)])

    def check_win(self):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for combo in win_combinations:
            a, b, c = combo
            print("self.board", self.board)
            if (
                self.board[a] == self.board[b] == self.board[c]
                and self.board[a] != 0
            ):
                turtle.TK.messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                return True
        return False

    def check_tie(self):
        if 0 not in self.board:
            turtle.TK.messagebox.showinfo("Game Over", "It's a tie!")
            return True
        return False

    def end_game(self):

        self.screen.clear()
        self.restart_game()

    def restart_game(self):
        # self.screen.bye()
        self.__init__()
        self.draw()
        self.start()
        #self.start_game("X")

    def start(self):
        self.screen.onclick(game.play)
        self.screen.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI("PolicyIteration")
    game.draw()
    game.start()