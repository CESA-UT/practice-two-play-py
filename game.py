"""
Main game class and game loop.
"""
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_SUN, 
                      SKY_SUN_INTERVAL, WHITE, BLACK, FONT_LARGE, FONT_MEDIUM,
                      FONT_SMALL, LEVEL_CONFIGS, DEFAULT_LEVEL,
                      BACKGROUND_MUSIC, BACKGROUND_MUSIC_VOLUME)
from board import Board
from card import CardBar
from wave_manager import WaveManager
from entities import PeaShooter, SunFlower, WallNut, Sun
from menu import MainMenu

STATE_MENU = 'menu'
STATE_PLAYING = 'playing'


class Game:
    """Main game class."""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plants vs. Zombies")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # State machine: start on the main menu so the player can pick a
        # difficulty level before the lawn/board is initialized.
        self.state = STATE_MENU
        self.menu = MainMenu()
        self.level = DEFAULT_LEVEL
        self.level_config = LEVEL_CONFIGS[DEFAULT_LEVEL]
        
        # Game state (populated by start_game() once the player presses Start)
        self.sun = INITIAL_SUN
        self.game_time = 0
        self.game_over = False
        self.player_won = False
        
        self.board = Board()
        self.card_bar = CardBar()
        self.wave_manager = WaveManager()
        
        self.plants = []
        self.zombies = []
        self.projectiles = []
        self.suns = []
        
        self.sky_sun_timer = 0
        
        # Font
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            
            if self.state == STATE_PLAYING and not self.paused and not self.game_over:
                self.update(dt)
            
            self.draw()
        
        pygame.quit()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_MENU:
                        self.running = False
                    elif self.game_over:
                        self.running = False
                    else:
                        self.paused = not self.paused
                
                elif event.key == pygame.K_r and self.game_over:
                    self.start_game(self.level)
                
                elif event.key == pygame.K_m and (self.game_over or self.paused):
                    self.state = STATE_MENU
                    self.paused = False
                    self.stop_background_music()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.state == STATE_MENU:
                        self.handle_menu_click(event.pos)
                    else:
                        self.handle_click(event.pos)
    
    def handle_menu_click(self, pos):
        """Handle mouse clicks while on the main menu."""
        action = self.menu.handle_click(pos)
        if action == 'start':
            self.start_game(self.menu.selected_level)
    
    def start_game(self, level):
        """Initialize/reset the game to be played at the given difficulty
        level (1=easiest .. 4=hardest) and switch to the playing state."""
        self.level = level
        self.level_config = LEVEL_CONFIGS[level]
        
        self.sun = INITIAL_SUN
        self.game_time = 0
        self.game_over = False
        self.player_won = False
        self.paused = False
        
        self.board = Board()
        self.card_bar = CardBar()
        self.wave_manager = WaveManager()
        
        self.plants = []
        self.zombies = []
        self.projectiles = []
        self.suns = []
        
        self.sky_sun_timer = 0
        
        self.state = STATE_PLAYING
        self.play_background_music()
    
    def play_background_music(self):
        """Start looping the background music track. Safe to call even if
        the audio device / music file is unavailable (e.g. in headless
        test environments) - failures are logged, not fatal."""
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.set_volume(BACKGROUND_MUSIC_VOLUME)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Warning: could not play background music: {e}")
    
    def stop_background_music(self):
        """Stop the background music (used when returning to the menu)."""
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
    
    def handle_click(self, pos):
        """Handle mouse clicks."""
        # Check if clicking on sun to collect
        for sun in self.suns:
            if sun.check_collection(pos):
                sun.alive = False
                self.sun += sun.value
                return
        
        # Check if clicking on card
        selected_plant = self.card_bar.handle_click(pos, self.sun)
        if selected_plant:
            return
        
        # Check if placing a plant
        if self.card_bar.selected_card:
            row, col = self.board.get_cell_from_pos(pos[0], pos[1])
            if row is not None and col is not None:
                if self.board.can_plant(row, col):
                    # Place plant
                    plant = self.create_plant(self.card_bar.selected_card.plant_type, row, col)
                    if plant:
                        self.plants.append(plant)
                        self.board.place_plant(row, col, plant)
                        cost = self.card_bar.use_selected_card()
                        self.sun -= cost
            else:
                # Click outside grid - cancel selection
                self.card_bar.cancel_selection()
    
    def create_plant(self, plant_type, row, col):
        """Create a plant instance based on type."""
        if plant_type == 'PeaShooter':
            return PeaShooter(row, col)
        elif plant_type == 'SunFlower':
            return SunFlower(row, col,
                            sun_interval_multiplier=self.level_config['sun_interval_multiplier'])
        elif plant_type == 'WallNut':
            return WallNut(row, col)
        return None
    
    def update(self, dt):
        """Update game state."""
        self.game_time += dt
        
        # Update card bar
        self.card_bar.update(dt)
        
        # Spawn sky suns - interval scaled by the selected difficulty level
        sky_sun_interval = SKY_SUN_INTERVAL * self.level_config['sun_interval_multiplier']
        self.sky_sun_timer += dt
        if self.sky_sun_timer >= sky_sun_interval:
            self.sky_sun_timer = 0
            sun = Sun(from_plant=False)
            self.suns.append(sun)
        
        # Update wave manager - newly spawned zombies get the difficulty's
        # speed multiplier applied
        self.wave_manager.update(self.game_time, self.zombies,
                                speed_multiplier=self.level_config['zombie_speed_multiplier'])
        
        # Create game state dict for entities
        game_state = {
            'plants': self.plants,
            'zombies': self.zombies,
            'projectiles': self.projectiles,
            'suns': self.suns,
            'game_over': self.game_over,
            'player_won': self.player_won
        }
        
        # Update plants
        for plant in self.plants[:]:
            plant.update(dt, game_state)
            if not plant.alive:
                self.board.remove_plant(plant.row, plant.col)
        
        # Remove dead plants
        self.plants = [p for p in self.plants if p.alive]
        
        # Update zombies
        for zombie in self.zombies:
            zombie.update(dt, game_state)
        
        # Remove dead zombies
        self.zombies = [z for z in self.zombies if z.alive]
        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt, game_state)
        
        # Remove dead projectiles
        self.projectiles = [p for p in self.projectiles if p.alive]
        
        # Update suns
        for sun in self.suns:
            sun.update(dt)
        
        # Remove dead suns
        self.suns = [s for s in self.suns if s.alive]
        
        # Check if game over flag was set by zombie
        if game_state['game_over']:
            self.game_over = True
            self.player_won = game_state['player_won']
        
        # Check win condition
        if self.wave_manager.is_complete(self.zombies):
            self.game_over = True
            self.player_won = True
    
    def draw(self):
        """Draw everything on screen."""
        # Draw board background (also used behind the menu screen so the
        # lawn is visible faintly under the overlay)
        self.board.draw(self.screen)
        
        if self.state == STATE_MENU:
            self.menu.draw(self.screen)
            pygame.display.flip()
            return
        
        # Draw plants
        for plant in self.plants:
            plant.draw(self.screen)
        
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Draw suns
        for sun in self.suns:
            sun.draw(self.screen)
        
        # Draw card bar
        self.card_bar.draw(self.screen, self.sun)
        
        # Draw sun counter
        self.draw_sun_counter()
        
        # Draw game time
        self.draw_game_time()
        
        # Draw cursor preview if card selected
        if self.card_bar.selected_card:
            self.draw_plant_preview()
        
        # Draw pause overlay
        if self.paused:
            self.draw_pause_overlay()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_sun_counter(self):
        """Draw sun counter just below the plant cards (over the house
        wall area), so it never overlaps the lawn grid."""
        panel_rect = pygame.Rect(45, 78, 220, 30)
        pygame.draw.rect(self.screen, (222, 222, 200), panel_rect, border_radius=4)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 1, border_radius=4)
        text = self.font_medium.render(f"Sun: {self.sun}", True, BLACK)
        self.screen.blit(text, (panel_rect.x + 8, panel_rect.y + 3))
    
    def draw_game_time(self):
        """Draw elapsed game time below the sun counter panel."""
        panel_rect = pygame.Rect(45, 112, 220, 26)
        pygame.draw.rect(self.screen, (222, 222, 200), panel_rect, border_radius=4)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 1, border_radius=4)
        text = self.font_small.render(
            f"Time: {int(self.game_time)}s   (Level {self.level})", True, BLACK)
        self.screen.blit(text, (panel_rect.x + 8, panel_rect.y + 4))
    
    def draw_plant_preview(self):
        """Draw plant preview at cursor."""
        mouse_pos = pygame.mouse.get_pos()
        row, col = self.board.get_cell_from_pos(mouse_pos[0], mouse_pos[1])
        
        if row is not None and col is not None:
            # Draw semi-transparent preview
            plant_type = self.card_bar.selected_card.plant_type
            # Simple preview - could be enhanced with actual plant image
            color = (0, 255, 0, 128) if self.board.can_plant(row, col) else (255, 0, 0, 128)
            preview_size = 75
            preview_surface = pygame.Surface((preview_size, preview_size))
            preview_surface.set_alpha(128)
            preview_surface.fill(color[:3])
            
            from constants import GRID_START_X, GRID_START_Y, CELL_WIDTH, CELL_HEIGHT
            x = GRID_START_X + col * CELL_WIDTH + CELL_WIDTH // 2 - preview_size // 2
            y = GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2 - preview_size // 2
            self.screen.blit(preview_surface, (int(x), int(y)))
    
    def draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        help_text = self.font_medium.render("Press ESC to resume", True, WHITE)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(help_text, help_rect)
        
        help_text2 = self.font_medium.render("Press M for main menu", True, WHITE)
        help_rect2 = help_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95))
        self.screen.blit(help_text2, help_rect2)
    
    def draw_game_over(self):
        """Draw game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.player_won:
            text = self.font_large.render("YOU WIN!", True, (0, 255, 0))
        else:
            text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        help_text1 = self.font_medium.render("Press R to restart", True, WHITE)
        help_rect1 = help_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(help_text1, help_rect1)
        
        help_text2 = self.font_medium.render("Press M for main menu", True, WHITE)
        help_rect2 = help_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(help_text2, help_rect2)
        
        help_text3 = self.font_medium.render("Press ESC to quit", True, WHITE)
        help_rect3 = help_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(help_text3, help_rect3)
