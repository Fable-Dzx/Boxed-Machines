#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盒装机器 (Boxed Machines) —— 16x16 像素贴图生成器
生成：机器顶/底/侧面贴图（25 台）、机械齿轮、盒装机壳
用法：python3 gen_textures.py <资源目录>
"""
import os
import sys
from PIL import Image, ImageDraw

RES = sys.argv[1] if len(sys.argv) > 1 else "."
BLOCK = os.path.join(RES, "assets", "boxedmachines", "textures", "block")
ITEM = os.path.join(RES, "assets", "boxedmachines", "textures", "item")
os.makedirs(BLOCK, exist_ok=True)
os.makedirs(ITEM, exist_ok=True)

# ---- 基础色板 ----
METAL_LIGHT = (184, 189, 196)
METAL_MID = (141, 147, 154)
METAL_DARK = (58, 63, 68)
METAL_BORDER = (38, 42, 47)
PANEL_BORDER = (30, 33, 37)

# ---- 机器: 面板色, 图标色 ----
MACHINES = {
    "iron_farm":            ((200, 204, 210), (55, 66, 77)),
    "fishing_machine":      ((63, 127, 212), (234, 242, 251)),
    "lava_machine":         ((232, 118, 31), (255, 233, 201)),
    "lava_chicken_machine": ((217, 95, 43),  (255, 243, 224)),
    "cobblestone_machine":  ((139, 144, 150), (58, 63, 69)),
    "mob_farm":             ((91, 74, 120),  (232, 226, 242)),
    "gold_farm":            ((232, 197, 49), (92, 71, 5)),
    "honey_farm":           ((217, 154, 31), (92, 58, 5)),
    "sugarcane_farm":       ((88, 160, 67),  (234, 247, 226)),
    "melon_farm":           ((111, 191, 63), (35, 74, 18)),
    "cactus_farm":          ((62, 125, 58),  (217, 240, 210)),
    "bamboo_farm":          ((143, 174, 74), (45, 61, 16)),
    "string_farm":          ((207, 201, 184), (90, 83, 66)),
    "bone_farm":            ((232, 226, 208), (107, 101, 82)),
    "ender_pearl_farm":     ((29, 106, 99),  (213, 245, 240)),
    "xp_machine":           ((62, 207, 143), (10, 61, 40)),
    "egg_farm":             ((232, 220, 192), (107, 92, 58)),
    "wool_farm":            ((236, 236, 236), (74, 74, 74)),
    "beef_machine":         ((138, 74, 42),  (242, 220, 200)),
    "moss_farm":            ((92, 156, 58),  (28, 58, 16)),
    "mushroom_farm":        ((160, 90, 58),  (242, 226, 210)),
    "deepslate_machine":    ((74, 79, 87),   (207, 212, 220)),
    "quartz_farm":          ((224, 220, 210), (107, 103, 92)),
    "slime_farm":           ((127, 207, 63), (31, 74, 12)),
    "redstone_machine":     ((192, 58, 42),  (255, 233, 224)),
}


def _icon_panel(name, panel, icon_color):
    """在 16x16 上画一个带图标的机器侧面。"""
    img = Image.new("RGB", (16, 16), METAL_MID)
    d = ImageDraw.Draw(img)
    # 外边框
    d.rectangle([0, 0, 15, 15], outline=METAL_BORDER)
    # 顶部/左侧高光
    d.line([(1, 1), (14, 1)], fill=METAL_LIGHT)
    d.line([(1, 1), (1, 14)], fill=METAL_LIGHT)
    # 底部/右侧阴影
    d.line([(1, 14), (14, 14)], fill=METAL_DARK)
    d.line([(14, 1), (14, 14)], fill=METAL_DARK)
    # 中央面板 10x10
    d.rectangle([3, 3, 12, 12], fill=panel)
    d.rectangle([3, 3, 12, 12], outline=PANEL_BORDER)
    # 图标 8x8 居中
    icon = Image.new("RGB", (8, 8), panel)
    _draw_icon(ImageDraw.Draw(icon), name, icon_color, panel)
    img.paste(icon, (4, 4))
    return img


def _draw_icon(d, name, fg, bg):
    """在 8x8 画布上绘制简单像素图标。"""
    def dot(x, y):
        d.point((x, y), fill=fg)

    def rect(x1, y1, x2, y2):
        d.rectangle([x1, y1, x2, y2], fill=fg)

    def ell(x1, y1, x2, y2):
        d.ellipse([x1, y1, x2, y2], fill=fg)

    def poly(*pts):
        d.polygon(list(pts), fill=fg)

    if name == "ingot":
        rect(0, 3, 7, 4); rect(1, 2, 2, 5); rect(5, 2, 6, 5)
    elif name == "fish":
        ell(0, 2, 5, 6); poly((5, 2, 7, 4, 5, 6)); dot(2, 4)
    elif name == "drop":
        poly((4, 0, 7, 4, 4, 7, 1, 4))
    elif name == "chicken":
        ell(1, 1, 6, 6); rect(3, 0, 4, 1); dot(3, 3); dot(5, 3)
    elif name == "rock":
        poly((0, 4, 2, 1, 5, 0, 7, 2, 7, 5, 4, 7, 1, 6))
    elif name == "skull":
        ell(1, 0, 6, 5); rect(2, 5, 5, 7); dot(2, 2); dot(5, 2)
    elif name == "coin":
        d.ellipse([1, 1, 6, 6], outline=fg); d.ellipse([2, 2, 5, 5], outline=fg)
    elif name == "honey":
        poly((4, 0, 7, 2, 7, 5, 4, 7, 1, 5, 1, 2))
        d.line([(1, 3), (7, 3)], fill=fg); d.line([(2, 1), (6, 1)], fill=fg); d.line([(2, 6), (6, 6)], fill=fg)
    elif name == "cane":
        rect(1, 1, 2, 6); rect(4, 0, 5, 6)
    elif name == "melon":
        poly((4, 0, 7, 4, 4, 7, 1, 4)); d.line([(4, 1), (6, 4)], fill=fg); d.line([(2, 4), (4, 6)], fill=fg)
    elif name == "cactus":
        rect(3, 0, 4, 7); rect(1, 2, 3, 3); rect(5, 1, 7, 3)
    elif name == "bamboo":
        rect(1, 0, 1, 7); rect(4, 0, 4, 7)
        d.line([(1, 2), (4, 2)], fill=fg); d.line([(1, 4), (4, 4)], fill=fg); d.line([(1, 6), (4, 6)], fill=fg)
    elif name == "string":
        d.line([(0, 5), (2, 2), (4, 5), (6, 2), (7, 4)], fill=fg)
    elif name == "bone":
        poly((0, 2, 2, 2, 2, 0, 4, 0, 4, 2, 7, 2, 7, 5, 4, 5, 4, 7, 2, 7, 2, 5, 0, 5))
    elif name == "pearl":
        ell(1, 1, 6, 6); dot(3, 3)
    elif name == "bottle":
        rect(2, 1, 5, 2); rect(1, 2, 6, 7); rect(1, 5, 6, 6)
    elif name == "egg":
        ell(2, 0, 5, 7); dot(3, 3)
    elif name == "wool":
        ell(1, 2, 4, 5); ell(3, 1, 6, 4); ell(2, 4, 5, 7); ell(4, 3, 7, 6)
    elif name == "steak":
        poly((0, 2, 3, 1, 6, 2, 6, 5, 3, 6, 0, 5)); d.line([(2, 2), (5, 5)], fill=bg)
    elif name == "moss":
        dot(1, 2); dot(4, 1); dot(6, 3); dot(2, 4); dot(5, 5); dot(3, 6); dot(6, 6)
    elif name == "mushroom":
        d.arc([0, 1, 7, 4], 180, 360, fill=fg); rect(1, 3, 6, 4); rect(3, 4, 4, 7); dot(3, 0); dot(5, 1)
    elif name == "deepslate":
        poly((0, 4, 2, 2, 4, 1, 6, 2, 7, 4, 6, 6, 3, 7, 1, 6)); d.line([(2, 2), (6, 2)], fill=bg); d.line([(4, 1), (4, 4)], fill=bg)
    elif name == "quartz":
        poly((4, 0, 6, 2, 4, 7, 2, 2)); d.line([(4, 0), (4, 7)], fill=bg); d.line([(2, 2), (6, 2)], fill=bg)
    elif name == "slime":
        ell(0, 1, 7, 7); dot(2, 3); dot(5, 3); d.arc([1, 3, 6, 7], 0, 180, fill=bg)
    elif name == "redstone":
        d.line([(0, 6), (3, 3), (5, 4), (7, 1)], fill=fg)
        for x, y in [(0, 6), (3, 3), (5, 4), (7, 1)]:
            d.rectangle([x, y, x + 1, y + 1], fill=fg)


def machine_top():
    img = Image.new("RGB", (16, 16), METAL_MID)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], outline=METAL_BORDER)
    d.line([(1, 1), (14, 1)], fill=METAL_LIGHT)
    d.line([(1, 1), (1, 14)], fill=METAL_LIGHT)
    d.line([(1, 14), (14, 14)], fill=METAL_DARK)
    d.line([(14, 1), (14, 14)], fill=METAL_DARK)
    # 中央通风槽
    d.rectangle([4, 6, 11, 6], fill=METAL_DARK)
    d.rectangle([4, 8, 11, 8], fill=METAL_DARK)
    d.rectangle([4, 10, 11, 10], fill=METAL_DARK)
    # 四角铆钉
    for x, y in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        d.rectangle([x - 1, y - 1, x, y], fill=METAL_LIGHT)
        d.rectangle([x - 1, y - 1, x - 1, y - 1], fill=(230, 233, 238))
    return img


def machine_bottom():
    img = Image.new("RGB", (16, 16), METAL_DARK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], outline=METAL_BORDER)
    d.line([(1, 1), (14, 1)], fill=(84, 89, 95))
    # 底部横筋
    d.rectangle([2, 8, 13, 8], fill=METAL_MID)
    d.rectangle([2, 12, 13, 12], fill=(44, 48, 53))
    for x in [2, 13]:
        d.rectangle([x, 2, x + 1, 6], fill=METAL_MID)
    return img


def gear_item():
    img = Image.new("RGB", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 铁齿轮外环
    d.ellipse([2, 2, 13, 13], outline=(90, 96, 104))
    d.ellipse([1, 1, 14, 14], outline=(184, 189, 196))
    d.ellipse([4, 4, 11, 11], outline=(120, 126, 134))
    # 齿（上下左右 + 对角）
    for x, y in [(6, 0), (9, 0), (6, 14), (9, 14), (0, 6), (0, 9), (14, 6), (14, 9)]:
        d.rectangle([x, y, x + 1, y + 1], fill=(184, 189, 196))
    # 中心红石
    d.rectangle([6, 6, 9, 9], fill=(200, 58, 42))
    d.rectangle([6, 6, 7, 7], fill=(255, 120, 90))
    return img


def casing_item():
    img = Image.new("RGB", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 铜盒主体
    d.rectangle([2, 3, 13, 13], fill=(201, 138, 74))
    d.rectangle([2, 3, 13, 13], outline=(90, 60, 30))
    d.line([(2, 3), (13, 3)], fill=(235, 180, 120))
    # 盒盖
    d.rectangle([1, 1, 14, 3], fill=(160, 104, 52))
    d.rectangle([1, 1, 14, 3], outline=(70, 44, 20))
    # 正面小齿轮
    d.ellipse([6, 7, 9, 10], outline=(220, 226, 232))
    d.rectangle([7, 6, 8, 6], fill=(220, 226, 232))
    d.rectangle([7, 11, 8, 11], fill=(220, 226, 232))
    d.rectangle([5, 8, 5, 9], fill=(220, 226, 232))
    d.rectangle([10, 8, 10, 9], fill=(220, 226, 232))
    d.rectangle([7, 8, 8, 9], fill=(160, 58, 42))
    return img


def main():
    for mid, (panel, icon_color) in MACHINES.items():
        name = mid.replace("_machine", "").replace("_farm", "").replace("_", "")
        icons = {
            "iron": "ingot", "fishing": "fish", "lava": "drop", "lavachicken": "chicken",
            "cobblestone": "rock", "mob": "skull", "gold": "coin", "honey": "honey",
            "sugarcane": "cane", "melon": "melon", "cactus": "cactus", "bamboo": "bamboo",
            "string": "string", "bone": "bone", "enderpearl": "pearl", "xp": "bottle",
            "egg": "egg", "wool": "wool", "beef": "steak", "moss": "moss",
            "mushroom": "mushroom", "deepslate": "deepslate", "quartz": "quartz",
            "slime": "slime", "redstone": "redstone",
        }
        icon = icons.get(name, "ingot")
        _icon_panel(mid, panel, icon_color).save(os.path.join(BLOCK, f"{mid}_side.png"))
        print("side", mid, icon)
    machine_top().save(os.path.join(BLOCK, "machine_top.png"))
    machine_bottom().save(os.path.join(BLOCK, "machine_bottom.png"))
    gear_item().save(os.path.join(ITEM, "mechanism_gear.png"))
    casing_item().save(os.path.join(ITEM, "boxed_casing.png"))
    print("done textures")


if __name__ == "__main__":
    main()
