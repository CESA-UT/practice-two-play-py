"""
Game constants based on character specifications.
All values are derived from docs/characters/ files.
"""

# Screen dimensions
# IMPORTANT: This matches Frontyard.png's native resolution (1024x626) exactly.
# The background image must always fully cover the window - otherwise any
# area outside the image is left un-cleared between frames, which causes
# old sprite positions to "smear"/ghost on screen (looks like stretching).
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 626
FPS = 60

# Grid configuration (calibrated by inspecting the actual checkerboard lawn
# pattern in Frontyard.png - the grid spans roughly x=[270,1008], y=[55,580])
ROWS = 5
COLS = 9
GRID_START_X = 270
GRID_START_Y = 55
CELL_WIDTH = 82
CELL_HEIGHT = 105

# Sun system
INITIAL_SUN = 150
SUN_VALUE = 25
SKY_SUN_INTERVAL = 10.0  # seconds
SUN_COLLECTION_RADIUS = 30

# Plant specifications (from docs/characters/)
PLANT_SPECS = {
    'PeaShooter': {
        'cost': 100,
        'hp': 300,
        'cooldown': 7.5,  # seconds
        'damage': 20,
        'fire_interval': 1.5,  # seconds
        'card_image': 'Assets/images/Cards/PeaShooter.png',
        'plant_image': 'Assets/images/Plants/Peashooter.gif',
    },
    'SunFlower': {
        'cost': 50,
        'hp': 300,
        'cooldown': 7.5,
        'sun_produce_interval': 24.0,  # seconds
        'sun_produce_amount': 25,
        'card_image': 'Assets/images/Cards/SunFlower.png',
        'plant_image': 'Assets/images/Plants/SunFlower.gif',
    },
    'WallNut': {
        'cost': 50,
        'hp': 4000,
        'cooldown': 30.0,
        'card_image': 'Assets/images/Cards/WallNut.png',
        'plant_image': 'Assets/images/Plants/Wallnut.gif',
    }
}

# Zombie specifications
ZOMBIE_SPECS = {
    'NormalZombie': {
        'hp': 200,
        'speed': 0.25,  # cells per second
        'damage': 100,  # HP per second to plants
        'walk_image': 'Assets/images/Zombies/NormalZombie.gif',
        'eat_image': 'Assets/images/Zombies/NormalZombieEat.gif',
    }
}

# Projectile specifications
PROJECTILE_SPEED = 3.5  # cells per second
PROJECTILE_IMAGE = 'Assets/images/items/Pea.png'

# Sun specifications
SUN_IMAGE = 'Assets/images/items/Sun.png'
SUN_SIZE = 60

# Background
BACKGROUND_IMAGE = 'Assets/images/items/Frontyard.png'

# Background music - starts looping as soon as the player presses "Start
# Game" on the main menu.
BACKGROUND_MUSIC = 'Assets/sounds/watery-graves.mp3'
BACKGROUND_MUSIC_VOLUME = 0.5

# Difficulty levels (1 = easiest, 4 = hardest).
# Level 3 matches the original baseline values from the spec docs
# (SKY_SUN_INTERVAL and NormalZombie speed are unscaled at multiplier 1.0).
# - sun_interval_multiplier scales how often sun appears (sky drops AND
#   SunFlower production): lower = sun arrives faster/more often.
# - zombie_speed_multiplier scales how fast zombies walk: lower = slower.
LEVEL_CONFIGS = {
    1: {
        'label': 'Level 1 - Easiest',
        'description': 'Sun falls often, zombies are slow.',
        'sun_interval_multiplier': 0.55,
        'zombie_speed_multiplier': 0.6,
    },
    2: {
        'label': 'Level 2 - Easy',
        'description': 'Sun falls a bit faster, zombies a bit slower.',
        'sun_interval_multiplier': 0.75,
        'zombie_speed_multiplier': 0.8,
    },
    3: {
        'label': 'Level 3 - Normal',
        'description': 'Original balance: default sun rate and zombie speed.',
        'sun_interval_multiplier': 1.0,
        'zombie_speed_multiplier': 1.0,
    },
    4: {
        'label': 'Level 4 - Hardest',
        'description': 'Sun is scarce, zombies rush in fast.',
        'sun_interval_multiplier': 1.4,
        'zombie_speed_multiplier': 1.5,
    },
}
DEFAULT_LEVEL = 3

# Wave configuration (from docs/characters/Waves.md)
WAVES = [
    {'start_time': 20, 'zombies': [{'type': 'NormalZombie', 'row': 0}, 
                                    {'type': 'NormalZombie', 'row': 1}, 
                                    {'type': 'NormalZombie', 'row': 2}]},
    {'start_time': 50, 'zombies': [{'type': 'NormalZombie', 'row': 0},
                                    {'type': 'NormalZombie', 'row': 1},
                                    {'type': 'NormalZombie', 'row': 2},
                                    {'type': 'NormalZombie', 'row': 3},
                                    {'type': 'NormalZombie', 'row': 4}]},
    {'start_time': 90, 'zombies': [{'type': 'NormalZombie', 'row': 0},
                                    {'type': 'NormalZombie', 'row': 1},
                                    {'type': 'NormalZombie', 'row': 1},
                                    {'type': 'NormalZombie', 'row': 2},
                                    {'type': 'NormalZombie', 'row': 3},
                                    {'type': 'NormalZombie', 'row': 3},
                                    {'type': 'NormalZombie', 'row': 4}]},
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Card dimensions and positions
# Source card images are landscape (~1.6:1 aspect ratio); the box below
# matches that ratio so cards are never squashed/stretched.
CARD_WIDTH = 90
CARD_HEIGHT = 62
CARD_START_X = 50
CARD_START_Y = 10
CARD_SPACING = 10

# Font sizes
FONT_LARGE = 48
FONT_MEDIUM = 32
FONT_SMALL = 24
