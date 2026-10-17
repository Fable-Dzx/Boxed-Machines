#!/usr/bin/env python3
"""
盒装机器 (Boxed Machines) — 资源文件生成脚本
生成所有 JSON 资源文件（模型、方块状态、配方、翻译）和贴图纹理。
"""
import json
import os
import struct
import zlib
import math

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "src/main/resources/assets/boxedmachines")
DATA = os.path.join(BASE, "src/main/resources/data/boxedmachines")

# ===== 27 种机器定义 =====
MACHINES = [
    # (id, 中文名, 英文名, 颜色hex, 类别中文, 类别英文)
    # 刷怪农场
    ("boxed_iron_farm",           "盒装刷铁机",       "Boxed Iron Farm",           "#D8D8D8", "刷怪农场", "Mob Farm"),
    ("boxed_gold_farm",           "盒装刷金机",       "Boxed Gold Farm",           "#FED959", "刷怪农场", "Mob Farm"),
    ("boxed_guardian_farm",       "盒装刷钩机",       "Boxed Guardian Farm",       "#5BA89A", "刷怪农场", "Mob Farm"),
    ("boxed_blaze_farm",          "盒装烈焰刷怪机",   "Boxed Blaze Farm",          "#FFAA00", "刷怪农场", "Mob Farm"),
    ("boxed_enderman_farm",       "盒装末影人机",     "Boxed Enderman Farm",       "#16162E", "刷怪农场", "Mob Farm"),
    ("boxed_creeper_farm",        "盒装苦力怕机",     "Boxed Creeper Farm",        "#4CAF50", "刷怪农场", "Mob Farm"),
    ("boxed_skeleton_farm",       "盒装骷髅机",       "Boxed Skeleton Farm",       "#C8C8C8", "刷怪农场", "Mob Farm"),
    ("boxed_zombie_farm",         "盒装僵尸机",       "Boxed Zombie Farm",         "#2D7835", "刷怪农场", "Mob Farm"),
    ("boxed_spider_farm",         "盒装蜘蛛机",       "Boxed Spider Farm",         "#5C1A1A", "刷怪农场", "Mob Farm"),
    ("boxed_slime_farm",          "盒装史莱姆机",     "Boxed Slime Farm",          "#7EC850", "刷怪农场", "Mob Farm"),
    ("boxed_witch_farm",          "盒装女巫机",       "Boxed Witch Farm",          "#4A3656", "刷怪农场", "Mob Farm"),
    ("boxed_wither_skeleton_farm","盒装凋灵骷髅机",   "Boxed Wither Skeleton Farm","#1A1A1A", "刷怪农场", "Mob Farm"),
    # 动物农场
    ("boxed_chicken_cooker",      "盒装岩浆烤鸡机",   "Boxed Chicken Cooker",      "#E85030", "动物农场", "Animal Farm"),
    ("boxed_chicken_farm",        "盒装养鸡机",       "Boxed Chicken Farm",        "#F5F5DC", "动物农场", "Animal Farm"),
    ("boxed_cow_farm",            "盒装养牛机",       "Boxed Cow Farm",            "#6B4226", "动物农场", "Animal Farm"),
    ("boxed_sheep_farm",          "盒装养羊机",       "Boxed Sheep Farm",          "#E8E8E8", "动物农场", "Animal Farm"),
    ("boxed_pig_farm",            "盒装养猪机",       "Boxed Pig Farm",            "#E89B9B", "动物农场", "Animal Farm"),
    # 资源生成
    ("boxed_lava_machine",        "盒装岩浆机",       "Boxed Lava Machine",        "#CF4A16", "资源生成", "Resource Gen"),
    ("boxed_cobblestone_machine", "盒装造石机",       "Boxed Cobblestone Machine", "#8B8B8B", "资源生成", "Resource Gen"),
    ("boxed_snow_machine",        "盒装刷雪机",       "Boxed Snow Machine",        "#E8F4FF", "资源生成", "Resource Gen"),
    ("boxed_ice_machine",         "盒装冰机",         "Boxed Ice Machine",         "#99CCFF", "资源生成", "Resource Gen"),
    # 植物农场
    ("boxed_auto_farm",           "盒装自动农场",     "Boxed Auto Farm",           "#8BC34A", "植物农场", "Plant Farm"),
    ("boxed_sugarcane_machine",   "盒装甘蔗机",       "Boxed Sugarcane Machine",   "#90C060", "植物农场", "Plant Farm"),
    ("boxed_cactus_machine",      "盒装仙人掌机",     "Boxed Cactus Machine",      "#1B6B1A", "植物农场", "Plant Farm"),
    ("boxed_tree_farm",           "盒装伐木机",       "Boxed Tree Farm",           "#795548", "植物农场", "Plant Farm"),
    ("boxed_fishing_machine",     "盒装钓鱼机",       "Boxed Fishing Machine",     "#2196F3", "植物农场", "Plant Farm"),
    # 特殊
    ("boxed_raid_farm",           "盒装袭击机",       "Boxed Raid Farm",           "#B71C1C", "特殊", "Special"),
]

# 核心组件（27种，每种机器对应一个）
CORES = [(m[0].replace("boxed_", "") + "_core", m[1] + "核心", m[2] + " Core") for m in MACHINES]

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def darken(color, factor=0.6):
    return tuple(max(0, int(c * factor)) for c in color)

def lighten(color, factor=1.4):
    return tuple(min(255, int(c * factor)) for c in color)


# ===================================================================
#  PNG 生成（纯 Python，无外部依赖）
# ===================================================================
def make_png(width, height, pixels):
    """生成 PNG 文件。pixels 是 [(r,g,b,a), ...] 列表，行优先。"""
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))

    raw = b""
    for y in range(height):
        raw += b"\x00"  # filter none
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            raw += struct.pack("BBBB", r, g, b, a)

    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return header + ihdr + idat + iend


def generate_machine_texture(color_hex, path, size=16):
    """生成一台机器的 16x16 贴图。"""
    color = hex_to_rgb(color_hex)
    frame = (80, 80, 85)       # 边框深灰
    frame_light = (120, 120, 125)  # 边框高光
    inner = color
    inner_dark = darken(color, 0.7)
    inner_light = lighten(color, 1.2)
    detail = darken(color, 0.5)

    pixels = []
    for y in range(size):
        for x in range(size):
            # 外框 (2px)
            if x < 2 or x >= size-2 or y < 2 or y >= size-2:
                # 左上高光
                if x < 2 or y < 2:
                    pixels.append((*frame_light, 255))
                else:
                    pixels.append((*frame, 255))
            # 内面板 (2-13)
            elif 2 <= x <= 13 and 2 <= y <= 13:
                # 内边框
                if x == 2 or y == 2:
                    pixels.append((*inner_light, 255))
                elif x == 13 or y == 13:
                    pixels.append((*inner_dark, 255))
                # 中间装饰图案
                elif 5 <= x <= 10 and 5 <= y <= 10:
                    # 小方块图案
                    if (x + y) % 3 == 0:
                        pixels.append((*detail, 255))
                    else:
                        pixels.append((*inner, 255))
                else:
                    pixels.append((*inner, 255))
            else:
                pixels.append((*inner_dark, 255))

    # 螺丝孔（四角内嵌）
    corners = [(3, 3), (3, 12), (12, 3), (12, 12)]
    for cx, cy in corners:
        idx = cy * size + cx
        if idx < len(pixels):
            pixels[idx] = (40, 40, 40, 255)

    png_data = make_png(size, size, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


def generate_side_texture(color_hex, path, size=16):
    """生成侧面贴图（比正面简单）"""
    color = hex_to_rgb(color_hex)
    frame = (70, 70, 75)
    frame_light = (100, 100, 105)
    panel = darken(color, 0.85)
    panel_light = lighten(darken(color, 0.85), 1.15)

    pixels = []
    for y in range(size):
        for x in range(size):
            if x < 1 or x >= size-1 or y < 1 or y >= size-1:
                if x < 1 or y < 1:
                    pixels.append((*frame_light, 255))
                else:
                    pixels.append((*frame, 255))
            elif x == 1 or y == 1:
                pixels.append((*panel_light, 255))
            elif x == size-2 or y == size-2:
                pixels.append((*darken(panel, 0.7), 255))
            else:
                # 水平条纹装饰
                if y % 4 == 0:
                    pixels.append((*darken(panel, 0.9), 255))
                else:
                    pixels.append((*panel, 255))

    png_data = make_png(size, size, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


def generate_top_texture(path, size=16):
    """生成顶面贴图（通用灰色）"""
    base = (90, 90, 95)
    light = (110, 110, 115)
    dark = (70, 70, 75)
    pixels = []
    for y in range(size):
        for x in range(size):
            if x < 1 or x >= size-1 or y < 1 or y >= size-1:
                if x < 1 or y < 1:
                    pixels.append((*light, 255))
                else:
                    pixels.append((*dark, 255))
            else:
                if (x + y) % 2 == 0:
                    pixels.append((*base, 255))
                else:
                    pixels.append((*darken(base, 0.92), 255))
    png_data = make_png(size, size, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


def generate_casing_textures():
    """生成机器外壳的贴图"""
    base = (140, 145, 155)
    frame = (100, 105, 115)
    light = (170, 175, 185)

    pixels = []
    for y in range(16):
        for x in range(16):
            if x < 1 or x >= 15 or y < 1 or y >= 15:
                pixels.append((*frame, 255))
            elif x == 1 or y == 1:
                pixels.append((*light, 255))
            elif x == 14 or y == 14:
                pixels.append((*darken(base, 0.7), 255))
            else:
                # 金属质感
                if (x * 3 + y * 7) % 5 == 0:
                    pixels.append((*lighten(base, 1.1), 255))
                else:
                    pixels.append((*base, 255))
    path = os.path.join(ASSETS, "textures/block/machine_casing.png")
    png_data = make_png(16, 16, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


def generate_gui_texture():
    """生成 GUI 背景贴图 (256x256)"""
    w, h = 256, 256
    pixels = [None] * (w * h)

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2):
            for x in range(x1, x2):
                if 0 <= x < w and 0 <= y < h:
                    pixels[y * w + x] = color

    def fill_border(x1, y1, x2, y2, border, inner):
        fill_rect(x1, y1, x2, y2, border)
        fill_rect(x1+1, y1+1, x2-1, y2-1, inner)

    # 背景填充为透明（用深紫替代，MC会处理）
    fill_rect(0, 0, w, h, (0, 0, 0, 0))

    # 主容器背景 (0,0) - 176x80
    fill_border(0, 0, 176, 80, (60, 60, 65, 255), (198, 198, 205, 255))

    # 产出槽区域 (7, 17) - 162x54
    fill_rect(7, 17, 169, 71, (139, 139, 149, 255))

    # 36 个槽位 (3行x9列)，每个 18x18，起始 (8, 18)
    for row in range(3):
        for col in range(9):
            sx = 8 + col * 18
            sy = 18 + row * 18
            fill_border(sx, sy, sx+16, sy+16, (55, 55, 60, 255), (139, 139, 149, 255))

    # 玩家背包区域 (0, 85) - 176x58
    fill_border(0, 85, 176, 143, (60, 60, 65, 255), (198, 198, 205, 255))

    # 3行背包槽 (8, 86)
    for row in range(3):
        for col in range(9):
            sx = 8 + col * 18
            sy = 86 + row * 18
            fill_border(sx, sy, sx+16, sy+16, (55, 55, 60, 255), (139, 139, 149, 255))

    # 快捷栏 (0, 143) - 176x24
    fill_border(0, 143, 176, 167, (60, 60, 65, 255), (198, 198, 205, 255))
    for col in range(9):
        sx = 8 + col * 18
        sy = 144
        fill_border(sx, sy, sx+16, sy+16, (55, 55, 60, 255), (139, 139, 149, 255))

    # 填充所有 None 像素
    for i in range(len(pixels)):
        if pixels[i] is None:
            pixels[i] = (0, 0, 0, 0)

    path = os.path.join(ASSETS, "textures/gui/container/boxed_machine.png")
    png_data = make_png(w, h, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


def generate_icon():
    """生成模组图标 (128x128)"""
    size = 128
    pixels = []
    bg = (50, 55, 65)
    frame = (100, 105, 115)
    accent = (255, 170, 0)

    for y in range(size):
        for x in range(size):
            # 圆角矩形
            cx, cy = size // 2, size // 2
            dx = abs(x - cx)
            dy = abs(y - cy)
            radius = 56

            if dx > radius or dy > radius:
                pixels.append((0, 0, 0, 0))
            elif dx > radius - 4 or dy > radius - 4:
                pixels.append((*frame, 255))
            else:
                # 内部
                if 20 <= dx <= 44 and 20 <= dy <= 44:
                    pixels.append((*accent, 255))
                elif dx <= 20 and dy <= 20:
                    pixels.append((*lighten(bg, 1.2), 255))
                else:
                    pixels.append((*bg, 255))

    path = os.path.join(ASSETS, "icon.png")
    png_data = make_png(size, size, pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_data)


# ===================================================================
#  JSON 生成
# ===================================================================
def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_blockstates():
    for mid, cn, en, color, cat_cn, cat_en in MACHINES:
        data = {
            "variants": {
                "facing=north": {"model": f"boxedmachines:block/{mid}"},
                "facing=south": {"model": f"boxedmachines:block/{mid}", "y": 180},
                "facing=west":  {"model": f"boxedmachines:block/{mid}", "y": 270},
                "facing=east":  {"model": f"boxedmachines:block/{mid}", "y": 90}
            }
        }
        write_json(os.path.join(ASSETS, f"blockstates/{mid}.json"), data)


def generate_block_models():
    for mid, cn, en, color, cat_cn, cat_en in MACHINES:
        data = {
            "parent": "minecraft:block/orientable",
            "textures": {
                "top": f"boxedmachines:block/machine_top",
                "bottom": f"boxedmachines:block/machine_top",
                "side": f"boxedmachines:block/{mid}_side",
                "front": f"boxedmachines:block/{mid}_front"
            }
        }
        write_json(os.path.join(ASSETS, f"models/block/{mid}.json"), data)


def generate_item_models():
    # 方块物品
    for mid, cn, en, color, cat_cn, cat_en in MACHINES:
        data = {
            "parent": f"boxedmachines:block/{mid}"
        }
        write_json(os.path.join(ASSETS, f"models/item/{mid}.json"), data)

    # 机器外壳
    write_json(os.path.join(ASSETS, "models/item/machine_casing.json"), {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": "boxedmachines:item/machine_casing"}
    })

    # 红石芯片
    write_json(os.path.join(ASSETS, "models/item/redstone_chip.json"), {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": "boxedmachines:item/redstone_chip"}
    })

    # 核心组件
    for core_id, cn, en in CORES:
        write_json(os.path.join(ASSETS, f"models/item/{core_id}.json"), {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"boxedmachines:item/{core_id}"}
        })


def generate_machine_casing_block():
    """机器外壳的方块状态和模型（用于配方展示，不可放置）"""
    write_json(os.path.join(ASSETS, "blockstates/machine_casing.json"), {
        "variants": {"": {"model": "boxedmachines:block/machine_casing"}}
    })
    write_json(os.path.join(ASSETS, "models/block/machine_casing.json"), {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": "boxedmachines:block/machine_casing"}
    })
    write_json(os.path.join(ASSETS, "models/item/machine_casing.json"), {
        "parent": "boxedmachines:block/machine_casing"
    })


def generate_lang():
    zh = {
        "itemGroup.boxedmachines.main": "盒装机器",
        "item.boxedmachines.machine_casing": "机器外壳",
        "item.boxedmachines.redstone_chip": "红石芯片",
    }
    en = {
        "itemGroup.boxedmachines.main": "Boxed Machines",
        "item.boxedmachines.machine_casing": "Machine Casing",
        "item.boxedmachines.redstone_chip": "Redstone Chip",
    }

    for mid, cn, en_name, color, cat_cn, cat_en in MACHINES:
        zh[f"block.boxedmachines.{mid}"] = cn
        en[f"block.boxedmachines.{mid}"] = en_name

    for core_id, cn, en_name in CORES:
        zh[f"item.boxedmachines.{core_id}"] = cn
        en[f"item.boxedmachines.{core_id}"] = en_name

    write_json(os.path.join(ASSETS, "lang/zh_cn.json"), zh)
    write_json(os.path.join(ASSETS, "lang/en_us.json"), en)


def generate_recipes():
    """生成所有合成配方"""
    recipe_dir = os.path.join(DATA, "recipe")

    # ===== 第1级：基础材料 =====

    # 机器外壳
    write_json(os.path.join(recipe_dir, "machine_casing.json"), {
        "type": "minecraft:crafting_shaped",
        "pattern": ["IRI", "OQO", "IRI"],
        "key": {
            "I": "minecraft:iron_ingot",
            "R": "minecraft:redstone",
            "O": "minecraft:obsidian",
            "Q": "minecraft:quartz"
        },
        "result": {"id": "boxedmachines:machine_casing", "count": 2}
    })

    # 红石芯片
    write_json(os.path.join(recipe_dir, "redstone_chip.json"), {
        "type": "minecraft:crafting_shaped",
        "pattern": ["GRG", "RDR", "GRG"],
        "key": {
            "G": "minecraft:gold_ingot",
            "R": "minecraft:redstone_block",
            "D": "minecraft:diamond"
        },
        "result": {"id": "boxedmachines:redstone_chip", "count": 1}
    })

    # ===== 第2级：核心组件 =====
    # 每种核心 = 机器外壳 + 红石芯片 + 特定材料

    core_recipes = {
        # id: (pattern, key, extra_desc)
        "iron_farm_core": {
            "pattern": ["IFI", "CMC", "IFI"],
            "key": {"I": "minecraft:iron_ingot", "F": "minecraft:poppy",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "gold_farm_core": {
            "pattern": ["GFG", "CMC", "GFG"],
            "key": {"G": "minecraft:gold_ingot", "F": "minecraft:nether_wart",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "guardian_farm_core": {
            "pattern": ["PSP", "CMC", "PSP"],
            "key": {"P": "minecraft:prismarine_shard", "S": "minecraft:sea_lantern",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "blaze_farm_core": {
            "pattern": ["BRB", "CMC", "BRB"],
            "key": {"B": "minecraft:blaze_powder", "R": "minecraft:blaze_rod",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "enderman_farm_core": {
            "pattern": ["EOE", "CMC", "EOE"],
            "key": {"E": "minecraft:ender_pearl", "O": "minecraft:obsidian",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "creeper_farm_core": {
            "pattern": ["GTG", "CMC", "GTG"],
            "key": {"G": "minecraft:gunpowder", "T": "minecraft:tnt",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "skeleton_farm_core": {
            "pattern": ["BAB", "CMC", "BAB"],
            "key": {"B": "minecraft:bone", "A": "minecraft:bow",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "zombie_farm_core": {
            "pattern": ["RZR", "CMC", "RZR"],
            "key": {"R": "minecraft:rotten_flesh", "Z": "minecraft:zombie_head",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "spider_farm_core": {
            "pattern": ["SCS2", "CMC", "SCS2"],
            "key": {"S": "minecraft:string", "C": "boxedmachines:machine_casing",
                    "C2": "minecraft:cobweb", "M": "boxedmachines:redstone_chip"}
        },
        "slime_farm_core": {
            "pattern": ["SBS", "CMC", "SBS"],
            "key": {"S": "minecraft:slime_ball", "B": "minecraft:slime_block",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "witch_farm_core": {
            "pattern": ["PGP", "CMC", "PGP"],
            "key": {"P": "minecraft:glowstone_dust", "G": "minecraft:glass_bottle",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "wither_skeleton_farm_core": {
            "pattern": ["WSW", "CMC", "WSW"],
            "key": {"W": "minecraft:coal_block", "S": "minecraft:skeleton_skull",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "chicken_cooker_core": {
            "pattern": ["FLF", "CMC", "FLF"],
            "key": {"F": "minecraft:feather", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "chicken_farm_core": {
            "pattern": ["ESE", "CMC", "ESE"],
            "key": {"E": "minecraft:egg", "S": "minecraft:wheat_seeds",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "cow_farm_core": {
            "pattern": ["LWL", "CMC", "LWL"],
            "key": {"L": "minecraft:leather", "W": "minecraft:wheat",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "sheep_farm_core": {
            "pattern": ["WSW", "CMC", "WSW"],
            "key": {"W": "minecraft:white_wool", "S": "minecraft:shears",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "pig_farm_core": {
            "pattern": ["CRC",2, "CMC", "CRC"],
            "key": {"C": "minecraft:carrot", "R": "minecraft:golden_carrot",
                    "C2": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "lava_machine_core": {
            "pattern": ["OLO", "CMC", "OLO"],
            "key": {"O": "minecraft:obsidian", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "cobblestone_machine_core": {
            "pattern": ["WLW", "CMC", "WLW"],
            "key": {"W": "minecraft:water_bucket", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "snow_machine_core": {
            "pattern": ["SBS", "CMC", "SBS"],
            "key": {"S": "minecraft:snow_block", "B": "minecraft:blue_ice",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "ice_machine_core": {
            "pattern": ["IWI", "CMC", "IWI"],
            "key": {"I": "minecraft:packed_ice", "W": "minecraft:water_bucket",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "auto_farm_core": {
            "pattern": ["WHC", "CMC", "BPP"],
            "key": {"W": "minecraft:wheat", "H": "minecraft:iron_hoe",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip",
                    "B": "minecraft:beetroot", "P": "minecraft:potato"}
        },
        "sugarcane_machine_core": {
            "pattern": ["SSS", "CMC", "WWW"],
            "key": {"S": "minecraft:sugar_cane", "C": "boxedmachines:machine_casing",
                    "M": "boxedmachines:redstone_chip", "W": "minecraft:water_bucket"}
        },
        "cactus_machine_core": {
            "pattern": ["CSC", "CMC", "SAS"],
            "key": {"C": "minecraft:cactus", "S": "minecraft:sand",
                    "M": "boxedmachines:redstone_chip",
                    "A": "boxedmachines:machine_casing"}
        },
        "tree_farm_core": {
            "pattern": ["LSL", "CMC", "LSL"],
            "key": {"L": "minecraft:oak_log", "S": "minecraft:oak_sapling",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "fishing_machine_core": {
            "pattern": ["FRF", "CMC", "FRF"],
            "key": {"F": "minecraft:fishing_rod", "R": "minecraft:cod",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
        "raid_farm_core": {
            "pattern": ["OTO", "CMC", "OTO"],
            "key": {"O": "minecraft:ominous_bottle", "T": "minecraft:totem_of_undying",
                    "C": "boxedmachines:machine_casing", "M": "boxedmachines:redstone_chip"}
        },
    }

    for core_id, recipe in core_recipes.items():
        # 修正 pig_farm_core 的 pattern 问题
        pattern = recipe["pattern"]
        if isinstance(pattern[1], int):
            pattern = [pattern[0], pattern[2], pattern[3]]

        write_json(os.path.join(recipe_dir, f"{core_id}.json"), {
            "type": "minecraft:crafting_shaped",
            "pattern": pattern,
            "key": recipe["key"],
            "result": {"id": f"boxedmachines:{core_id}", "count": 1}
        })

    # ===== 第3级：机器成品 =====
    # 每台机器 = 对应核心 + 辅助材料 + 机器外壳

    machine_recipes = {
        "boxed_iron_farm": {
            "pattern": ["IVI", "CXC", "IPI"],
            "key": {"I": "minecraft:iron_block", "V": "minecraft:iron_ingot",
                    "C": "boxedmachines:iron_farm_core", "X": "boxedmachines:machine_casing",
                    "P": "minecraft:poppy"}
        },
        "boxed_gold_farm": {
            "pattern": ["GBG", "CXC", "GNG"],
            "key": {"G": "minecraft:gold_block", "B": "minecraft:blaze_powder",
                    "C": "boxedmachines:gold_farm_core", "X": "boxedmachines:machine_casing",
                    "N": "minecraft:nether_wart"}
        },
        "boxed_guardian_farm": {
            "pattern": ["PSP", "CXC", "PLP"],
            "key": {"P": "minecraft:prismarine", "S": "minecraft:sea_lantern",
                    "C": "boxedmachines:guardian_farm_core", "X": "boxedmachines:machine_casing",
                    "L": "minecraft:water_bucket"}
        },
        "boxed_blaze_farm": {
            "pattern": ["BRB", "CXC", "BFB"],
            "key": {"B": "minecraft:blaze_rod", "R": "minecraft:blaze_powder",
                    "C": "boxedmachines:blaze_farm_core", "X": "boxedmachines:machine_casing",
                    "F": "minecraft:fire_charge"}
        },
        "boxed_enderman_farm": {
            "pattern": ["EOE", "CXC", "EPE"],
            "key": {"E": "minecraft:ender_pearl", "O": "minecraft:obsidian",
                    "C": "boxedmachines:enderman_farm_core", "X": "boxedmachines:machine_casing",
                    "P": "minecraft:end_stone"}
        },
        "boxed_creeper_farm": {
            "pattern": ["GTG", "CXC", "GRG"],
            "key": {"G": "minecraft:gunpowder", "T": "minecraft:tnt",
                    "C": "boxedmachines:creeper_farm_core", "X": "boxedmachines:machine_casing",
                    "R": "minecraft:repeater"}
        },
        "boxed_skeleton_farm": {
            "pattern": ["BAB", "CXC", "BSB"],
            "key": {"B": "minecraft:bone_block", "A": "minecraft:arrow",
                    "C": "boxedmachines:skeleton_farm_core", "X": "boxedmachines:machine_casing",
                    "S": "minecraft:bow"}
        },
        "boxed_zombie_farm": {
            "pattern": ["RIR", "CXC", "RZR"],
            "key": {"R": "minecraft:rotten_flesh", "I": "minecraft:iron_ingot",
                    "C": "boxedmachines:zombie_farm_core", "X": "boxedmachines:machine_casing",
                    "Z": "minecraft:zombie_head"}
        },
        "boxed_spider_farm": {
            "pattern": ["SCS2", "CXC", "SES"],
            "key": {"S": "minecraft:string", "C": "minecraft:cobweb",
                    "C2": "boxedmachines:spider_farm_core", "X": "boxedmachines:machine_casing",
                    "E": "minecraft:spider_eye", "S2": "minecraft:fermented_spider_eye"}
        },
        "boxed_slime_farm": {
            "pattern": ["SBS", "CXC", "SHS"],
            "key": {"S": "minecraft:slime_ball", "B": "minecraft:slime_block",
                    "C": "boxedmachines:slime_farm_core", "X": "boxedmachines:machine_casing",
                    "H": "minecraft:honey_block"}
        },
        "boxed_witch_farm": {
            "pattern": ["PGP", "CXC", "PRP"],
            "key": {"P": "minecraft:glowstone_dust", "G": "minecraft:glass_bottle",
                    "C": "boxedmachines:witch_farm_core", "X": "boxedmachines:machine_casing",
                    "R": "minecraft:redstone_block"}
        },
        "boxed_wither_skeleton_farm": {
            "pattern": ["WSW", "CXC", "WNW"],
            "key": {"W": "minecraft:coal_block", "S": "minecraft:skeleton_skull",
                    "C": "boxedmachines:wither_skeleton_farm_core", "X": "boxedmachines:machine_casing",
                    "N": "minecraft:nether_star"}
        },
        "boxed_chicken_cooker": {
            "pattern": ["FLF", "CXC", "FLF"],
            "key": {"F": "minecraft:feather", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:chicken_cooker_core", "X": "boxedmachines:machine_casing"}
        },
        "boxed_chicken_farm": {
            "pattern": ["ESE", "CXC", "EHE"],
            "key": {"E": "minecraft:egg", "S": "minecraft:wheat_seeds",
                    "C": "boxedmachines:chicken_farm_core", "X": "boxedmachines:machine_casing",
                    "H": "minecraft:hay_block"}
        },
        "boxed_cow_farm": {
            "pattern": ["LWL", "CXC", "LHL"],
            "key": {"L": "minecraft:leather", "W": "minecraft:wheat",
                    "C": "boxedmachines:cow_farm_core", "X": "boxedmachines:machine_casing",
                    "H": "minecraft:hay_block"}
        },
        "boxed_sheep_farm": {
            "pattern": ["WSW", "CXC", "WHW"],
            "key": {"W": "minecraft:white_wool", "S": "minecraft:shears",
                    "C": "boxedmachines:sheep_farm_core", "X": "boxedmachines:machine_casing",
                    "H": "minecraft:hay_block"}
        },
        "boxed_pig_farm": {
            "pattern": ["CGC", "CXC", "CGC"],
            "key": {"C": "minecraft:carrot", "G": "minecraft:golden_carrot",
                    "C2": "boxedmachines:pig_farm_core", "X": "boxedmachines:machine_casing"}
        },
        "boxed_lava_machine": {
            "pattern": ["OLO", "CXC", "OBO"],
            "key": {"O": "minecraft:obsidian", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:lava_machine_core", "X": "boxedmachines:machine_casing",
                    "B": "minecraft:blaze_rod"}
        },
        "boxed_cobblestone_machine": {
            "pattern": ["WLP", "CXC", "PLW"],
            "key": {"W": "minecraft:water_bucket", "L": "minecraft:lava_bucket",
                    "C": "boxedmachines:cobblestone_machine_core", "X": "boxedmachines:machine_casing",
                    "P": "minecraft:piston"}
        },
        "boxed_snow_machine": {
            "pattern": ["SBS", "CXC", "SWS"],
            "key": {"S": "minecraft:snow_block", "B": "minecraft:blue_ice",
                    "C": "boxedmachines:snow_machine_core", "X": "boxedmachines:machine_casing",
                    "W": "minecraft:water_bucket"}
        },
        "boxed_ice_machine": {
            "pattern": ["IWI", "CXC", "IPI"],
            "key": {"I": "minecraft:packed_ice", "W": "minecraft:water_bucket",
                    "C": "boxedmachines:ice_machine_core", "X": "boxedmachines:machine_casing",
                    "P": "minecraft:piston"}
        },
        "boxed_auto_farm": {
            "pattern": ["WHC", "CXC", "BPH"],
            "key": {"W": "minecraft:wheat", "H": "minecraft:iron_hoe",
                    "C": "boxedmachines:auto_farm_core", "X": "boxedmachines:machine_casing",
                    "B": "minecraft:bone_meal", "P": "minecraft:potato"}
        },
        "boxed_sugarcane_machine": {
            "pattern": ["SSS", "CXC", "WWW"],
            "key": {"S": "minecraft:sugar_cane",
                    "C": "boxedmachines:sugarcane_machine_core", "X": "boxedmachines:machine_casing",
                    "W": "minecraft:water_bucket"}
        },
        "boxed_cactus_machine": {
            "pattern": ["CSC", "CXC", "SAS"],
            "key": {"C": "minecraft:cactus", "S": "minecraft:sand",
                    "A": "boxedmachines:cactus_machine_core", "X": "boxedmachines:machine_casing"}
        },
        "boxed_tree_farm": {
            "pattern": ["LSL", "CXC", "LAL"],
            "key": {"L": "minecraft:oak_log", "S": "minecraft:oak_sapling",
                    "C": "boxedmachines:tree_farm_core", "X": "boxedmachines:machine_casing",
                    "A": "minecraft:iron_axe"}
        },
        "boxed_fishing_machine": {
            "pattern": ["FRF", "CXC", "FBF"],
            "key": {"F": "minecraft:fishing_rod", "R": "minecraft:cod",
                    "C": "boxedmachines:fishing_machine_core", "X": "boxedmachines:machine_casing",
                    "B": "minecraft:water_bucket"}
        },
        "boxed_raid_farm": {
            "pattern": ["OTO", "CXC", "OEO"],
            "key": {"O": "minecraft:ominous_bottle", "T": "minecraft:totem_of_undying",
                    "C": "boxedmachines:raid_farm_core", "X": "boxedmachines:machine_casing",
                    "E": "minecraft:emerald_block"}
        },
    }

    for machine_id, recipe in machine_recipes.items():
        # 修正 pig_farm 和 spider_farm 的 key 冲突
        key = recipe["key"].copy()
        pattern = recipe["pattern"]

        # 特殊处理有 key 冲突的配方
        if machine_id == "boxed_spider_farm":
            pattern = ["SCW", "CXE", "FES"]
            key = {
                "S": "minecraft:string", "C": "minecraft:cobweb", "W": "minecraft:white_wool",
                "X": "boxedmachines:machine_casing",
                "E": "minecraft:spider_eye", "F": "minecraft:fermented_spider_eye",
            }
            # C2 被替换为 W (white_wool) 因为 spider_farm_core 用了 C
        elif machine_id == "boxed_pig_farm":
            pattern = ["CGC", "AXA", "CGC"]
            key = {
                "C": "minecraft:carrot", "G": "minecraft:golden_carrot",
                "A": "boxedmachines:pig_farm_core", "X": "boxedmachines:machine_casing"
            }

        write_json(os.path.join(recipe_dir, f"{machine_id}.json"), {
            "type": "minecraft:crafting_shaped",
            "pattern": pattern,
            "key": key,
            "result": {"id": f"boxedmachines:{machine_id}", "count": 1}
        })


def generate_item_textures():
    """生成物品贴图"""
    # 机器外壳物品贴图
    casing_color = (140, 145, 155)
    pixels = []
    for y in range(16):
        for x in range(16):
            if x < 2 or x >= 14 or y < 2 or y >= 14:
                if 2 <= x <= 13 and 2 <= y <= 13:
                    pixels.append((*casing_color, 255))
                else:
                    pixels.append((0, 0, 0, 0))
            elif x == 2 or y == 2:
                pixels.append((*lighten(casing_color, 1.3), 255))
            elif x == 13 or y == 13:
                pixels.append((*darken(casing_color, 0.7), 255))
            else:
                if (x + y) % 3 == 0:
                    pixels.append((*lighten(casing_color, 1.15), 255))
                else:
                    pixels.append((*casing_color, 255))
    path = os.path.join(ASSETS, "textures/item/machine_casing.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(make_png(16, 16, pixels))

    # 红石芯片
    chip_base = (200, 40, 40)
    gold = (220, 190, 50)
    pixels = []
    for y in range(16):
        for x in range(16):
            # 芯片形状：圆角矩形
            in_chip = (3 <= x <= 12 and 4 <= y <= 11)
            if in_chip:
                if x == 3 or y == 4:
                    pixels.append((*lighten(chip_base, 1.3), 255))
                elif x == 12 or y == 11:
                    pixels.append((*darken(chip_base, 0.7), 255))
                elif 5 <= x <= 10 and 6 <= y <= 9:
                    # 金线
                    if y == 6 or y == 9 or x == 5 or x == 10:
                        pixels.append((*gold, 255))
                    elif x == 7 or x == 8:
                        pixels.append((*gold, 255))
                    else:
                        pixels.append((*chip_base, 255))
                else:
                    pixels.append((*chip_base, 255))
            else:
                pixels.append((0, 0, 0, 0))
    path = os.path.join(ASSETS, "textures/item/redstone_chip.png")
    with open(path, "wb") as f:
        f.write(make_png(16, 16, pixels))

    # 核心组件贴图 — 每种核心用一个和机器相近的颜色，带中心标记
    for (mid, cn, en, color_hex, cat_cn, cat_en) in MACHINES:
        core_id = mid.replace("boxed_", "") + "_core"
        color = hex_to_rgb(color_hex)
        border = (60, 60, 70)
        center = lighten(color, 1.3)
        inner = darken(color, 0.8)

        pixels = []
        for y in range(16):
            for x in range(16):
                # 圆形
                dx, dy = x - 7.5, y - 7.5
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 7:
                    pixels.append((0, 0, 0, 0))
                elif dist > 6:
                    pixels.append((*border, 255))
                elif dist < 3:
                    # 中心亮点
                    pixels.append((*center, 255))
                elif dist < 3.5:
                    pixels.append((*inner, 255))
                else:
                    # 中间区域
                    if (x + y) % 4 == 0:
                        pixels.append((*lighten(inner, 1.2), 255))
                    else:
                        pixels.append((*inner, 255))

        path = os.path.join(ASSETS, f"textures/item/{core_id}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(make_png(16, 16, pixels))


# ===================================================================
#  主流程
# ===================================================================
if __name__ == "__main__":
    print("开始生成盒装机器模组资源文件...")

    print("  生成方块状态...")
    generate_blockstates()

    print("  生成方块模型...")
    generate_block_models()

    print("  生成物品模型...")
    generate_item_models()

    print("  生成机器外壳方块...")
    generate_machine_casing_block()

    print("  生成语言文件...")
    generate_lang()

    print("  生成合成配方...")
    generate_recipes()

    print("  生成方块贴图...")
    for mid, cn, en, color, cat_cn, cat_en in MACHINES:
        tex_dir = os.path.join(ASSETS, "textures/block")
        generate_machine_texture(color, os.path.join(tex_dir, f"{mid}_front.png"))
        generate_side_texture(color, os.path.join(tex_dir, f"{mid}_side.png"))
    generate_top_texture(os.path.join(ASSETS, "textures/block/machine_top.png"))

    print("  生成物品贴图...")
    generate_item_textures()

    print("  生成机器外壳贴图...")
    generate_casing_textures()

    print("  生成 GUI 贴图...")
    generate_gui_texture()

    print("  生成模组图标...")
    generate_icon()

    # 统计
    total_files = 0
    for root, dirs, files in os.walk(os.path.join(BASE, "src")):
        total_files += len(files)

    print(f"\n完成！共生成 {total_files} 个文件。")
    print(f"  机器数量: {len(MACHINES)}")
    print(f"  核心组件: {len(CORES)}")
    print(f"  方块贴图: {len(MACHINES) * 2 + 1} (正面+侧面+通用顶面)")
    print(f"  物品贴图: {2 + len(CORES)} (外壳+芯片+核心)")
