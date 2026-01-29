import pygame
import copy

class Blocks:
    class Square():
        def __init__(self, row, column):
            self.shape = [(0,0), (1, 0), (0, 1), (1, 1)] # When rotated once this would turn into [(0,0),(0,-1),(1,0),(1,-1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c) in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c) in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self): # We iterate through the offsets of the shape In order to rotate the Tetromino 90 degrees clockwise and set its new offset.
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset)) # We don't immediately set this as the shapes new offset because we must first check if the shape can be rotated, if not can it be kicked off of another piece or a wall.
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape
        
    class Line():
        def __init__(self, row, column):
            self.shape = [(0,0), (-1, 0), (1, 0), (2, 0)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c)in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c)in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape


    
    class L_shape_R():
        def __init__(self, row, column):
            self.shape = [(0,0), (-1, 0), (1, 0), (1, 1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c) in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c) in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape
    
    class L_shape_L():
        def __init__(self, row, column):
            self.shape = [(0,0), (-1, 0), (1, 0), (1, -1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c) in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c) in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape

    class Z_shape_L():
        def __init__(self, row, column):
            self.shape = [(0,0), (0, -1), (1, 0), (1, 1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c)in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c)in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape
    
    class Z_shape_R():
        def __init__(self, row, column):
            self.shape = [(0,0), (0, 1), (1, 0), (1, -1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c)in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c)in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape

    class T_shape():
        def __init__(self, row, column):
            self.shape = [(0,0), (1, 0), (1, -1), (1, 1)]
            self.row = row
            self.column = column

        def blocks_at(self, row, column):
            return [(row + r , column + c) for (r, c)in self.shape]
        
        def blocks(self):
            return [(self.row + r, self.column + c) for (r, c) in self.shape]
        
        def set(self, row, column):
            self.row = row
            self.column = column

        def rotated_offset(self):
            new_shape = []
            for (roffset, coffset) in self.shape:
                new_column_offset = -roffset
                new_row_offset = coffset
                new_shape.append((new_row_offset, new_column_offset))
            return new_shape
        
        def rotate(self, new_shape):
            self.shape = new_shape