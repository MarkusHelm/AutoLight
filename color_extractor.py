import cv2
import colorsys
from random import randrange
from os import path as os_path

class Color:
    def __init__(self, id=-1, hue=0, hex="#000000"):
        self.id = id
        self.hue = hue
        self.hex = hex

    id: int
    hue: int
    hex: str

class ColorExtractor:
    def __init__(self):
        self.AVAILABLE_HUES = [0, 30, 60, 120, 160, 200, 240, 270, 300]
        self.HUE_COUNT = len(self.AVAILABLE_HUES)
        self.SCANNER_HUES = [0, 120, 240, -1]
        self.SCANNER_WHITE_THRESHOLD = 5000

    def hue_to_hex(self, hue: int) -> str:
        if hue < 0:
            return "#FFFFFF"
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
        hue %= 360
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
                closest_hue_id = self.find_closest_hue_id(int(x)*2)
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

    def extract_colors(self, image_path: str) -> tuple[Color, Color, Color]:
        """primary color (0-8), secondary color (0-8), scanner color (0-3)"""
        collected_hues = self.collect_colors_from_image(image_path)

        color_scanner = Color()

        rgb_colors = [0] * 3
        rgb_colors[0] = collected_hues[0]
        rgb_colors[1] = collected_hues[3]
        rgb_colors[2] = collected_hues[6]
        if sum(rgb_colors) > self.SCANNER_WHITE_THRESHOLD:
            color_scanner.id = rgb_colors.index(max(rgb_colors)) * 3
        else:
            color_scanner.id = self.HUE_COUNT # white

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
        if color_scanner.id >= self.HUE_COUNT:
            color_scanner.hue = -1
            color_scanner.hex = "#FFFFFF"
        else:
            color_scanner.hue = self.AVAILABLE_HUES[color_scanner.id]
            color_scanner.hex = self.hue_to_hex(color_scanner.hue)

        return [color_1, color_2, color_scanner]
    
    def hue_to_string(self, hue: int) -> str:
        if hue == 0:
            return "red"
        if hue == 30:
            return "orange"
        if hue == 60:
            return "yellow"
        if hue == 120:
            return "green"
        if hue == 160:
            return "cyan"
        if hue == 200:
            return "aqua"
        if hue == 240:
            return "blue"
        if hue == 270:
            return "purple"
        if hue == 300:
            return "pink"
        if hue == -1:
            return "white"
        else:
            return "unknown"
    
def main():
    colorex = ColorExtractor()
    colors = colorex.extract_colors("img/cover_small.png")
    for color in colors:
        print(f"id: {color.id}, hue: {color.hue}, hex: {color.hex}, name: {colorex.hue_to_string(color.hue)}")

if __name__ == "__main__":
    main()