"""
Projectile entity.
"""
import pygame
from constants import (PROJECTILE_SPEED, PROJECTILE_IMAGE, 
                      GRID_START_X, CELL_WIDTH, SCREEN_WIDTH)
from assets import asset_loader


class Projectile:
    """Projectile fired by plants."""
    
    def __init__(self, row, col, x, y, damage):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = PROJECTILE_SPEED  # cells per second
        self.alive = True
        
        # Load image
        self.image = asset_loader.load_image(PROJECTILE_IMAGE, (28, 28))
    
    def update(self, dt, game_state):
        """Update projectile position and check collisions."""
        if not self.alive:
            return
        
        # Move right
        self.x += self.speed * CELL_WIDTH * dt
        
        # Check if off screen
        if self.x > SCREEN_WIDTH:
            self.alive = False
            return
        
        # Check collision with zombies in the same row
        for zombie in game_state['zombies']:
            if zombie.row == self.row and zombie.alive:
                # Simple collision detection
                distance = abs(zombie.x - self.x)
                if distance < 40:  # Collision threshold
                    zombie.take_damage(self.damage)
                    self.alive = False
                    break
    
    def draw(self, screen):
        """Draw the projectile on screen."""
        if self.alive:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
