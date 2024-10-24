import cv2
import colorsys
from random import randrange
from os import path as os_path

class Color:
    id: int
    hue: int
    hex: str

class ColorExtractor:
    def __init__(self):
        self.AVAILABLE_HUES = [0, 30, 60, 120, 160, 200, 240, 270, 300]
        self.HUE_COUNT = len(self.AVAILABLE_HUES)

    def hue_to_hex(self, hue: int) -> str:
        hue = hue % 360
        (r, g, b) = colorsys.hsv_to_rgb(hue/360, 1, 1)
        (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
        return '#%02x%02x%02x' % (r, g, b)
    
    def colors_are_neighbors(self, hue_id_1, hue_id_2) -> bool:
        if (hue_id_1 - 1) % self.HUE_COUNT == hue_id_2 or (hue_id_1 + 1) % self.HUE_COUNT == hue_id_2:
            return True
        return False
    
    def find_closest_hue_id(self, hue: int) -> int:
        def circular_distance(a: int, b: int) -> int:
            return min(abs(a - b), 360 - abs(a - b))
        
        hue = hue % 360
        closest_hue = min(self.AVAILABLE_HUES, key=lambda x:circular_distance(x, hue))
        return self.AVAILABLE_HUES.index(closest_hue)

    def collect_colors_from_image(self, image_path: str, debug=True) -> list[int]:
        print("  Collecting colors: ", end="")
        collected_hues = [0] * self.HUE_COUNT

        if not os_path.exists(image_path):
            print("Image not found")
            return collected_hues

        img = cv2.imread(image_path)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        (h, s, v) = cv2.split(img_hsv)
        for iy, y in enumerate(h):
            for ix, x in enumerate(y):
                closest_hue_id = self.find_closest_hue_id(x*2)
                h[iy][ix] = self.AVAILABLE_HUES[closest_hue_id]*0.5
                weight = int(0.0039 * v[iy][ix] * (s[iy][ix] if s[iy][ix] > 32 else 0))
                collected_hues[closest_hue_id] += weight
                if debug:
                    v[iy][ix] = weight
                    s[iy][ix] = weight
        if debug:
            debug_img_hsv = cv2.merge([h, s, v])
            debug_img = cv2.cvtColor(debug_img_hsv, cv2.COLOR_HSV2BGR)
            cv2.imwrite(image_path.split(".")[0] + "_debug.png", debug_img)
        print(collected_hues)
        return collected_hues

    def extract_2_colors(self, image_path: str) -> tuple[Color, Color]:
        collected_hues = self.collect_colors_from_image(image_path)

        color_1 = Color()

        if sum(collected_hues) > 0:
            print("  1 Searching primary color")
            color_1_weight = max(collected_hues)
            color_1.id = collected_hues.index(color_1_weight)
            collected_hues[color_1.id] = 0
        else:
            print("  1 Random primary color")
            color_1.id = randrange(0, self.HUE_COUNT - 1)
                
        color_2 = Color()
        color_2_weight = 0

        if sum(collected_hues) > 0:
            print("  2 Searching secondary color")
            color_2_weight = max(collected_hues)
            color_2.id = collected_hues.index(color_2_weight)
            collected_hues[color_2.id] = 0
            # remove primary color neighbors
            collected_hues[(color_1.id+1)%self.HUE_COUNT] = 0
            collected_hues[(color_1.id+self.HUE_COUNT-1)%self.HUE_COUNT] = 0
        else:
            print("  2 Random secondary color")
            # choose random color that is not a neighbor of primary color
            random_offset = randrange(2, self.HUE_COUNT - 2)
            color_2.id = (color_1.id + random_offset) % self.HUE_COUNT

        if sum(collected_hues) > 0 and self.colors_are_neighbors(color_1.id, color_2.id):
            color_3 = Color()
            print("    Searching for alternative color")
            color_3_weight = max(collected_hues)
            color_3.id = collected_hues.index(color_3_weight)

            if color_3_weight * 3 >= color_2_weight:
                print("    Changing to alternative color")
                color_2 = color_3

        color_1.hue = self.AVAILABLE_HUES[color_1.id]
        color_2.hue = self.AVAILABLE_HUES[color_2.id]
        color_1.hex = self.hue_to_hex(color_1.hue)
        color_2.hex = self.hue_to_hex(color_2.hue)

        return [color_1, color_2]