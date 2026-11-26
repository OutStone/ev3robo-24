#!/usr/bin/env pybricks-micropython
"""
Domino brick selector for EV3 (Pybricks MicroPython v2.x).

Screen shows the field rotated 180 deg (screen "up" = bottom of the layout picture).

Controls
  SIDE mode : UP / DOWN / LEFT / RIGHT  -> pick the side shown on that edge of the screen
              CENTER                    -> confirm the whole selection (finish)
  BRICK mode: arrows ALONG the side     -> move the cursor
              CENTER                    -> toggle brick (select / unselect)
              arrow ACROSS the side     -> back to SIDE mode
  Anywhere  : hold CENTER > 1 s         -> confirm the whole selection (finish)

Drawing
  empty box   = not selected
  filled box  = selected
  double frame around a brick = cursor
  dotted frame around a side  = active side

Brick names follow the layout picture (original orientation):
  T1..T4 = top row (left -> right), B1..B4 = bottom row (left -> right)
  L1..L4 = left column (top -> bottom), R1..R4 = right column (top -> bottom)
"""

from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import Font

ev3 = EV3Brick()
FONT = Font(size=10)
ev3.screen.set_font(FONT)

# ---------------------------------------------------------------- layout
IMG_W, IMG_H = 530, 720           # size of the layout picture (px)
SCALE = 0.172                     # picture px -> screen px (picture 720 high -> ~124 px)
OX, OY = 2, 2                     # screen offset of the field
LONG, SHORT = 16, 7               # drawn brick size on screen (exaggerated for visibility)
LINE = 11                         # text line height


def to_screen(ix, iy):
    """Picture coordinates -> screen coordinates, rotated 180 deg."""
    return OX + (IMG_W - ix) * SCALE, OY + (IMG_H - iy) * SCALE


# (name, x in picture, y in picture, vertical?)
RAW = []
for i, x in enumerate((153, 233, 313, 392)):
    RAW.append(("T%d" % (i + 1), x, 78, True))
    RAW.append(("B%d" % (i + 1), x, 645, True))
for i, y in enumerate((196, 307, 418, 529)):
    RAW.append(("L%d" % (i + 1), 75, y, False))
    RAW.append(("R%d" % (i + 1), 474, y, False))

# picture side -> which screen edge it ends up on after the 180 deg rotation
SCREEN_EDGE = {"T": Button.DOWN, "B": Button.UP, "L": Button.RIGHT, "R": Button.LEFT}
EDGE_NAME = {Button.UP: "TOP", Button.DOWN: "BOTTOM", Button.LEFT: "LEFT", Button.RIGHT: "RIGHT"}

BRICKS = []
for name, ix, iy, vertical in RAW:
    cx, cy = to_screen(ix, iy)
    w, h = (SHORT, LONG) if vertical else (LONG, SHORT)
    x1, y1 = int(cx - w / 2), int(cy - h / 2)
    BRICKS.append({"name": name, "cx": cx, "cy": cy,
                   "box": (x1, y1, x1 + w, y1 + h),
                   "edge": SCREEN_EDGE[name[0]]})

# bricks of every screen edge, ordered as they appear on the screen
SIDES = {}
for edge in (Button.UP, Button.DOWN, Button.LEFT, Button.RIGHT):
    members = [b for b in BRICKS if b["edge"] == edge]
    if edge in (Button.UP, Button.DOWN):
        members.sort(key=lambda b: b["cx"])     # left -> right on screen
    else:
        members.sort(key=lambda b: b["cy"])     # top -> bottom on screen
    SIDES[edge] = members

FIELD_BOX = (1, 1, 92, 126)
yx1, yy1 = to_screen(360, 528)                  # yellow zone from the picture
yx2, yy2 = to_screen(185, 195)
YELLOW_BOX = (int(yx1), int(yy1), int(yx2), int(yy2))


# ---------------------------------------------------------------- drawing helpers
def dotted_box(x1, y1, x2, y2, step=3):
    for x in range(x1, x2 + 1, step):
        ev3.screen.draw_pixel(x, y1)
        ev3.screen.draw_pixel(x, y2)
    for y in range(y1, y2 + 1, step):
        ev3.screen.draw_pixel(x1, y)
        ev3.screen.draw_pixel(x2, y)


def draw(mode, side, cursor, selected):
    scr = ev3.screen
    scr.clear()

    # field + yellow start zone
    scr.draw_box(*FIELD_BOX)
    dotted_box(*YELLOW_BOX, step=4)

    # bricks
    for b in BRICKS:
        scr.draw_box(*b["box"], fill=b["name"] in selected)

    # active side + cursor
    if mode == "brick":
        members = SIDES[side]
        xs1 = min(b["box"][0] for b in members) - 3
        ys1 = min(b["box"][1] for b in members) - 3
        xs2 = max(b["box"][2] for b in members) + 3
        ys2 = max(b["box"][3] for b in members) + 3
        dotted_box(max(xs1, 0), max(ys1, 0), min(xs2, 177), min(ys2, 127))

        x1, y1, x2, y2 = members[cursor]["box"]
        scr.draw_box(x1 - 2, y1 - 2, x2 + 2, y2 + 2)
        scr.draw_box(x1 - 3, y1 - 3, x2 + 3, y2 + 3)

    # text panel
    tx, ty = 97, 2
    if mode == "side":
        lines = ["Pick side:", "arrow = side", "OK = done"]
    else:
        along = "< >" if side in (Button.UP, Button.DOWN) else "^ v"
        lines = ["Side " + EDGE_NAME[side],
                 "Brick " + members[cursor]["name"],
                 along + " move",
                 "OK toggle"]
    lines.append("Sel: %d" % len(selected))
    names = sorted(selected)
    for i in range(0, len(names), 4):
        lines.append(" ".join(names[i:i + 4]))
    for line in lines:
        scr.draw_text(tx, ty, line)
        ty += LINE


# ---------------------------------------------------------------- input
def wait_button():
    """Wait for one press + release. Returns (button, held_ms)."""
    while not ev3.buttons.pressed():
        wait(10)
    button = ev3.buttons.pressed()[0]
    timer = StopWatch()
    while ev3.buttons.pressed():
        wait(10)
    return button, timer.time()


# ---------------------------------------------------------------- main selector
def select_bricks():
    """Interactive selection. Returns sorted list of selected brick names."""
    selected = set()
    mode, side, cursor = "side", None, 0

    while True:
        draw(mode, side, cursor, selected)
        button, held = wait_button()

        # long press OK = finish from anywhere
        if button == Button.CENTER and held > 1000:
            break

        if mode == "side":
            if button == Button.CENTER:
                break
            if button in SIDES:
                side, cursor, mode = button, 0, "brick"
            continue

        # brick mode
        members = SIDES[side]
        prev_b, next_b = ((Button.LEFT, Button.RIGHT) if side in (Button.UP, Button.DOWN)
                          else (Button.UP, Button.DOWN))
        if button == prev_b:
            cursor = (cursor - 1) % len(members)
        elif button == next_b:
            cursor = (cursor + 1) % len(members)
        elif button == Button.CENTER:
            name = members[cursor]["name"]
            if name in selected:
                selected.remove(name)
                ev3.speaker.beep(500, 60)
            else:
                selected.add(name)
                ev3.speaker.beep(1000, 60)
        else:
            mode = "side"   # arrow across the side -> back to side selection

    ev3.speaker.beep(1500, 150)
    return sorted(selected)


# ---------------------------------------------------------------- demo
if __name__ == "__main__":
    flipped = select_bricks()

    ev3.screen.clear()
    ev3.screen.draw_text(2, 2, "Selected %d:" % len(flipped))
    for i in range(0, len(flipped), 6):
        ev3.screen.draw_text(2, 2 + LINE * (1 + i // 6), " ".join(flipped[i:i + 6]))
    print("Selected:", flipped)
    wait(5000)
