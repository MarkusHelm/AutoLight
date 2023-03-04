import cv2
import colorsys
from random import randrange

colorHues = [0, 30, 60, 120, 160, 200, 240, 270, 300, 360]

def getClosestHueIndex(hue: int) -> int:
    if hue < 0 or hue > 360: return 0
    for index, colorHue in enumerate(colorHues):
        if (hue == colorHue): return index
        if (hue > colorHue): continue
        if ((colorHue - hue) < (hue - colorHues[index - 1])):
            return index if (index < len(colorHues) - 1) else 0
        else: return index - 1

def hueToHex(hue):
    (r, g, b) = colorsys.hsv_to_rgb(hue/360, 1, 1)
    (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
    return '#%02x%02x%02x' % (r, g, b)

def createColorList(debug=True):
    print("  Collecting colors: ", end="")
    colorList = [0] * (len(colorHues) - 1)
    img = cv2.imread('img/cover_small.png')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(img_hsv)
    for iy, y in enumerate(h):
        for ix, x in enumerate(y):
            closestIndex = getClosestHueIndex(x*2)
            h[iy][ix] = colorHues[closestIndex]*0.5
            weight = int(0.0039 * v[iy][ix] * (s[iy][ix] if s[iy][ix] > 32 else 0))
            colorList[closestIndex] += weight
            if debug:
                v[iy][ix] = weight
                s[iy][ix] = weight
    if debug:
        img_hsv = cv2.merge([h, s, v])
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        cv2.imwrite('img/cover_small_color.png', img)
    print(colorList)
    return colorList

def getColors():
    colHues = colorHues.copy()[:-1]
    COLCOUNT = len(colHues)
    colList = createColorList()

    col1id = 0
    if sum(colList) > 0: # test if color left
        print("  1 Searching primary color")
        for idx, col in enumerate(colList):
            if col > colList[col1id]:
                col1id = idx
        colList[col1id] = 0
    else:
        print("  1 Random primary color")
        col1id = randrange(0,COLCOUNT - 1)
            
    col2id = 0
    col2prob = 0
    if sum(colList) > 0: # test if color left
        print("  2 Searching secondary color")
        for idx, col in enumerate(colList):
            if col > colList[col2id]:
                col2id= idx
        col2prob = colList[col2id]
        colList[col2id] = 0
        # remove primary neightbors
        colList[(col1id+1)%COLCOUNT] = 0
        colList[(col1id+COLCOUNT-1)%COLCOUNT] = 0
    else:
        print("  2 Random secondary color")
        mod = randrange(2,COLCOUNT - 2)
        col2id = (col1id + mod) % COLCOUNT

    if sum(colList) > 0 and closeColors(col1id, col2id):
        col3id = 0
        print("    Searching for alternative color")
        for idx, col in enumerate(colList):
            if col > colList[col3id]:
                col3id= idx
        if colList[col3id] * 3 >= col2prob:
            print("    Changing to alternative color")
            col2id = col3id

    col1hue = colHues[col1id]
    col2hue = colHues[col2id]
    col1hex = hueToHex(col1hue)
    col2hex = hueToHex(col2hue)

    return [[col1id, col1hue, col1hex], [col2id, col2hue, col2hex]]

def closeColors(col1id, col2id) -> bool:
    LASTHUE = len(colorHues) - 2
    if col1id == 0:
        if col2id == 1: return True
        if col2id == LASTHUE: return True
    if col2id == 0:
        if col1id == 1: return True
        if col1id == LASTHUE: return True
    if abs(col1id - col2id) <= 1:
        return True
    return False