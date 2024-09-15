import os
from itertools import product
from random import randrange

from PIL import Image, ImageDraw


def convert_to_dec(num, base):
    res = 0
    for n in num:
        res = res * base + n
    return res


def convert_to(number, base, upper=True):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    if base > len(digits): return None
    result = ''
    result = digits[number % base] + result
    number //= base
    while number > 0:
        result = digits[number % base] + result
        number //= base
    return result.upper() if upper else result


def get_line(seed, rule, types):
    return [rule[convert_to_dec([seed[i - 1], seed[i], seed[(i + 1) % len(seed)]], types)] for i in
            range(len(seed))]


def get_image(img, rule, seed, types, width, height, stx=0, sty=0):
    pixels = img.load()
    line = seed
    if len(line) < width:
        pl = 0
    for y in range(sty, height + sty):
        for x in range(stx, width + stx):
            pixels[x, y] = palette[int(str(line[x - stx]), 36)]
        line = get_line(line, rule, types)
        if len(line) < width:
            pl = 0
    return img


def format_image(img, rule, seed, width, height, header, indent, stroke, stroke_color, seed_info):
    draw = ImageDraw.Draw(img)
    draw.rectangle((indent - stroke, indent - stroke, width + indent + stroke, header + indent + stroke),
                   fill=(255, 255, 255),
                   outline=stroke_color, width=stroke)
    draw.text((indent + width // 2, indent + header // 2),
              f'rule: {str(int("".join(map(str, rule)), types))}, {"".join(map(str, rule))}; seed: {seed_info}',
              fill=stroke_color, anchor='mm', align='center')
    return img


def gen_card(rule, seed, width, height, header, indent, stroke, background_color, stroke_color, seed_info):
    img = Image.new("RGB", (width + 2 * indent, height + header + 3 * indent), (255, 230, 200))
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (indent - stroke, header + 2 * indent - stroke, width + indent + stroke, height + header + 2 * indent + stroke),
        fill=background_color,
        outline=stroke_color, width=stroke)
    img = get_image(img, rule, seed, types, width, height, indent, header + 2 * indent)
    img = format_image(img, rule, seed, width, height, header, indent, stroke, stroke_color, seed_info)
    return img


types = 9

rule = [1, 0, 0, 1, 1, 0, 1, 0]
palette = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128)]
width, height, header, indent, stroke = tuple(map(lambda x: 2 * x, (300, 200, 40, 7, 2)))
background_color = (255, 230, 200)
stroke_color = (150, 120, 100)
seed_types = [([randrange(types) for _ in range(width)], 'random#1'),
              ([randrange(types) for _ in range(width)], 'random#2'),
              ([randrange(types) for _ in range(width)], 'random#3')]
for s in product((i for i in range(types)), repeat=2):
    s = list(s)
    if s[0] != s[1]:
        s[0] = convert_to(s[0], 36)
        s[1] = convert_to(s[1], 36)
        seed_types.append(
            (list(map(lambda x: int(x, 36), s[0] * (width // 2) + s[1] + s[0] * (width // 2 - ((width - 1) & 1)))),
             f'{s[0]}...{s[0]}{s[1]}{s[0]}...{s[0]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36), s[0] * (width // 2 - 1) + s[1] * 2 + s[0] * (width // 2 - ((width - 1) & 1)))),
                           f'{s[0]}...{s[0]}{s[1] * 2}{s[0]}...{s[0]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36), s[0] * (width // 2 - 2) + s[1] * 3 + s[0] * (width // 2 - ((width - 1) & 1)))),
                           f'{s[0]}...{s[0]}{s[1] * 3}{s[0]}...{s[0]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36),
                s[0] * (width // 2 - 2) + s[1] * 4 + s[0] * (width // 2 - 1 - ((width - 1) & 1)))),
                           f'{s[0]}...{s[0]}{s[1] * 4}{s[0]}...{s[0]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36), s[0] * (width // 2) + s[1] * (width // 2 + (width & 1)))),
                           f'{s[0]}...{s[0]}{s[1]}...{s[1]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36), s[0] * (width // 2 - 1) + s[1] + s[0] + s[1] * (width // 2 + (width & 1) - 1))),
                           f'{s[0]}...{s[0]}{s[1]}{s[0]}{s[1]}...{s[1]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36),
                s[0] * (width // 2 - 2) + s[1] * 2 + s[0] * 2 + s[1] * (width // 2 + (width & 1) - 2))),
                           f'{s[0]}...{s[0]}{s[1] * 2}{s[0] * 2}{s[1]}...{s[1]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36),
                s[0] * (width // 2 - 3) + s[1] * 3 + s[0] * 3 + s[1] * (width // 2 + (width & 1) - 3))),
                           f'{s[0]}...{s[0]}{s[1] * 3}{s[0] * 3}{s[1]}...{s[1]}'))
        seed_types.append((list(
            map(lambda x: int(x, 36),
                s[0] * (width // 2 - 4) + s[1] * 4 + s[0] * 4 + s[1] * (width // 2 + (width & 1) - 4))),
                           f'{s[0]}...{s[0]}{s[1] * 4}{s[0] * 4}{s[1]}...{s[1]}'))

    if not os.path.exists(f'All_rules_{types}_types'):
        os.mkdir(f'All_rules_{types}_types')
# for num_rule in range(types ** (types ** 3)):
#     rule = list(map(lambda x: int(x, 36), (types ** 3 * '0' + convert_to(num_rule, types))[-(types ** 3):]))
#     if not os.path.exists(f'All_rules_{types}_types/rule{num_rule}'):
#         os.mkdir(f'All_rules_{types}_types/rule{num_rule}')
#     for seed, seed_info in seed_types:
#         res = gen_card(rule, seed, width, height, header, indent, stroke, background_color, stroke_color, seed_info)
#         res.save(f'All_rules_{types}_types/rule{num_rule}/seed{seed_info}.png')
for i in range(100):
    num_rule = randrange(types ** (types ** 3))
    rule = list(map(lambda x: int(x, 36), (types ** 3 * '0' + convert_to(num_rule, types))[-(types ** 3):]))
    if types > 5:
        num_rule = convert_to(num_rule, 36)
        num_rule = f'{i}#{num_rule[:100]}'
    if not os.path.exists(f'All_rules_{types}_types/rule{num_rule}'):
        os.mkdir(f'All_rules_{types}_types/rule{num_rule}')
    for seed, seed_info in seed_types:
        res = gen_card(rule, seed, width, height, header, indent, stroke, background_color, stroke_color, seed_info)
        res.save(f'All_rules_{types}_types/rule{num_rule}/seed{seed_info}.png')
