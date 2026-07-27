"""
Sun entity.
"""
import pygame
import random
from constants import (SUN_IMAGE, SUN_VALUE, SUN_SIZE, SUN_COLLECTION_RADIUS,
                      GRID_START_X, GRID_START_Y, CELL_WIDTH, CELL_HEIGHT, COLS, ROWS)
from assets import asset_loader


class Sun:
    """Sun resource that can be collected."""
    
    def __init__(self, x=None, y=None, from_plant=False):
        self.value = SUN_VALUE
        self.alive = True
        self.from_plant = from_plant
        
        if from_plant:
            # Sun from SunFlower - appears at plant location
            self.x = x
            self.y = y
            self.target_y = y + 60  # Fall a bit
            self.falling = True
        else:
            # Sun from sky - random position
            self.x = random.randint(GRID_START_X, GRID_START_X + COLS * CELL_WIDTH)
            self.y = 0
            self.target_y = random.randint(GRID_START_Y + 50, GRID_START_Y + ROWS * CELL_HEIGHT)
            self.falling = True
        
        # Load image
        self.image = asset_loader.load_image(SUN_IMAGE, (SUN_SIZE, SUN_SIZE))
        
        # Lifetime after landing
        self.lifetime = 8.0  # seconds
        self.timer = 0
    
    def update(self, dt):
        """Update sun state."""
        if not self.alive:
            return
        
        # Fall animation
        if self.falling:
            fall_speed = 100  # pixels per second
            self.y += fall_speed * dt
            
            if self.y >= self.target_y:
                self.y = self.target_y
                self.falling = False
        else:
            # Count down lifetime
            self.timer += dt
            if self.timer >= self.lifetime:
                self.alive = False
    
    def check_collection(self, mouse_pos):
        """Check if sun is clicked and should be collected."""
        if not self.alive or self.falling:
            return False
        
        distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
        return distance <= SUN_COLLECTION_RADIUS
    
    def draw(self, screen):
        """Draw the sun on screen."""
        if self.alive:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
            
            # Draw sun value text
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(text, text_rect)
