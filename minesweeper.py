import random
import datetime


class Saper():
    '''Game minesweeper'''

    used_squares = []                                      # used squares while game

    def __init__(self, n, number_of_mines):
        self.n = n                                         # number of columns and rows
        self.fields = self.n ** 2                          # number of squares
        self.number_of_mines = number_of_mines             # number of mines
        self.board = ['   ' for i in range(self.fields)]   # clean board
        self.board_game = self.board.copy()                # board to update on game
        self.win = False


    def print_board(self, board):
        '''Print clean board to game or board with mines and numbers.'''

        print()
        print('    ' + '| '.join(str(i).zfill(2) for i in list(range(1, self.n + 1))))  # 0 | 1 | 2 | 3...
        print('---' + '----' * self.n)
        #for n, row in enumerate([self.board[i*10:(i+1)*10] for i in range(10)]):
        for k, row in enumerate([board[i*self.n:(i+1)*self.n] for i in range(self.n)], start=1):
            print(f"{str(k):2s}|{'|'.join(row)}|")
        print()


    def make_mines(self):
        '''Make mines in board.'''

        global mines
        mines = random.sample(list(range(self.fields)), self.number_of_mines)
        for i in mines:
            self.board[i] = ' * '


    def near_indexes(self, x):
        '''Indexes of near squares.'''

        if 1 <= x <= self.n-2:  # top horizontal (without corners)
            #near_indexes = [-1, 1, 9, 10, 11]  # for 10x10 board
            near_indexes = [-1, 1, self.n-1, self.n, self.n+1]

        #elif x in [19, 29, 39, 49, 59, 69, 79, 89]:
        elif x in list(range(2*self.n-1, self.fields-1, self.n)):  # right vertical (without corners)
            #near_indexes = [-11, -10, -1, 9, 10]  # for 10x10 board
            near_indexes = [-self.n-1, -self.n, -1, self.n-1, self.n]

        #elif x in [10, 20, 30, 40, 50, 60, 70, 80]:
        elif x in list(range(self.n, self.fields-self.n, self.n)):  # left vertical (without corners)
            #near_indexes = [-10, -9, 1, 10, 11]  # for 10x10 board
            near_indexes = [-self.n, -self.n+1, 1, self.n, self.n+1]

        #elif 91 <= x <= 98:
        elif self.fields+1-self.n <= x <= self.fields-2:  # down horizontal (without corners)
            #near_indexes = [-11, -10, -9, -1, 1]  # for 10x10 board
            near_indexes = [-self.n-1, -self.n, -self.n+1, -1, 1]

        elif x == 0:  # top left corner
            #near_indexes = [1, 10, 11]  # for 10x10 board
            near_indexes = [1, self.n, self.n+1]

        elif x == self.n-1:  # top right corner
            #near_indexes = [-1, 9, 10]  # for 10x10 board
            near_indexes = [-1, self.n-1, self.n]

        elif x == self.fields-self.n: # down left corner
            #near_indexes = [-10, -9, 1]  # for 10x10 board
            near_indexes = [-self.n, -self.n+1, 1]

        elif x == self.fields-1:  # down right corner
            #near_indexes = [-11, -10, -1]  # for 10x10 board
            near_indexes = [-self.n-1, -self.n, -1]

        else:
            #near_indexes = [-11, -10, -9, -1, 1, 9, 10, 11]  # for 10x10 board
            near_indexes = [-self.n-1, -self.n, -self.n+1, -1, 1, self.n-1, self.n, self.n+1]

        return near_indexes


    def count_near_mines(self):
        '''Count mines near the every square.'''

        for r in range(self.fields):
            near_indexes = self.near_indexes(r)
            counter = 0
            near_list = []
            for e in near_indexes:
                near_list.append(self.board[r+e])
            for j in near_list:
                if j == ' * ':
                    counter += 1
            if self.board[r] != ' * ':
                self.board[r] = f' {str(counter)} '


    def choose_square(self):
        '''User choose square'''

        valid_square = False
        while not valid_square:
            user = input('Choose square (row, column): ')
            try:
                user_s = user.split(',')
                row = int(user_s[0])
                column = int(user_s[1])
                val = (row - 1) * self.n + column - 1
                #print(val)
                if val not in list(range(self.fields)) or val in self.used_squares:
                    raise ValueError
                valid_square = True
                self.used_squares.append(val)
            except Exception:
                print('Invalid square. Try again.')
        if self.board[val] == ' * ':
            self.board_game[val] = '!*!'
            self.used_squares.clear()
            print('You lose.')
        return val


    def check_square(self, square):
        '''Check square (mine, near mine, empty).'''

        if self.board[square] in [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ']:
            self.board_game[square] = self.board[square]
            self.used_squares.append(square)
        elif self.board[square] == ' 0 ':
            self.board_game[square] = self.board[square]
            self.used_squares.append(square)
            near_indexes = self.near_indexes(square)

            for n in near_indexes:
                if self.board_game[square + n] not in [' 0 ', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ']:
                    try:
                        self.check_square(square + n)
                    except IndexError:
                        print('Error')

    def winner(self):
        '''Check used squares and they number.'''

        if len(self.used_squares) != 0:
            if self.used_squares[-1] not in mines and self.board_game.count('   ') == self.number_of_mines:
                print('CONGRATULATIONS, YOU WIN!!!!')
                self.print_board(self.board)
                self.win = True
                self.used_squares.clear()
                return self.win



def play(game):
    game.make_mines()
    game.count_near_mines()
    #game.print_board(game.board)  # to check
    game.print_board(game.board_game)
    global moves, time_delta
    moves = 0
    while '!*!' not in game.board_game and game.win == False:
        game.check_square(game.choose_square())
        game.print_board(game.board_game)
        game.winner()
        moves += 1
        if moves == 1:
            time_start = datetime.datetime.now()

    time_stop = datetime.datetime.now()
    time_delta = (time_stop - time_start).seconds

    if game.win == True:
        print(f'Your time: {time_delta} seconds. Number of moves: {moves}.')
    print('Thank You for a game!')



if __name__ == '__main__':
    game_easy = Saper(4, 2)
    play(game_easy)



