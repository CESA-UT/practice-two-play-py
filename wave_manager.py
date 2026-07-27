"""
Wave manager for spawning zombies.
"""
from constants import WAVES
from entities import NormalZombie


class WaveManager:
    """Manages zombie waves."""
    
    def __init__(self):
        self.waves = WAVES
        self.current_wave_index = 0
        self.all_waves_spawned = False
    
    def update(self, game_time, zombies, speed_multiplier=1.0):
        """Update wave spawning based on game time.
        
        speed_multiplier scales newly spawned zombies' movement speed
        according to the selected difficulty level.
        """
        if self.all_waves_spawned:
            return
        
        if self.current_wave_index >= len(self.waves):
            self.all_waves_spawned = True
            return
        
        current_wave = self.waves[self.current_wave_index]
        
        # Check if it's time to spawn this wave
        if game_time >= current_wave['start_time']:
            # Spawn all zombies in this wave
            for zombie_data in current_wave['zombies']:
                zombie_type = zombie_data['type']
                row = zombie_data['row']
                
                if zombie_type == 'NormalZombie':
                    zombie = NormalZombie(row, speed_multiplier=speed_multiplier)
                    zombies.append(zombie)
            
            # Move to next wave
            self.current_wave_index += 1
    
    def is_complete(self, zombies):
        """Check if all waves are complete and all zombies are dead."""
        if not self.all_waves_spawned:
            return False
        
        # Check if any zombies are still alive
        for zombie in zombies:
            if zombie.alive:
                return False
        
        return True
