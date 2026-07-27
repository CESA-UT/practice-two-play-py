"""
Zombie entities.
"""
import pygame
from constants import (ZOMBIE_SPECS, GRID_START_X, GRID_START_Y, 
                      CELL_WIDTH, CELL_HEIGHT, COLS)
from assets import asset_loader


class Zombie:
    """Base class for all zombies."""
    
    def __init__(self, row, zombie_type, speed_multiplier=1.0):
        self.row = row
        self.zombie_type = zombie_type
        self.specs = ZOMBIE_SPECS[zombie_type]
        self.hp = self.specs['hp']
        self.max_hp = self.specs['hp']
        # Difficulty level scales movement speed (see constants.LEVEL_CONFIGS)
        self.speed = self.specs['speed'] * speed_multiplier  # cells per second
        self.damage = self.specs['damage']  # HP per second
        self.alive = True
        self.eating = False
        
        # Start position: just past the right edge of the grid, but still
        # well within the canvas (which now exactly matches the background
        # image), so the zombie is always drawn on top of real artwork,
        # never in an un-cleared/black region.
        self.col_float = COLS + 0.1
        self.x = GRID_START_X + self.col_float * CELL_WIDTH
        self.y = GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2
        
        # Load images preserving their original aspect ratio so they never
        # look stretched/squashed, regardless of the source GIF's dimensions.
        max_width, max_height = 78, 100
        
        self.walk_image = asset_loader.load_image_fit(
            self.specs['walk_image'], max_width, max_height)
        self.eat_image = asset_loader.load_image_fit(
            self.specs['eat_image'], max_width, max_height)
        self.current_image = self.walk_image
        
        # Store dimensions for consistent rendering
        self.width, self.height = self.walk_image.get_size()
    
    def take_damage(self, damage):
        """Take damage and check if zombie dies."""
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
    
    def update(self, dt, game_state):
        """Update zombie state."""
        if not self.alive:
            return
        
        # Check if there's a plant in front of this zombie
        plant_in_front = None
        for plant in game_state['plants']:
            if plant.row == self.row and plant.alive:
                plant_col = plant.col
                # Check if plant is in front of zombie (to the left)
                if plant_col < self.col_float and plant_col >= self.col_float - 1:
                    plant_in_front = plant
                    break
        
        if plant_in_front:
            # Stop and eat
            self.eating = True
            self.current_image = self.eat_image
            
            # Deal damage to plant
            plant_in_front.take_damage(self.damage * dt)
        else:
            # Move left
            self.eating = False
            self.current_image = self.walk_image
            
            self.col_float -= self.speed * dt
            self.x = GRID_START_X + self.col_float * CELL_WIDTH
            
            # Check if zombie reached the house (left side)
            if self.col_float <= -0.5:
                game_state['game_over'] = True
                game_state['player_won'] = False
    
    def draw(self, screen):
        """Draw the zombie on screen."""
        if self.alive:
            # Draw zombie image with consistent size (no stretching)
            rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.current_image, rect)
            
            # Draw HP bar
            self.draw_hp_bar(screen)
    
    def draw_hp_bar(self, screen):
        """Draw HP bar above the zombie."""
        bar_width = 60
        bar_height = 5
        bar_x = int(self.x - bar_width // 2)
        bar_y = int(self.y - 55)
        
        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Foreground (green) based on remaining HP
        hp_ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))


class NormalZombie(Zombie):
    """Normal zombie - basic enemy."""
    
    def __init__(self, row, speed_multiplier=1.0):
        super().__init__(row, 'NormalZombie', speed_multiplier=speed_multiplier)
