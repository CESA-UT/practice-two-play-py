"""
Asset loading and management.
"""
import pygame
import os


class AssetLoader:
    """Loads and manages game assets."""
    
    def __init__(self):
        self.images = {}
        self.sounds = {}
        
    def load_image(self, path, scale=None):
        """Load an image from the given path."""
        if path in self.images:
            return self.images[path]
        
        try:
            full_path = path
            if not os.path.exists(full_path):
                print(f"Warning: Image not found: {full_path}")
                # Create a placeholder surface
                surface = pygame.Surface((50, 50))
                surface.fill((255, 0, 255))  # Magenta placeholder
                self.images[path] = surface
                return surface
            
            image = pygame.image.load(full_path).convert_alpha()
            
            if scale:
                # Use smoothscale for better quality and prevent stretching
                image = pygame.transform.smoothscale(image, scale)
            
            self.images[path] = image
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Create placeholder
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 255))
            self.images[path] = surface
            return surface
    
    def load_image_fit(self, path, max_width, max_height):
        """Load an image and scale it to FIT within (max_width, max_height)
        while preserving its original aspect ratio (no distortion/stretching).
        The returned surface may be smaller than the box in one dimension.
        """
        cache_key = f"{path}::fit::{max_width}x{max_height}"
        if cache_key in self.images:
            return self.images[cache_key]

        try:
            if not os.path.exists(path):
                print(f"Warning: Image not found: {path}")
                surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
                surface.fill((255, 0, 255, 255))
                self.images[cache_key] = surface
                return surface

            image = pygame.image.load(path).convert_alpha()
            orig_width, orig_height = image.get_size()

            scale = min(max_width / orig_width, max_height / orig_height)
            new_width = max(1, round(orig_width * scale))
            new_height = max(1, round(orig_height * scale))

            image = pygame.transform.smoothscale(image, (new_width, new_height))
            self.images[cache_key] = image
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
            surface.fill((255, 0, 255, 255))
            self.images[cache_key] = surface
            return surface

    def load_sound(self, path):
        """Load a sound from the given path."""
        if path in self.sounds:
            return self.sounds[path]
        
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                self.sounds[path] = sound
                return sound
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
        
        return None


# Global asset loader instance
asset_loader = AssetLoader()
