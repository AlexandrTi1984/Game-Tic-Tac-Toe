import  pygame
from  pygame.locals import *
from os import path
import random

img_dir = path.join(path.dirname(__file__),'img')
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial',28)
windows_size = (450,500)
cell_size = 150
range_lst = [0,1,2]
running = True
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode(windows_size)
pygame.display.set_caption('Tic Tac Tore')

class TicTacToe():
    def __init__(self, table_size):
        self.table_size = table_size
        self.cells_size = table_size / 3
        self.table_space = 20
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append('-')
        self.player = 'X'
        self.winner = None
        self.taking_move = True
        self.running = True
        self.background_color = (255, 174, 66)
        self.table_color = (50, 50, 50)
        self.game_over_bg_color = (47, 98, 162)
        self.game_over_color = (255, 179, 1)
        self.line_color = (190, 0, 10)
        self.instructions_color = (17, 53, 165)
        self.font = pygame.font.SysFont("Courier New", 30)
        self.FPS = pygame.time.Clock()
        self.comp_move = False
        self.name = 'Player'
    def draw_table (self):
        tb_space_point = (self.table_space,self.table_size-self.table_space)
        cell_space_point = (self.cells_size, self.cells_size * 2)
        r1 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[0]],
                              [tb_space_point[1], cell_space_point[0]], 8)
        c1 = pygame.draw.line(screen, self.table_color, [cell_space_point[0], tb_space_point[0]],
                              [cell_space_point[0], tb_space_point[1]], 8)
        r2 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[1]],
                              [tb_space_point[1], cell_space_point[1]], 8)
        c2 = pygame.draw.line(screen, self.table_color, [cell_space_point[1], tb_space_point[0]],
                              [cell_space_point[1], tb_space_point[1]], 8)
    def change_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
            #меняем ходы компьютера
        if self.comp_move == True:
            self.comp_move = False
        else:
            self.comp_move = True

    def move (self, pos):
        try:
            x, y = int(pos[0] // self.cells_size), int(pos[1] // self.cells_size)

            if self.table[x][y] == '-':
                self.table[x][y] = self.player
                self.draw_char(x, y, self.player)
                self.game_chek()
                self.change_player()
        except:
            print('Click inside the table only')
    def draw_char(self, x, y, player):
        if self.player == 'O':
            img = pygame.image.load(path.join(img_dir,'1.png')).convert()
        if self.player == 'X':
            img = pygame.image.load(path.join(img_dir,'2.png')).convert()
        img.set_colorkey(BLACK) # убрать лишний фон с картинки
        img2 = pygame.transform.scale(img, (120, 120))

        screen.blit(img2, (x * self.cells_size+10, y * self.cells_size+10, self.cells_size, self.cells_size))
    def message(self):
        if self.winner is not None:
            screen.fill(self.game_over_bg_color, (10, 445, 450, 35))
            msg = self.font.render(f' {self.name} WINS!', True, self.game_over_color)
            screen.blit(msg, (144, 445))
            self.taking_move = False
        elif not self.taking_move:
            screen.fill(self.game_over_bg_color, (10, 445, 450, 35))
            instructions = self.font.render('Not bad, DRAW!', True, self.game_over_color)
            screen.blit(instructions, (165, 445))
        else:
            screen.fill(self.background_color, (135, 445, 450, 35))
            instructions = self.font.render(f'{self.name} to move', True, self.instructions_color)
            screen.blit(instructions, (165, 445))

    def game_chek(self):
        # vertical check
        for x_index, col in enumerate(self.table):
            win = True
            pattern_list = []
            for y_index, content in enumerate(col):
                if content != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))
            if win == True:
                #print(pattern_list[0], pattern_list[-1])
                self.pattern_strike(pattern_list[0],pattern_list[-1],"vert")
                #self.pattern_strike(pattern_list[0], pattern_list[-1], "ver")
                self.winner = self.name
                self.taking_move = False
                break

        # horizontal check
        for row in range(len(self.table)):
            win = True
            pattern_list = []
            for col in range(len(self.table)):
                if self.table[col][row] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((col, row))
            if win == True:
                #print(pattern_list[0],pattern_list[-1])
                #self.pattern_strike((0,0),(2,0), "hor")
                self.pattern_strike(pattern_list[0],pattern_list[-1],"hor")
                self.winner = self.player
                self.taking_move = False
                break

        # left diagonal check
        for index, row in enumerate(self.table):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self.pattern_strike((0, 0), (2, 2), "left-diag")
            self.winner = self.player
            self.taking_move = False

        # right diagonal check
        for index, row in enumerate(self.table[::-1]):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self.pattern_strike((2, 0), (0, 2), "right-diag")
            self.winner = self.player
            self.taking_move = False

        # blank table cells check
        blank_cells = 0
        for row in self.table:
            for cell in row:
                if cell == "-":
                    blank_cells += 1
        if blank_cells == 0:
            self.taking_move = False


    def pattern_strike(self, start_point, end_point, line_type):
        # gets the middle value of the cell
        mid_val = self.cells_size // 2

        if self.player == 'X':
            self.line_color = (0,0,255)
        else:
            self.line_color = (255,36,0)

        # for the vertical winning pattern
        if line_type == 'vert':
            start_x, start_y = start_point[0] * self.cells_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cells_size + mid_val, self.table_size - self.table_space

            # for the horizontal winning pattern
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[-1] * self.cells_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[-1] * self.cells_size + mid_val

        # for the diagonal winning pattern from top-left to bottom right
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space

        # for the diagonal winning pattern from top-right to bottom-left
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        # draws the line strike
        line_strike = pygame.draw.line(screen, self.line_color, [start_x, start_y], [end_x, end_y], 8)

    def main (self):
        screen.fill(self.background_color)
        self.draw_table()
        # Определяем кто первый ходит, 1 - компьютер
        if int(random.randint(0,1))==1:
            self.comp_move = True
        while self.running:
            self.message()
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False
            if self.comp_move == False:
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.taking_move:
                        self.name = 'Player'
                        self.move(self.event.pos)
            else:
                if self.taking_move == True:
                    comp_do_turn = False
                    # Ставим в центр если свободно
                    if self.table[1][1] == '-':
                        self.move((self.cells_size, self.cells_size))
                        comp_do_turn = True
                        # если есть свободный слот - делаем ход
                    if self.table[0][0] == '-' or self.table[0][1] == '-' or self.table[0][2] == '-' or self.table[1][0] == '-' or self.table[1][1] == '-' or self.table[1][2] == '-' or self.table[2][0] == '-' or self.table[2][1] == '-' or self.table[2][2] == '-' and self.winner == None:
                            while comp_do_turn == False:
                                comp_x = int(random.choice(range_lst))
                                comp_y = int(random.choice(range_lst))
                                if self.table[comp_x][comp_y] =='-':
                                    self.move((comp_x * self.cells_size, comp_y * self.cells_size))
                                    self.name = 'Python Ai'
                                    comp_do_turn = True
                    else:
                            pass
            pygame.display.flip()
            self.FPS.tick(60)

if __name__ == '__main__':
    g = TicTacToe(windows_size[0])
    g.main()

pygame.display.update()
