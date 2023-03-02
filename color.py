from colorthief import ColorThief
import colorsys as cs
import cv2 as cv
import numpy as np
import os

def getRGB(file='img/cover.png'):
    color_thief = ColorThief(file)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def getHex(file='img/cover.png'):
    return '#%02x%02x%02x' % getRGB(file)

def getPaletteRGB(file='img/cover.png', count=4):
    color_thief = ColorThief(file)
    palette = color_thief.get_palette(color_count=count)
    return palette

def getPaletteHex(file='img/cover.png', count=4):
    palRGB = getPaletteRGB(file, count)
    palHex = []
    for rgb in palRGB:
        palHex.append('#%02x%02x%02x' % rgb)
    return palHex

def getPaletteSatRGB(file='img/cover.png', count=4):
    saturate()
    return getPaletteRGB(os.path.splitext(file)[0]+"_sat.png", count)

def getPaletteSatHex(file='img/cover.png', count=4):
    palRGB = getPaletteSatRGB(file, count)
    palHex = []
    for rgb in palRGB:
        palHex.append('#%02x%02x%02x' % rgb)
    return palHex

def saturate(file='img/cover.png'):
    img = cv.imread(file)
    imghsv = cv.cvtColor(img, cv.COLOR_RGB2HSV).astype("float32")
    (h, s, v) = cv.split(imghsv)
    s = s*10
    s = np.clip(s, 0, 255)
    imghsv = cv.merge([h, s, v])
    imgsat = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2RGB)
    cv.imwrite(os.path.splitext(file)[0]+"_sat.png", imgsat) 
