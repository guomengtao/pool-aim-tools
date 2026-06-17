# Pool Aim Tools

A transparent overlay tool for billiards/pool aiming assistance.

## Features

- ✅ **Click-through Transparency**: Clicks outside the overlay window pass through to applications below
- ✅ **Real-time Aiming Lines**: Click inside the window to draw lines from the clicked point to all 6 pockets
- ✅ **Vertical Table Layout**: Optimized for vertical (portrait) pool table orientation
- ✅ **Semi-transparent Display**: Light gray lines and circles won't obscure the game view
- ✅ **Always-on-top**: Window stays above all other applications

## Requirements

- Python 3.7+
- PyQt5
- pynput

## Installation

```bash
git clone https://github.com/guomengtao/pool-aim-tools.git
cd pool-aim-tools
pip install -r requirements.txt
```

## Usage

```bash
python final_overlay.py
```

## Controls

| Action | Description |
|--------|-------------|
| Click inside window | Place aiming point and draw lines to pockets |
| Click outside window | Click passes through to pool game |
| Press `q` | Quit the application |

## Pocket Positions (Vertical Table 224x432)

| Pocket | Position | Coordinates |
|--------|----------|-------------|
| Top Left | Corner | (15, 15) |
| Top Right | Corner | (209, 15) |
| Left Middle | Side | (15, 216) |
| Right Middle | Side | (209, 216) |
| Bottom Left | Corner | (15, 417) |
| Bottom Right | Corner | (209, 417) |

## Window Position

- Default position: 100px from left edge, vertically centered
- Size: 224px × 432px (standard pool table proportions)

## How It Works

1. A transparent overlay window appears on the left side of your screen
2. Click anywhere inside the window to mark a target position
3. Six semi-transparent lines are drawn from the target to each pocket
4. Use these lines to visualize aiming paths for your shots
5. Clicks outside the window work normally with your pool game

## Notes

- The overlay is fully transparent and won't interfere with your game
- The aiming lines are semi-transparent (40% opacity) to avoid obscuring the table
- The window stays on top of all other applications
- Press `q` at any time to close the overlay

## License

MIT License