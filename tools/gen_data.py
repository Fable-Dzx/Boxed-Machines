#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盒装机器 (Boxed Machines) —— 数据文件生成器
生成：合成配方、战利品表、方块状态、方块模型、客户端物品模型、语言文件
用法：python3 gen_data.py <项目资源目录>
"""
import json
import os
import sys

MOD = "boxedmachines"
RES = sys.argv[1] if len(sys.argv) > 1 else "."

# id: (中文名, 英文名, 配方主料A, 配方辅料B)
MACHINES = {
    "iron_farm":            ("盒装刷铁机",     "Boxed Iron Farm",          "minecraft:iron_ingot",     "minecraft:iron_bars"),
    "fishing_machine":      ("盒装自动钓鱼机", "Boxed Auto-Fisher",        "minecraft:fishing_rod",    "minecraft:string"),
    "lava_machine":         ("盒装岩浆机",     "Boxed Lava Machine",       "minecraft:magma_cream",    "minecraft:obsidian"),
    "lava_chicken_machine": ("盒装岩浆烤鸡机", "Boxed Lava Chicken",       "minecraft:chicken",        "minecraft:magma_cream"),
    "cobblestone_machine":  ("盒装刷石机",     "Boxed Cobblestone",        "minecraft:cobblestone",    "minecraft:stone"),
    "mob_farm":             ("盒装刷怪机",     "Boxed Mob Farm",           "minecraft:rotten_flesh",   "minecraft:bone"),
    "gold_farm":            ("盒装刷金机",     "Boxed Gold Farm",          "minecraft:gold_ingot",     "minecraft:gold_nugget"),
    "honey_farm":           ("盒装刷蜜机",     "Boxed Honey Farm",         "minecraft:honey_bottle",   "minecraft:honeycomb"),
    "sugarcane_farm":       ("盒装甘蔗机",     "Boxed Sugarcane Farm",     "minecraft:sugar_cane",     "minecraft:sugar"),
    "melon_farm":           ("盒装瓜机",       "Boxed Melon Farm",         "minecraft:melon_slice",    "minecraft:pumpkin"),
    "cactus_farm":          ("盒装仙人掌机",   "Boxed Cactus Farm",        "minecraft:cactus",         "minecraft:green_dye"),
    "bamboo_farm":          ("盒装竹子机",     "Boxed Bamboo Farm",        "minecraft:bamboo",         "minecraft:paper"),
    "string_farm":          ("盒装刷线机",     "Boxed String Farm",        "minecraft:string",         "minecraft:white_wool"),
    "bone_farm":            ("盒装刷骨机",     "Boxed Bone Farm",          "minecraft:bone",           "minecraft:bone_meal"),
    "ender_pearl_farm":     ("盒装末影珍珠机", "Boxed Ender Pearl Farm",   "minecraft:ender_pearl",    "minecraft:chorus_fruit"),
    "xp_machine":           ("盒装经验机",     "Boxed XP Machine",         "minecraft:lapis_lazuli",   "minecraft:glowstone_dust"),
    "egg_farm":             ("盒装鸡蛋机",     "Boxed Egg Farm",           "minecraft:egg",            "minecraft:feather"),
    "wool_farm":            ("盒装羊毛机",     "Boxed Wool Farm",          "minecraft:white_wool",     "minecraft:string"),
    "beef_machine":         ("盒装烤牛肉机",   "Boxed Beef Machine",       "minecraft:beef",           "minecraft:leather"),
    "moss_farm":            ("盒装苔藓机",     "Boxed Moss Farm",          "minecraft:moss_block",     "minecraft:bone_meal"),
    "mushroom_farm":        ("盒装蘑菇机",     "Boxed Mushroom Farm",      "minecraft:brown_mushroom", "minecraft:red_mushroom"),
    "deepslate_machine":    ("盒装深板岩机",   "Boxed Deepslate Machine",  "minecraft:cobbled_deepslate", "minecraft:deepslate"),
    "quartz_farm":          ("盒装石英机",     "Boxed Quartz Farm",        "minecraft:quartz",         "minecraft:quartz_block"),
    "slime_farm":           ("盒装粘液机",     "Boxed Slime Farm",         "minecraft:slime_ball",     "minecraft:slime_block"),
    "redstone_machine":     ("盒装红石机",     "Boxed Redstone Machine",   "minecraft:redstone",       "minecraft:redstone_torch"),
}

ITEMS = {
    "mechanism_gear": ("机械齿轮", "Mechanism Gear"),
    "boxed_casing":   ("盒装机壳", "Boxed Casing"),
}


def write(path, data):
    full = os.path.join(RES, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("write", path)


def shaped(keys, pattern, result, count=1, group=None):
    recipe = {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "pattern": pattern,
        "key": keys,
        "result": {"id": f"{MOD}:{result}", "count": count},
    }
    if group:
        recipe["group"] = group
    return recipe


def main():
    # ---------- 合成配方 ----------
    # 第一层：机械齿轮（铁锭 + 红石）
    write(f"data/{MOD}/recipe/mechanism_gear.json", shaped(
        {"I": {"item": "minecraft:iron_ingot"}, "R": {"item": "minecraft:redstone"}},
        [" I ", "IRI", " I "],
        "mechanism_gear",
    ))
    # 第二层：盒装机壳（机械齿轮 + 铜锭 + 铁锭）
    write(f"data/{MOD}/recipe/boxed_casing.json", shaped(
        {"G": {"item": f"{MOD}:mechanism_gear"}, "C": {"item": "minecraft:copper_ingot"}, "I": {"item": "minecraft:iron_ingot"}},
        ["GCG", "CIC", "GCG"],
        "boxed_casing",
    ))
    # 第三层：各盒装机器（盒装机壳 + 主题材料）——套娃深度共 3 层
    for mid, (_, _, a, b) in MACHINES.items():
        write(f"data/{MOD}/recipe/{mid}.json", shaped(
            {"A": {"item": a}, "B": {"item": b}, "C": {"item": f"{MOD}:boxed_casing"}},
            ["ABA", "BCB", "ABA"],
            mid,
        ))

    # ---------- 战利品表 ----------
    for mid in MACHINES:
        write(f"data/{MOD}/loot_table/blocks/{mid}.json", {
            "type": "minecraft:block",
            "pools": [
                {
                    "bonus_rolls": 0.0,
                    "conditions": [{"condition": "minecraft:survives_explosion"}],
                    "entries": [{"type": "minecraft:item", "name": f"{MOD}:{mid}"}],
                    "rolls": 1.0,
                }
            ],
            "random_sequence": f"{MOD}:blocks/{mid}",
        })

    # ---------- 方块状态 / 方块模型 ----------
    for mid in MACHINES:
        write(f"assets/{MOD}/blockstates/{mid}.json", {
            "variants": {"": {"model": f"{MOD}:block/{mid}"}}
        })
        write(f"assets/{MOD}/models/block/{mid}.json", {
            "parent": "minecraft:block/cube_bottom_top",
            "textures": {
                "bottom": f"{MOD}:block/machine_bottom",
                "side": f"{MOD}:block/{mid}_side",
                "top": f"{MOD}:block/machine_top",
            },
        })

    # ---------- 客户端物品模型（1.21.9+ 新格式，items/ 目录） ----------
    for mid in MACHINES:
        write(f"assets/{MOD}/items/{mid}.json", {
            "model": {"type": "minecraft:model", "model": f"{MOD}:block/{mid}"}
        })
    for iid in ITEMS:
        write(f"assets/{MOD}/models/item/{iid}.json", {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{MOD}:item/{iid}"},
        })
        write(f"assets/{MOD}/items/{iid}.json", {
            "model": {"type": "minecraft:model", "model": f"{MOD}:item/{iid}"}
        })

    # ---------- 语言文件 ----------
    zh = {"itemGroup.boxedmachines": "盒装机器"}
    en = {"itemGroup.boxedmachines": "Boxed Machines"}
    for iid, (zh_n, en_n) in ITEMS.items():
        zh[f"item.{MOD}.{iid}"] = zh_n
        en[f"item.{MOD}.{iid}"] = en_n
    for mid, (zh_n, en_n, _, _) in MACHINES.items():
        zh[f"block.{MOD}.{mid}"] = zh_n
        en[f"block.{MOD}.{mid}"] = en_n
    write(f"assets/{MOD}/lang/zh_cn.json", zh)
    write(f"assets/{MOD}/lang/en_us.json", en)

    print(f"OK: {len(MACHINES)} machines, {len(ITEMS)} items generated.")


if __name__ == "__main__":
    main()
