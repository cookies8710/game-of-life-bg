# game-of-life-bg
Game of life rendered into a PNG file

Use:
- `python3 game_of_life.py` - periodically renders game state into 'game_of_life_frontbuffer.png' file
- ` ls game_of_life_frontbuffer.png | entr feh --bg-scale game_of_life_frontbuffer.png` uses it as background
