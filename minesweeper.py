from PIL import Image
import random
class Sapper():
    def __init__(self, size = 10, bombs=15, img_dir='img/', covered_tile='covered_tile.png', empty_tile='empty_tile.png', bomb_tile='bomb_tile.png'):
        assert bombs <= size**2, 'too many bombs'
        self.bombs = bombs
        self.img_dir = img_dir
        self.size = size
        self.covered_tile = img_dir + covered_tile
        self.empty_tile = img_dir + empty_tile
        self.bomb_tile = img_dir + bomb_tile
        self.num_tiles = [img_dir + str(i+1) + '_tile.png' for i in range(10)]
        self.letter_tiles = [img_dir + chr(i+65) + '_tile.png' for i in range(10)]
        self.field_img = self.new_field()
        self.field_covered = [
            [True for i in range(size)] for j in range(size)    # all tiles are covered at the start
        ]
        self.field_tab = self.new_field_tab(bombs)
    
    def get_covered_tile(self):
        return Image.open(self.covered_tile)
    
    def get_empty_tile(self):
        return Image.open(self.empty_tile)
    
    def get_bomb_tile(self):
        return Image.open(self.bomb_tile)
    
    def get_num_tiles(self):
        return [Image.open(el) for el in self.num_tiles]
    
    def get_letter_tiles(self):
        return [Image.open(el) for el in self.letter_tiles]
    
    def get_tile_size(self):
        return self.get_covered_tile().size
    
    def update_field_img(self):
        tile_size = self.get_tile_size()
        for row in range(len(self.field_tab)):
            for el in range(len(self.field_tab[row])):
                if self.field_covered[row][el]:
                    self.field_img.paste(self.get_covered_tile(), (tile_size[0]*(row + 1) + 1, tile_size[1]*(el + 1) + 1))
                else:
                    self.field_img.paste(self.field_tab[row][el], (tile_size[0]*(row + 1) + 1, tile_size[1]*(el + 1) + 1))
    
    def display_game(self):
        self.update_field_img()
        display(self.field_img)
        
    def uncover_field(self):
        size = self.size
        self.field_covered = [
            [False for i in range(size)] for j in range(size)    # all tiles are uncovered now
        ]
    
    def cover_field(self):
        size = self.size
        self.field_covered = [
            [True for i in range(size)] for j in range(size)    # all tiles are covered now
        ]
    
    def how_much_bombs(self, xy, field):
        size = self.size
        t = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        x, y = xy
        bomb = self.bomb_tile
        bombs = 0
        for i in t:
            if ((x+i[0] >= size) or (x+i[0] < 0) or (y+i[1] >= size) or (y+i[1] < 0)):
                continue
            if field[x+i[0]][y+i[1]] is None:
                continue
            if field[x+i[0]][y+i[1]].filename == bomb:
                bombs += 1
        return bombs
    
    def new_field(self):
        size = self.size
        
        assert size<=10 and size>=1, 'Field size must be >=1 and <=10'
        
        covered_tile = self.get_covered_tile()
        tile_size = self.get_tile_size()
        num_tiles = self.get_num_tiles()
        letter_tiles = self.get_letter_tiles()
        
        row = Image.new('RGB', (tile_size[0]*(size + 1), tile_size[1])) # one row
        field = Image.new('RGB', (tile_size[0]*(size + 1) + 4, tile_size[1]*(size + 1) + 4)) # whole field
        
        for i in range(size):
            row.paste(num_tiles[i], (tile_size[0]*(i + 1), 0))  # first row
        field.paste(row, (1, 1))
        
        
        for i in range(size):
            row.paste(letter_tiles[i], (0, 0))
            
            for j in range(size):
                row.paste(covered_tile, (tile_size[0]*(j + 1), 1))
            field.paste(row, (1, tile_size[1]*(i + 1) + 1))
            
        return field
    
    def new_field_tab(self, bombs):
        size = self.size
        field = [
            [None for i in range(size)] for j in range(size)
        ]
        bomb_tile = self.get_bomb_tile()
        empty_tile = self.get_empty_tile()
        num_tiles = self.get_num_tiles()[:8]
        bomb_pos = [(random.randint(0, size - 1), random.randint(0, size - 1))]
        
        for i in range(bombs - 1):
            pos = (random.randint(0, size - 1), random.randint(0, size - 1)) # (x, y)
            while pos in bomb_pos:
                pos = (random.randint(0, size - 1), random.randint(0, size - 1))
            bomb_pos.append(pos)
        
        for pos in bomb_pos:
            x = pos[0]
            y = pos[1]
            field[y][x] = bomb_tile
        
        
        for row in range(size):
            for el in range(size):
                if field[row][el] is None:
                    bombs_number = self.how_much_bombs((row, el), field)
                    if bombs_number == 0:
                        field[row][el] = empty_tile
                    else:
                        field[row][el] = num_tiles[bombs_number-1]
        return field
    
    def uncover_tiles(self, xy):
        size = self.size
        field = self.field_tab
        x, y = xy
        t = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        assert self.field_covered[x][y], 'This tile is already uncovered.'
        self.field_covered[x][y] = False
        if self.field_tab[x][y].filename == self.bomb_tile:
            self.game = False
            return -1
        
        if self.field_tab[x][y].filename in self.num_tiles:
            self.update_field_img()
            return 0
        
        for i in t:
            new_x = x + i[0]
            new_y = y + i[1]
            if ((new_x >= size) or (new_x < 0) or (new_y >= size) or (new_y < 0)):
                continue
            if not self.field_covered[new_x][new_y]:
                continue
            if self.field_tab[new_x][new_y].filename == self.bomb_tile:
                continue
            if self.field_tab[new_x][new_y].filename in self.num_tiles:
                self.field_covered[new_x][new_y] = False
                continue
            else:
                if abs(i[0]*i[1]) == 1:
                    continue
                self.uncover_tiles((new_x, new_y))
    
    def how_many_covered(self):
        s = 0
        for row in self.field_covered:
            for el in row:
                if el:
                    s += 1
        return s
    
    def mov_to_xy(self, mov):
        if len(mov) < 2 or len(mov) > 3:
            return False
        x = False
        y = False
        if len(mov) == 2:
            if ord(mov[0])>=49 and ord(mov[0])<=57:
                x = int(mov[0]) - 1
            elif ord(mov[0].upper())>=65 and ord(mov[0].upper())<=74:
                y = ord(mov[0].upper()) - 65
            else:
                return False
                    
            if ord(mov[1])>=49 and ord(mov[1])<=57:
                if type(x) == int:
                    return False
                x = int(mov[1]) - 1
            elif ord(mov[1].upper())>=65 and ord(mov[1].upper())<=74:
                if type(y) == int:
                    return False
                y = ord(mov[1].upper()) - 65
            else:
                return False
        else:
            if ord(mov[0].upper())>=65 and ord(mov[0].upper())<=74:
                y = ord(mov[0].upper()) - 65
                if ord(mov[1]) == 49 and ord(mov[2]) == 48:
                    x = 9
                else:
                    return False
            elif ord(mov[2].upper())>=65 and ord(mov[2].upper())<=74:
                y = ord(mov[2].upper()) - 65
                if ord(mov[0]) == 49 and ord(mov[1]) == 48:
                    x = 9
            else:
                return False
        return (x, y)
                
    def play(self):
        self.game = True
        self.win = False
        while self.game:
            self.display_game()
            mov = input('Wybierz pole do odkrycia: ')
            mov = self.mov_to_xy(mov)
            if not mov:
                print('Wprowadzono błędną wartość.')
                continue
            
            try:
                u = self.uncover_tiles(mov)
            except AssertionError as e:
                print(e)
                continue
            
            if u == -1:
                self.game = False
            if self.how_many_covered() == self.bombs:
                self.win = True
                self.game = False
        
        self.display_game()
        
        if self.win:
            print('Gratulacje, wygrałeś!')
        else:
            print('Niestety, nie udało Ci się.')