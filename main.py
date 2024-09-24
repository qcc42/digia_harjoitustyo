import pyautogui as pag
import random
from typing import Union

canvas_w = 1280
canvas_h = 720
square_side = 50
no_sq = random.randint(2, 5)
offset_lc = [49, 43]

#function for determining whether two squares (x1, y1) and (x2, y2) with certain side length collide
def collides(x1: int, y1: int, x2: int, y2: int, side: int) -> bool:
    return not (x2 > x1 + side or y2 > y1 + side or x2 < x1 - side or y2 < y1 - side)

#determines whether square in position x, y of size "side" collides wit any square defined a position array
def collides_array(x: int, y: int, side: int, array: list) -> bool:
    for i in array:
        if collides(x, y, *i, side):
            return True
    return False

#generic function for drawing a square in position (x, y), position is relative to canvas upper left corner
def draw_square(x: int, y: int, side: int, borders: Union[list, tuple] = (0, 0, 0, 0)) -> None:

    pag.moveTo(x+borders[0], y+borders[1])
    pag.mouseDown()
    pag.drag(side, 0)
    pag.drag(0, side)
    pag.drag(-side, 0)
    pag.drag(0 , -side)
    pag.mouseUp()

#------------------------------------- execution starts here----------------------------------#

#open paint and set canvas size
pag.hotkey('win', 'r')
pag.write('mspaint')
pag.press('enter')
pag.sleep(1)
win = pag.getActiveWindow()
win.maximize()
pag.hotkey('ctrl', 'e')
pag.write(str(canvas_w))
pag.press('tab')
pag.write(str(canvas_h))
pag.press('enter')

pag.sleep(1)

#get canvas xy position (left upper corner)
canvas_coords = pag.locateOnScreen("lc.png",  confidence = 0.99)
canvas_xy = [canvas_coords[0] + offset_lc[0], canvas_coords[1] + offset_lc[1]]
#borders coordinates left up right down
borders_lurd = [canvas_xy[0], canvas_xy[1], canvas_xy[0] + canvas_w, canvas_xy[1] + canvas_h]

#define square positions, avoid overlaps
square_positions = []
init_pos = [random.randint(0, canvas_w - square_side), random.randint(0, canvas_h - square_side)]
curr_pos = init_pos
for i in range(no_sq):
    while collides_array(*curr_pos, square_side, square_positions):
        curr_pos = [random.randint(0, canvas_w - square_side), random.randint(0, canvas_h - square_side)]
    square_positions.append(curr_pos)

#draw all squares
for i in square_positions:
    draw_square(*i, square_side, borders_lurd)

#snap a screenshot of a square in order to know what to count
square_coords = (int(square_positions[0][0] + canvas_xy[0]), int(square_positions[0][1] + canvas_xy[1]), 5, 5)
scr_sh = pag.screenshot(region = square_coords)
scr_sh.save("scr_sh.png")

#counts square occurances based on screenshot
def getSquareCount() -> int:
    occurances = pag.locateAllOnScreen(scr_sh, confidence=0.99, grayscale=False)
    return len([i for i in occurances])

#draws noise until square count is no longer correct
def drawNoise(borders: Union[tuple, list] = (0, 0, pag.size()[0], pag.size()[1])) -> int:
    pag.moveTo(borders[0], borders[1])
    while no_sq == getSquareCount():
        pag.dragTo(random.randint(borders[0], borders[2]), random.randint(borders[1], borders[3]))
    return getSquareCount()

counted_occurances = getSquareCount()

#print the answer on the canvas
canvas_center = [canvas_w//2 + canvas_xy[0], canvas_h//2 + canvas_xy[1]]
pag.moveTo(canvas_center)
pag.press('t')
pag.click()
pag.write("Counted squares: " + str(counted_occurances))
pag.sleep(1)
pag.hotkey('ctrl', 'z')
pag.press('esc')
pag.press('p')

#draw noise
to_print = drawNoise(borders_lurd)

#print new square count on canvas
pag.moveTo(canvas_center)
pag.press('t')
pag.click()
pag.write("Counted squares: " + str(to_print))



