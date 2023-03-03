import cv2
import colorsys
from random import randrange

#colorNames = ('red', 'orange', 'yellow', 'green', 'aqua', 'cyan', 'blue', 'violet', 'magenta')
colorHues = (0, 30, 60, 120, 160, 200, 240, 270, 300, 360)

def getClosestHueIndex(hue: int) -> int:
    if hue < 0 or hue > 360: return 0
    for index, colorHue in enumerate(colorHues):
        if (hue == colorHue): return index
        if (hue > colorHue): continue
        if ((colorHue - hue) < (hue - colorHues[index - 1])):
            return index if (index < len(colorHues) - 1) else 0
        else: return index - 1

def getClosestHue(hue: int) -> int:
    return colorHues[getClosestHueIndex(hue)]

def getColorList():
    colorList = [0] * (len(colorHues) - 1)
    img = cv2.imread('img/cover.png')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(img_hsv)
    for iy, y in enumerate(h):
        for ix, x in enumerate(y):
            h[iy][ix] = getClosestHue(x*2)*0.5
            weight = int(0.0039 * v[iy][ix] * s[iy][ix])
            colorList[getClosestHueIndex(x*2)] += weight
            v[iy][ix] = weight
            s[iy][ix] = weight
    img_hsv = cv2.merge([h, s, v])
    img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite('img/cover2.png', img)
    maxCC = max(colorList)
    for index, col in enumerate(colorList):
        if maxCC > 0:
            colorList[index] = int(col*float(255/maxCC))
    return colorList

def getHex(colorList, nr = 1):
    colorListCopy = colorList.copy()
    if nr < 1: nr = 1
    maxid = 0
    for _ in range(nr):
        maxval = max(colorListCopy)
        if maxval == 0: return getRandomHex()
        maxid = colorListCopy.index(maxval)
        colorListCopy[maxid] = 0
    hue = colorHues[maxid]
    return hueToHex(hue)

def getRandomHex():
    rand = randrange(0,len(colorHues) - 2)
    print("Random Color")
    return hueToHex(colorHues[rand])

def hueToHex(hue):
    (r, g, b) = colorsys.hsv_to_rgb(hue/360, 1, 1)
    (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
    return '#%02x%02x%02x' % (r, g, b)