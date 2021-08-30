import numpy as np
import cv2
import time

TILE_SIZE = 32
MARKET = """
##################
##..............##
##..FB..DS..GW..##
##..FB..DS..GW..##
##..FB..DS..GW..##
##..FB..DS..GW..##
##..FB..DS..GW..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############EE##
""".strip()

class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()
        self.shelves = {'fruits': [[11,14],[2,3,4,5,6]],
                      'spices': [[10], [2,3,4,5,6]],
                      'dairy': [[7], [2,3,4,5,6]],
                      'drinks': [[3,6], [2,3,4,5,6]],
                      'checkout': [[3,7,11],[8]]
                      }

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(6, 11)
        if char == "!":
            return self.extract_tile(1, 0)
        elif char == "E":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        elif char == "W":
            return self.extract_tile(3, 4)
        elif char == "S":
            return self.extract_tile(4, 9)
        elif char == "D":
            return self.extract_tile(6, 12)
        elif char == "G":
            return self.extract_tile(4, 4)
        elif char == "B":
            return self.extract_tile(6, 13)
        elif char == "F":
            return self.extract_tile(3, 13)                  
        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


class Customer:
    
   def __init__(self, supermarket, avatar, row, col):
      """
      supermarket: A SuperMarketMap object
      avatar : a numpy array containing a 32x32 tile image
      row: the starting row
      col: the starting column
      """

      self.supermarket = supermarket
      self.avatar = avatar              #self.extract_tile(6, 14)
      
      self.row = row
      self.col = col
      self.dest_row = None
      self.dest_col = None
      self.image = np.zeros((TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
      self.change_location = np.random.choice([ 'drinks', 'dairy', 'fruits','spices', 'checkout'])
      self.check = self.col == self.dest_col and self.row == self.dest_row
      
      
   def draw(self, frame):
      x = self.col * TILE_SIZE
      y = self.row * TILE_SIZE
      frame[y:y+self.image.shape[0], x:x+self.image.shape[1]] = self.avatar

    # ---> check the self/not self change_location!!
   def move_to_dest(self,change_location,frame):
        self.dest_col = np.random.choice(self.supermarket.shelves[change_location][0])
        self.dest_row = np.random.choice(self.supermarket.shelves[change_location][1])
        print(change_location,'col:', self.dest_col, '  row:', self.dest_row)  
        
        if self.col != self.dest_col and self.row != self.dest_row:
            
            time.sleep(1)
            direction = np.random.choice(['up','down','left','right'])            
            self.move(direction)#,curr_row,curr_col)
            

        else: 
            print('here')
            self.col = self.dest_col
            self.row = self.dest_row

        
   def move(self, direction):#, new_row, new_col):
        new_row = self.row
        new_col = self.col

        if direction == 'up':
            new_row -= 1
        if direction == 'down':
            new_row += 1
        if direction == 'left':
            new_col -= 1
        if direction == 'right':
            new_col += 1

        if self.supermarket.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row
            print('next step:', direction, '----- col:', self.col, '  row:', self.row)


if __name__ == "__main__":

    background = np.zeros((1500, 2100, 3), np.uint8)
    tiles = cv2.imread("tiles.png")         #function reads in the image as a NumPy array, so it can be sliced within the program.

    market = SupermarketMap(MARKET, tiles)
    x = 14 * TILE_SIZE   # 5th column starting from 0
    y = 5 * TILE_SIZE   # 2nd row
    av = tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]
    
 #   customer = Customer(market,market.extract_tile(6, 14),30,29)
    customer = Customer(market,av,10,15)
    
    while True:
        #time.sleep(5)
        #print('REMIIIX')
        frame = background.copy()
        market.draw(frame)
        #print('drawn market')
        customer.draw(frame)
        #€print('draw customer')
        # https://www.ascii-code.com/
        key = cv2.waitKey(1)

        if key == 32: # space bar
            while customer.check == False:
                change_location = np.random.choice([ 'drinks', 'dairy', 'fruits','spices', 'checkout'])
                customer.move_to_dest(change_location,frame)   ##### added market
        
        cv2.imshow("frame", frame) 
        #time.sleep(10)
        # for i in range(10):
        #     change_location = np.random.choice([ 'drinks', 'dairy', 'fruits','spices', 'checkout'])
        #     customer.move_to_dest(change_location)
            
        #     #time.sleep(5)
        #     if key == 113: # 'q' key
        #         break
        # if key == 113: # 'q' key
        #     break

        # if key == 54: # '6' key
        #     customer.move('right')

        # if key == 52: # '4' key
        #     customer.move('left')

        # if key == 56: # '8' key
        #     customer.move('up')

        # if key == 50: # '2' key
        #     customer.move('down')

    
                #method that's displaying each frame on the screen.


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
    
    
    
        
#    def dest_coor(self,change_location):
#         dest_col = np.random.choice(SupermarketMap.shelves[self.change_location][0])
#         dest_row = np.random.choice(SupermarketMap.shelves[self.change_location][1])
