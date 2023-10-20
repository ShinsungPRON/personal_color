import random
import json

colors = json.load(open("/Users/flyahn06/code/PRON/personal_color/color_extractor/colors.json"))
tones = {
    "봄웜톤 (spring)": "SpringWarm",
    "가을웜톤 (fall)": "FallWarm",
    "여름쿨톤 (summer)": "SummerCool",
    "겨울쿨톤 (winter)": "WinterCool",
}


def get_random_color_from_tone(tone):
    return random.choice(colors[tones[tone]])


if __name__ == '__main__':
    print(get_random_color_from_tone('봄웜톤 (spring)'))