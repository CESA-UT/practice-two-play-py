"""
Plant card system for selecting and planting.
"""
import pygame
from constants import (PLANT_SPECS, CARD_WIDTH, CARD_HEIGHT, 
                      CARD_START_X, CARD_START_Y, CARD_SPACING, WHITE, BLACK)
from assets import asset_loader


class Card:
    """Represents a plant card in the selection bar."""
    
    def __init__(self, plant_type, index):
        self.plant_type = plant_type
        self.specs = PLANT_SPECS[plant_type]
        self.cost = self.specs['cost']
        self.cooldown_time = self.specs['cooldown']
        self.cooldown_remaining = 0
        
        # Position
        self.x = CARD_START_X + index * (CARD_WIDTH + CARD_SPACING)
        self.y = CARD_START_Y
        self.rect = pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT)
        
        # Load card image preserving its original aspect ratio (fit inside
        # the card box) so it is never squashed/stretched.
        self.image = asset_loader.load_image_fit(self.specs['card_image'],
                                                 CARD_WIDTH, CARD_HEIGHT)
        self.image_rect = self.image.get_rect(
            center=(self.x + CARD_WIDTH // 2, self.y + CARD_HEIGHT // 2))
        
        # Font for text
        self.font = pygame.font.Font(None, 20)
    
    def update(self, dt):
        """Update cooldown timer."""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= dt
            if self.cooldown_remaining < 0:
                self.cooldown_remaining = 0
    
    def can_use(self, sun_amount):
        """Check if card can be used (enough sun and cooldown ready)."""
        return sun_amount >= self.cost and self.cooldown_remaining <= 0
    
    def use(self):
        """Use the card (start cooldown)."""
        self.cooldown_remaining = self.cooldown_time
    
    def is_clicked(self, pos):
        """Check if card is clicked."""
        return self.rect.collidepoint(pos)
    
    def draw(self, screen, sun_amount):
        """Draw the card on screen."""
        # Draw card background box first (some card art has transparent
        # margins after aspect-preserving fit, so give it a solid backing)
        pygame.draw.rect(screen, (222, 222, 200), self.rect)
        
        # Draw card image, centered within the box (no distortion)
        screen.blit(self.image, self.image_rect)
        
        # Draw cost
        cost_text = self.font.render(str(self.cost), True, BLACK)
        screen.blit(cost_text, (self.x + 5, self.y + CARD_HEIGHT - 20))
        
        # Draw darkening overlay if not usable
        if not self.can_use(sun_amount):
            overlay = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (self.x, self.y))
        
        # Draw cooldown overlay
        if self.cooldown_remaining > 0:
            cooldown_ratio = self.cooldown_remaining / self.cooldown_time
            overlay_height = int(CARD_HEIGHT * cooldown_ratio)
            overlay = pygame.Surface((CARD_WIDTH, overlay_height))
            overlay.set_alpha(180)
            overlay.fill((50, 50, 50))
            screen.blit(overlay, (self.x, self.y))
            
            # Draw cooldown time
            cooldown_text = self.font.render(f"{self.cooldown_remaining:.1f}s", 
                                            True, WHITE)
            text_rect = cooldown_text.get_rect(center=(self.x + CARD_WIDTH // 2, 
                                                       self.y + CARD_HEIGHT // 2))
            screen.blit(cooldown_text, text_rect)
        
        # Draw border
        border_color = (0, 255, 0) if self.can_use(sun_amount) else (128, 128, 128)
        pygame.draw.rect(screen, border_color, self.rect, 2)


class CardBar:
    """Manages all plant cards."""
    
    def __init__(self):
        self.cards = []
        plant_types = ['SunFlower', 'PeaShooter', 'WallNut']
        
        for i, plant_type in enumerate(plant_types):
            card = Card(plant_type, i)
            self.cards.append(card)
        
        self.selected_card = None
    
    def update(self, dt):
        """Update all cards."""
        for card in self.cards:
            card.update(dt)
    
    def handle_click(self, pos, sun_amount):
        """Handle click on cards. Returns selected plant type or None."""
        for card in self.cards:
            if card.is_clicked(pos) and card.can_use(sun_amount):
                self.selected_card = card
                return card.plant_type
        return None
    
    def use_selected_card(self):
        """Use the currently selected card."""
        if self.selected_card:
            self.selected_card.use()
            selected = self.selected_card
            self.selected_card = None
            return selected.cost
        return 0
    
    def cancel_selection(self):
        """Cancel current card selection."""
        self.selected_card = None
    
    def draw(self, screen, sun_amount):
        """Draw all cards."""
        for card in self.cards:
            card.draw(screen, sun_amount)
        
        # Draw indicator for selected card
        if self.selected_card:
            rect = self.selected_card.rect
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)
