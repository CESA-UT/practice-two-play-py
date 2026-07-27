"""
Plant entities.
"""
import pygame
from constants import PLANT_SPECS, GRID_START_X, GRID_START_Y, CELL_WIDTH, CELL_HEIGHT
from assets import asset_loader


class Plant:
    """Base class for all plants."""
    
    def __init__(self, row, col, plant_type):
        self.row = row
        self.col = col
        self.plant_type = plant_type
        self.specs = PLANT_SPECS[plant_type]
        self.hp = self.specs['hp']
        self.max_hp = self.specs['hp']
        self.alive = True
        
        # Position on screen
        self.x = GRID_START_X + col * CELL_WIDTH + CELL_WIDTH // 2
        self.y = GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2
        
        # Load image preserving aspect ratio so it never looks stretched
        max_size = 78
        self.image = asset_loader.load_image_fit(
            self.specs['plant_image'], max_size, max_size)
        self.width, self.height = self.image.get_size()
        
    def take_damage(self, damage):
        """Take damage and check if plant dies."""
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
    
    def update(self, dt, game_state):
        """Update plant state. Override in subclasses."""
        pass
    
    def draw(self, screen):
        """Draw the plant on screen."""
        if self.alive:
            # Draw plant image centered with proper positioning
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
            
            # Draw HP bar
            self.draw_hp_bar(screen)
    
    def draw_hp_bar(self, screen):
        """Draw HP bar above the plant."""
        bar_width = 60
        bar_height = 5
        bar_x = int(self.x - bar_width // 2)
        bar_y = int(self.y - 45)
        
        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Foreground (green) based on remaining HP
        hp_ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))


class PeaShooter(Plant):
    """PeaShooter plant - shoots peas at zombies."""
    
    def __init__(self, row, col):
        super().__init__(row, col, 'PeaShooter')
        self.fire_timer = 0
        self.fire_interval = self.specs['fire_interval']
    
    def update(self, dt, game_state):
        """Update PeaShooter - fire at zombies in the same row."""
        self.fire_timer += dt
        
        # Check if there's a zombie in the same row
        has_zombie_in_row = False
        for zombie in game_state['zombies']:
            if zombie.row == self.row and zombie.alive:
                has_zombie_in_row = True
                break
        
        # Fire if cooldown is ready and there's a zombie
        if has_zombie_in_row and self.fire_timer >= self.fire_interval:
            self.fire_timer = 0
            # Create projectile
            from .projectile import Projectile
            projectile = Projectile(self.row, self.col, self.x, self.y, self.specs['damage'])
            game_state['projectiles'].append(projectile)


class SunFlower(Plant):
    """SunFlower plant - produces sun."""
    
    def __init__(self, row, col, sun_interval_multiplier=1.0):
        super().__init__(row, col, 'SunFlower')
        self.produce_timer = 0
        # Difficulty level scales how often sun is produced (see
        # constants.LEVEL_CONFIGS) - lower multiplier means sun more often.
        self.sun_interval_multiplier = sun_interval_multiplier
        self.produce_interval = self.specs['sun_produce_interval'] * sun_interval_multiplier
        self.first_sun = True
    
    def update(self, dt, game_state):
        """Update SunFlower - produce sun periodically."""
        self.produce_timer += dt
        
        # First sun comes faster (after 7 seconds, scaled by difficulty)
        interval = 7.0 * self.sun_interval_multiplier if self.first_sun else self.produce_interval
        
        if self.produce_timer >= interval:
            self.produce_timer = 0
            self.first_sun = False
            
            # Create sun
            from .sun import Sun
            sun = Sun(self.x, self.y, from_plant=True)
            game_state['suns'].append(sun)


class WallNut(Plant):
    """WallNut plant - defensive wall."""
    
    def __init__(self, row, col):
        super().__init__(row, col, 'WallNut')
    
    def update(self, dt, game_state):
        """WallNut doesn't have active behavior, just blocks zombies."""
        pass
