import random
import json
import os

colors = json.load(open(os.path.join(os.path.dirname(__file__), "colors.json")))
color_descriptions = json.load(open(os.path.join(os.path.dirname(__file__), "color_desc.json")))

tones = {
    "봄웜톤 (spring)": "SpringWarm",
    "가을웜톤 (fall)": "FallWarm",
    "여름쿨톤 (summer)": "SummerCool",
    "겨울쿨톤 (winter)": "WinterCool",
}


def get_random_color_from_tone(tone):
    return random.choice(colors[tones[tone]])

def get_color_description(color):
    return color_descriptions[color]


if __name__ == '__main__':
    a = get_random_color_from_tone("봄웜톤 (spring)")
    b = get_color_description(a)

    print(a, b)