# Plants vs. Zombies — Python Implementation

## How to Run

**1. Install dependencies**
```bash
pip install pygame
```

Or use the virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Run the game**
```bash
python main.py
```

## Controls

| Action | Input |
|---|---|
| Select a plant card | Left-click on a card |
| Place a plant | Left-click on a grid cell |
| Collect sun | Left-click on a sun |
| Pause / Resume | ESC |
| Restart (after game over) | R |
| Return to main menu | M (from pause or game over) |

## Code Structure

```
py_game_excercise/
│
├── main.py              # Entry point — creates and runs the Game instance
├── game.py              # Main game loop, state machine (menu / playing),
│                        # input handling, update/draw dispatch
├── menu.py              # Main menu screen with difficulty level dropdown
├── board.py             # 5×9 grid management and background rendering
├── card.py              # Plant card UI (cooldown, cost display, selection)
├── wave_manager.py      # Zombie wave spawning at timed intervals
├── constants.py         # All numeric constants and configuration
│                        # (HP, speed, costs, grid dimensions, level configs)
├── assets.py            # Image/sound asset loading and caching
├── requirements.txt     # Python dependencies (pygame)
│
├── entities/
│   ├── plant.py         # Plant base class + PeaShooter, SunFlower, WallNut
│   ├── zombie.py        # Zombie base class + NormalZombie
│   ├── projectile.py    # Pea projectile (movement + collision)
│   └── sun.py           # Sun resource (falling animation + collection)
│
├── Assets/
│   ├── images/
│   │   ├── Cards/       # Plant card artwork
│   │   ├── Plants/      # Plant GIF animations
│   │   ├── Zombies/     # Zombie GIF animations
│   │   └── items/       # Background, projectiles, UI elements
│   └── sounds/          # Sound effects and background music
│
└── docs/
    └── characters/      # Gameplay specs (HP, speed, damage, cooldown)
                         # for every plant and zombie type
```
