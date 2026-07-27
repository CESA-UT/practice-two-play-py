"""
Main menu screen with a difficulty level dropdown selector.
"""
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_CONFIGS, DEFAULT_LEVEL,
                      WHITE, BLACK, GREEN, FONT_LARGE, FONT_MEDIUM, FONT_SMALL)


class LevelDropdown:
    """A simple dropdown widget for selecting the difficulty level (1-4)."""

    def __init__(self, x, y, width=280, item_height=38):
        self.x = x
        self.y = y
        self.width = width
        self.item_height = item_height
        self.is_open = False
        self.selected_level = DEFAULT_LEVEL
        self.levels = sorted(LEVEL_CONFIGS.keys())

        self.font = pygame.font.Font(None, FONT_SMALL)
        self.header_rect = pygame.Rect(x, y, width, item_height)

    def get_option_rect(self, index):
        """Rect for the Nth option in the expanded list, below the header."""
        return pygame.Rect(self.x, self.y + self.item_height * (index + 1),
                          self.width, self.item_height)

    def handle_click(self, pos):
        """Handle a mouse click. Returns True if this widget consumed it."""
        if self.header_rect.collidepoint(pos):
            self.is_open = not self.is_open
            return True

        if self.is_open:
            for i, level in enumerate(self.levels):
                if self.get_option_rect(i).collidepoint(pos):
                    self.selected_level = level
                    self.is_open = False
                    return True
            # Clicked elsewhere while the list was open - just close it,
            # but let the caller still process the click (e.g. Start button).
            self.is_open = False

        return False

    def draw(self, screen):
        # Header showing the current selection
        pygame.draw.rect(screen, WHITE, self.header_rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.header_rect, 2, border_radius=6)

        label = LEVEL_CONFIGS[self.selected_level]['label']
        text = self.font.render(label, True, BLACK)
        text_rect = text.get_rect(midleft=(self.header_rect.x + 12, self.header_rect.centery))
        screen.blit(text, text_rect)

        arrow = self.font.render("v" if not self.is_open else "^", True, BLACK)
        arrow_rect = arrow.get_rect(midright=(self.header_rect.right - 14, self.header_rect.centery))
        screen.blit(arrow, arrow_rect)

        if self.is_open:
            for i, level in enumerate(self.levels):
                rect = self.get_option_rect(i)
                is_selected = level == self.selected_level
                color = (205, 235, 205) if is_selected else WHITE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                option_text = self.font.render(LEVEL_CONFIGS[level]['label'], True, BLACK)
                option_rect = option_text.get_rect(midleft=(rect.x + 12, rect.centery))
                screen.blit(option_text, option_rect)


class MainMenu:
    """Main menu screen: title, difficulty dropdown, and a start button."""

    def __init__(self):
        self.font_title = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)

        dropdown_width = 280
        dropdown_x = SCREEN_WIDTH // 2 - dropdown_width // 2
        dropdown_y = SCREEN_HEIGHT // 2 - 30
        self.dropdown = LevelDropdown(dropdown_x, dropdown_y, dropdown_width)

        button_width = 200
        button_height = 50
        self.start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            dropdown_y + 90,
            button_width, button_height)

    @property
    def selected_level(self):
        return self.dropdown.selected_level

    def handle_click(self, pos):
        """Handle a mouse click on the menu. Returns 'start' if the Start
        Game button was pressed, otherwise None."""
        if self.dropdown.handle_click(pos):
            return None

        # Don't let a click "through" an open dropdown trigger Start
        if self.start_button.collidepoint(pos):
            return 'start'

        return None

    def draw(self, screen):
        """Draw the menu on top of whatever is already on screen (usually
        the lawn background, drawn by the caller first)."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((10, 40, 10))
        screen.blit(overlay, (0, 0))

        title = self.font_title.render("Plants vs. Zombies", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
        screen.blit(title, title_rect)

        label = self.font_medium.render("Select Difficulty:", True, WHITE)
        label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, self.dropdown.y - 28))
        screen.blit(label, label_rect)

        # Draw the Start button before the dropdown so an expanded dropdown
        # list always renders on top of it.
        pygame.draw.rect(screen, GREEN, self.start_button, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.start_button, 2, border_radius=8)
        start_text = self.font_medium.render("Start Game", True, BLACK)
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect)

        description = LEVEL_CONFIGS[self.dropdown.selected_level]['description']
        desc_text = self.font_small.render(description, True, WHITE)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, self.start_button.bottom + 26))
        screen.blit(desc_text, desc_rect)

        self.dropdown.draw(screen)
