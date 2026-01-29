import sys
import pygame
import random

from blcks import Blocks # Accessing the Blocks class from the blcks.py file using an import.

class Game():
    
    def __init__(self): # Initializes the Game class.
        
        pygame.init() # Initializes pygame and necessary for all pygame code to function.

        self.screen_size = (401, 801) # Screen size in a 401x801 pixel size, this includes the game board and the header.

        self.game_size = (401, 721) # The size of the actual game board not including the header.

        self.random_color_tuple = (random.randint(0, 255), random.randint(0,255), random.randint(0,255)) # Random color for the Header of the game.

        self.display_background_color = (0,0,0)

        self.grid_color = (150, 150, 150)

        self.game_FPS = 60 #Used to decide how many times the screen will update within a second.

        self.display = pygame.display.set_mode(self.screen_size) # Used to refer to  display whenever we want to update the screen with new pixels.

        self.clock = pygame.Clock() 

        self.current_tick = pygame.time.get_ticks() #We use this later on to add delays for Tetrominos falling.

        self.last_title_tick = 0 # We use this to set a delay for the title to change colors.

        self.last_block_tick = 0 # Once this variable goes above the specified threshold, we update this variable to reflect the current tick. Essentially this keeps track of the time between the last time the Tetromino fell down 1 block.

        self.default_fall_delay = 500 # This is the threshold i mentioned previously.

        self.fall_delay = self.default_fall_delay # We use this variable as a proxy for the previous variable In cases where the player presses "S" making the delay shorter and the block fall faster.

        self.fall_speed_multiplier = 10 # This value is the going to be the denominator for the self.default_fall_delay division to calculate the self.fall_delay.

        self.game_score = 0

        self.grid = {i: {j: 0 for j in range(10)} for i in range(20)} # Sets up a dictionary that keeps track of block positions on the game board internally, There are 10 columns and 20 rows, though the first 2 rows are not visible because they lack graphical outlines.

        self.shapes = {0: Blocks.Square, 1: Blocks.Line, 2: Blocks.L_shape_L, 3: Blocks.T_shape, 4: Blocks.Z_shape_L, 5: Blocks.Z_shape_R, 6: Blocks.L_shape_R} # Predetermined shapes that are selected at random to be deployed on start or if there are no active shapes on the game.

        self.shape_colors = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255), 3: (200, 200, 0), 4: (0, 255, 255), 5: (255, 0, 255)} # Predetermined shape colors.

        self.current_shape = None #Keeps track of the active shape falling on the screen.

        self.tile_size = 40 #In pixels. Used to snap blocks onto the graphical game grid.

        self.starting_row_column = [-3, 4] #This is the position in which each shape will spawn at.

        self.shapes_on_screen = [] # Keeps track of all shapes on the screen including the active Tetromino. A list which holds a shape class and its respective color.

        self._display() #Calls unto the display function to officially start the game.

    def _display(self):
        
        while True: # A while loop is used because we want our game to run forever unless the program is exited by the user.
            
            self.event_handler() # This must be the 1st function called because it is the core of the program as it handles user inputs for Tetromino rotation and "S" key presses and handles closing the program.

            self.display.fill(self.display_background_color) # This is the first layer of pixels on the screen and used to set up our background.

            self.draw_shapes(self.display) # Shapes are drawn second because we want the grid outline to appear ontop of shapes for visual aesthetics.

            self.draw_grid(self.display) # Handles drawing the grid as the 3rd layer.
            
            self.header_text() # Updates the score and header color continously.

            self.shape_logic() # Backbone of all shape movement, collision, and row clears.

            self.current_tick = pygame.time.get_ticks() # We continously update this variable so that we can calculate how much time has passed before a Tetromino is able to fall.

            self.clock.tick(self.game_FPS) # This allows us to update the display 60 times in a second, or however much the value self.game_FPS is set to.

            pygame.display.update() # Updates the display.

    def rows_cleared_logic(self):
         
         rows_cleared = [] # We use a list to hold any possible row clears and can calculate how many have been cleared.

         b_anchor_row, b_anchor_column = self.current_shape.row, self.current_shape.column # We use this to update a shapes row if rows have been cleared under it.

         for row in self.grid: # This for loop iterated through each row in self.grid, then iterates again through each column in that row, if all columns in that row have a state of 1 then we know it is filled and we can clear that row.
              
              for column in self.grid[row]:
                   
                   if self.grid[row][column] == 1:
                        
                        continue
                   else: 
                        
                        break
              else:
                   
                   rows_cleared.append(row)
         
         if len(rows_cleared) == 0: # If no rows have been cleared then we simply return 0
              
              return 0

         for row in range(20): # We reset the grid to prevent any confusion and errors.
               
               for col in range(10):

                    self.grid[row][col] = 0

         for (shape, color) in self.shapes_on_screen: # We iterate through all shapes on the screen and we get rid of any blocks that were in the cleared row.
               
               new_shape = [(r_off, c_off) for (r_off, c_off) in shape.shape if (shape.row + r_off) not in rows_cleared] # When trying to optimize this line i believed that using shape.blocks() would work because it would take out the added math of adding the shapes anchor row to the offset but this will not work because on line 113 we must set the shapes offsets to a new list of offsets the reflect the cleared row rather than block positions.

               shape.shape = new_shape # Set the new shapes offset once we clear any of the Tetromino's piece's that were part of any cleared rows.
          
         self.shapes_on_screen = [ (shape, color) for (shape, color) in self.shapes_on_screen if len(shape.blocks()) > 0] # We get rid of any shapes from this list if they have 0 blocks.
                         
         for (shape, color) in self.shapes_on_screen: # This is the logic for making Tetromino's fall.
               
               shape_rows = [row for (row, column) in shape.blocks()] # We gather all of the shape's current rows.

               if len(shape_rows) > 0: # Verify that the shape has atleast 1 row.

                    rows_cleared_under = [cleared_row for cleared_row in rows_cleared if cleared_row > max(shape_rows)] # This is a list of the cleared rows which are lower than the shapes lowest row.

                    if len(rows_cleared_under) > 0: # If there has been any rows cleared under the Tetromino's lowest row then we proceed by looping through an enumerated list of the shapes' blocks and looking at which specific blocks have cleared rows under them.

                         for index, (r, c) in enumerate(shape.blocks()):

                              for cleared_row in rows_cleared_under:

                                   if r < cleared_row:

                                        r_offset = r - shape.row
                                        c_offset = c - shape.column

                                        shape.shape[index] = (r_offset + len(rows_cleared_under), c_offset)

                    # Now we need to handle when a a cleared row is between a Tetromino using the same logic.

                    rows_cleared_between = [cleared_row for cleared_row in rows_cleared if cleared_row > min(shape_rows) and cleared_row < max(shape_rows)]

                    if len(rows_cleared_between) > 0:

                         for index, (r, c) in enumerate(shape.blocks()):

                              for cleared_row in rows_cleared_between:

                                   if r < cleared_row:

                                        r_offset = r - shape.row
                                        c_offset = c - shape.column

                                        shape.shape[index] = (r_offset + len(rows_cleared_between) , c_offset)


               for (r, c) in shape.blocks(): # Finally we can configure the game grid to reflect all of the Tetrominos on screen.

                    if r <= 19:
                     
                         self.grid[r][c] = 1
        
         return len(rows_cleared)*(10*len(rows_cleared)) # If rows were cleared then we can add these points to the players score.

    def shape_logic(self):

         if not self.current_shape: # Passes if there are no active shapes on the screen.

            self.current_shape = random.choice(self.shapes)(*self.starting_row_column) # We choose a random predetermined shape to use as our new current shape. The shape is then spawned at the default row and column.
            
            if self.block_collision(0, 0): # If there is a block collision when trying to spawn then we will end the game.

                print("Collided trying to spawn inside another block")

                pygame.quit()

                sys.exit()
            
            self.shapes_on_screen.insert(0, (self.current_shape, random.choice(self.shape_colors))) # This line executes if there was no block collision, we insert the new active shape onto the self.shapes_on_screen list with its respective random color.

         if self.current_shape: # Passes if there is an active shape on the screen.
                
                b_anchor_row, b_anchor_column = self.current_shape.row, self.current_shape.column # Current block anchor row and anchor column.

                mousepos_test_column = pygame.mouse.get_pos()[0]//self.tile_size # This is a test column we determine from the mouse position to test for block collision.

                test_row = self.current_shape.row+1 # This is a test of the row right below the block, if it passes collision tests then we can move the block down by 1 grid.
                
                predicted_column_shift = 0 # Using this value we can test for collisions and boundaries on movements a player wants to make.

                if mousepos_test_column > b_anchor_column: # If the mouse column is greater than the block's anchor column then we know the user is trying to move the block to the right so the predicted_column_shift is 1 block to the right of the Tetromino's anchor position.
                     
                     predicted_column_shift = 1

                elif mousepos_test_column < b_anchor_column: # If the mouse column is greater than the block's anchor column then we know the user is trying to move the block to the left so the predicted_column_shift is -1 block to the left of the Tetromino's anchor position.
                     
                     predicted_column_shift = -1

                if (self.current_tick-self.last_block_tick) > self.fall_delay: # We subtract the current tick from the last time the block fell to calculate how long has passed, if it is longer than the fall delay then we can let the block fall 1 grid position.

                    if not self.block_collision(1, 0) and all(r <= 19 for (r, c) in self.current_shape.blocks_at(test_row, b_anchor_column)): # We simulate the blocks anchor position being the test_row to calculate any possible collisions or if any of the blocks are out of bounds.
                            
                            self.last_block_tick = self.current_tick # We reset the tick once we know that the block is within bounds without any collisions

                            b_anchor_row += 1 # We can now update the block's real anchor row.

                            self.current_shape.set(b_anchor_row, b_anchor_column) # We set the new anchor row and column internally as well so that we can keep track of these positions.

                    else: # In the case where the test row has a collision with another Tetromino or is out of bounds.

                        if not all(r > 1 for (r,c) in self.current_shape.blocks()): # Tests if all rows in a Tetromino's pieces are within the grid's bounds. If not then we end the game.

                            print("Tried to spawn/place outside of the grid")

                            pygame.quit()

                            sys.exit()

                        for (r,c) in self.current_shape.blocks(): # We iterate through all of the Tetromino's piece's real time position and update the grid to match this.
                             
                             if r <= 19 and r > 1:

                                self.grid[r][c] = 1
                        
                        self.game_score += self.rows_cleared_logic() # Calculate if any rows have been cleared and returns the amount of points earned.

                        self.current_shape = None # Since the Tetromino has been placed and any necessary rows have been cleared we can now start with a new shape.
                
                if self.current_shape: # This part handles the Tetromino's column position and tests the player's wanted shift. We need to make sure that we still currently have an active block to avoid any errors.
                     
                     if not self.block_collision(0, predicted_column_shift) and all(0 <= c <= 9 for (r, c) in self.current_shape.blocks_at(b_anchor_row, b_anchor_column+predicted_column_shift)): # Makes sure the wanted shift is within bounds and that there are no collisions.

                        b_anchor_column += predicted_column_shift # Update its real time anchor column.

                        self.current_shape.set(b_anchor_row, b_anchor_column) # Update the shapes internal row and column.
    
    def block_collision(self, test_row_predicted_column_shift, mousepos_test_column_predicted_column_shift): # We simply iterate through the shape's blocks at a test predicted_column_shift and see if that test position is already taken by another Tetromino on the grid. If not we return True.
         
          shape_blocks = self.current_shape.blocks_at(self.current_shape.row + test_row_predicted_column_shift, self.current_shape.column + mousepos_test_column_predicted_column_shift) # This function is embedded in the block class and returns a list of tuples which hold a test shape position in the game in rows and columns for each block. Ex: [(r_0,c_0),(r_1,c_1), ...]

          for (r, c) in shape_blocks:

               if r >= 1 and c >= 0 and r <= 19 and c <= 9:

                    if self.grid[r][c] == 1:

                         return True
               
          return False

         # From Lines 206 - 226 this is the Old code that was used to detect block collison, but while updating my entire program to have comments It helped me think more logically and realize this section could be massively optimized from a triple nested for loop.

         #for (shape, color) in self.shapes_on_screen:
                
                #if shape == self.current_shape:
                     
                     #continue
                
                #for (_r, _c) in shape.blocks():
                          
                     #for (r, c) in self.current_shape.blocks():
                          #if test:
                            #if (_r, _c) == (r+test_row_predicted_column_shift, c+mousepos_test_column_predicted_column_shift):

                                #return True
                          #if not test:
                            #if (_r, _c) == (r, c):

                                #return True
                 
         #return False

    def shape_fits(self, test_shape, row, column): # We iterate through each offset in the proposed rotated shape making sure none of the pieces are out of bounds and not colliding with other Tetrominos. Returns True if all tests pass.
         
         for (r_off, c_off) in test_shape:
              
              r = row + r_off

              c = column + c_off

              if not (0 <= c <= 9) or not (r <= 19):
                   
                   return False
              
              if (r >= 0 and self.grid[r][c] == 1):
                   
                   return False
              
         return True

    def kick_logic(self, rotated_shape): # The rotated_shape argument is a 90 degree clockwise rotation of the shape that does not reflect the actual current shape but instead used to test whether this rotation is viable.
         
         kicks = [                 # A large list of tuples each reflecting a possible offset from the test shapes anchor position. The anchor position refers to the shapes absolute position on the grid not account for the pieces not in the anchor position.
              (0, 0), (0, -1), 
              (0, -2), (0, -3), 
              (0, 1), (0, 2), 
              (0, 3),
              ]
         
         for (r,c) in kicks: # We iterate through each kick offset tuple on the list to find a viable offset we can kick the test shape by where it won't be out of bounds or colliding with other shapes.
              
              shape_fits = self.shape_fits(rotated_shape, self.current_shape.row + r, self.current_shape.column + c)  # Checking the test shape is within bounds and returns true if no collisions.

              if shape_fits:
                   
                   return (r, c)
              
         return None # If the test shape is colliding or outside of the border then we cannot 

    def rotation_logic(self): # The logic we use for rotation split into steps in which we first create a test shape which is a 90 degree rotation of the current active shape and use that to determine if we can actually rotate the shape or if we must kick it first to ensure it is within bounds and not making any collisions with other Tetrominos.
         
         rotated_shape = self.current_shape.rotated_offset() # Calls onto the function embedded in the block's class.

         kick = self.kick_logic(rotated_shape) # If there is a viable kick offset then the shape is kicked by however much that offset is when rotating.

         if kick: # Checking if we can kick the shape
              
              dr, dc = kick

              if self.current_shape: # Checking if there is a current active shape on the screen
                
                self.current_shape.set(self.current_shape.row + dr, self.current_shape.column + dc) # We can now proceed by updating the current shapes position offset to the succesful kick offset

                self.current_shape.rotate(rotated_shape) # We update the current shape with its new rotation aswell.
    
    def key_handler(self): # Descendant from the event_handler function and specifcally handles when a key is held down for a period of time.
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]: # Verify the key being pressed is the "S" key.
            
            self.fall_delay = self.default_fall_delay/self.fall_speed_multiplier # Updates the Tetromino fall delay to reflect the key being pressed.

        elif not keys[pygame.K_s]:
            
            self.fall_delay = self.default_fall_delay # Once the key press has ended we can use the self.default_fall_delay to revert back to the default delay.

    def event_handler(self): # Handles event requests from the user.
        
        for event in pygame.event.get(): # Every frame we iterate through each event request from the user.
                
                if event.type == pygame.QUIT: # If the X is pressed at the top right of the screen, we close the program.

                    pygame.quit()

                    sys.exit()

                if event.type == pygame.KEYDOWN: # We first check if the event is a downward key press.
                     
                     if event.key == pygame.K_r and self.current_shape: # Then we verify that the key that was pressed down was the R key and that there is a current active shape on the screen to make rotation possible.
                          
                          self.rotation_logic()
                                     
        self.key_handler() # We put this outside of the event request loop because I want this to handle when the "S" key is held down.
    
    def draw_shapes(self, surface): # Iterates through all shapes on the screen and draws them on the display.
         
         for (shape, color) in self.shapes_on_screen:
                
                for (r, c) in shape.blocks():

                    x, y = c*self.tile_size, r*self.tile_size
                
                    pygame.draw.rect(surface, color, (x, y, self.tile_size, self.tile_size))
    
    def draw_grid(self, surface): # Draws the game grid.
        for x in range(0, self.game_size[0]+self.tile_size, self.tile_size):
            pygame.draw.rect(surface, self.grid_color, (x, 80, 1, self.game_size[1])) 
                    
        for y in range(80, self.game_size[1]+self.tile_size, self.tile_size):
            pygame.draw.rect(surface, self.grid_color, (0, y, self.game_size[0], 1))
        
    def header_text(self): # Handles the score count and title.
     
        header_font = pygame.font.SysFont("impact", 32)

        header_render = header_font.render("Tetris", True, self.random_color_tuple)

        header = self.display.blit(header_render, ((self.screen_size[0]/2)-(header_render.get_width()/2), 10))
        
        if (self.current_tick - self.last_title_tick) > 600: # We subtract the current tick and the last title tick to find out how much time has passed between the two. If it is greater than 600 then we know enough delay has passed so that we can update the color of the title.
                
                self.last_title_tick = self.current_tick

                self.random_color_tuple = (random.randint(0, 255), random.randint(0,255), random.randint(0,255))

        score_font = pygame.font.SysFont("impact", 24)

        score_render = score_font.render(f"Score: {self.game_score}", True, (255,255,255))

        score = self.display.blit(score_render, (10, 40))        

if __name__ == "__main__": # This is necessary to start the game.
    
    Game()