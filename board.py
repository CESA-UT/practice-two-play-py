"""
Game board and grid management.
"""
import pygame
from constants import (ROWS, COLS, GRID_START_X, GRID_START_Y, 
                      CELL_WIDTH, CELL_HEIGHT, BACKGROUND_IMAGE,
                      SCREEN_WIDTH, SCREEN_HEIGHT, BLACK)
from assets import asset_loader


class Board:
    """Manages the game board and grid."""
    
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        
        # Grid to track which cells have plants
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # Load background scaled to exactly fill the window. SCREEN_WIDTH/
        # SCREEN_HEIGHT are set to the image's native size, so this is a
        # no-op resize in practice, but it guarantees full coverage even if
        # someone changes the window size later.
        self.background = asset_loader.load_image(
            BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def can_plant(self, row, col):
        """Check if a plant can be placed in the given cell."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.grid[row][col] is None
    
    def place_plant(self, row, col, plant):
        """Place a plant in the grid."""
        if self.can_plant(row, col):
            self.grid[row][col] = plant
            return True
        return False
    
    def remove_plant(self, row, col):
        """Remove a plant from the grid."""
        if row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            self.grid[row][col] = None
    
    def get_cell_from_pos(self, x, y):
        """Get grid cell (row, col) from screen position."""
        if x < GRID_START_X or y < GRID_START_Y:
            return None, None
        
        col = int((x - GRID_START_X) / CELL_WIDTH)
        row = int((y - GRID_START_Y) / CELL_HEIGHT)
        
        if row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            return row, col
        
        return None, None
    
    def update(self, plants):
        """Update the grid based on current plants."""
        # Clear grid
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # Repopulate with alive plants
        for plant in plants:
            if plant.alive:
                self.grid[plant.row][plant.col] = plant
    
    def draw(self, screen):
        """Draw the board background.
        
        We always fill the entire screen first as a defensive measure: even
        though the background image is sized to exactly match the window,
        this guarantees no stale pixels from a previous frame are ever left
        visible (which previously looked like "stretched"/smeared sprites
        in the area outside the lawn image).
        """
        screen.fill(BLACK)
        screen.blit(self.background, (0, 0))
        
        # Optional: Draw grid lines for debugging
        # self.draw_grid(screen)
    
    def draw_grid(self, screen):
        """Draw grid lines (for debugging)."""
        for row in range(self.rows + 1):
            y = GRID_START_Y + row * CELL_HEIGHT
            pygame.draw.line(screen, (100, 100, 100), 
                           (GRID_START_X, y), 
                           (GRID_START_X + COLS * CELL_WIDTH, y), 1)
        
        for col in range(self.cols + 1):
            x = GRID_START_X + col * CELL_WIDTH
            pygame.draw.line(screen, (100, 100, 100), 
                           (x, GRID_START_Y), 
                           (x, GRID_START_Y + ROWS * CELL_HEIGHT), 1)
