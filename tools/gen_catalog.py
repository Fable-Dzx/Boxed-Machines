#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盒装机器图鉴生成器：输出自包含 catalog.html（合成链 + 机器一览 + 使用说明）
数据与 Java 注册（ModBlocks.java）逐项一致。
"""
import base64
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
TEX = os.path.join(ROOT, "src/main/resources/assets/boxedmachines/textures/block")

# id: (中文名, 英文名, 产出描述, 间隔tick, 配方主料, 配方辅料, 类别, 类别色)
M = {
    "iron_farm":            ("盒装刷铁机", "铁锭×1-2、铁粒×2-4", 600, "铁锭", "铁栏杆", "金属矿物", "#d8b45a"),
    "gold_farm":            ("盒装刷金机", "金粒×2-4、金锭×1", 600, "金锭", "金粒", "金属矿物", "#d8b45a"),
    "quartz_farm":          ("盒装石英机", "下界石英×1-2、石英块×1", 600, "下界石英", "石英块", "金属矿物", "#d8b45a"),
    "deepslate_machine":    ("盒装深板岩机", "深板岩×1-2、深板岩圆石×1", 200, "深板岩圆石", "深板岩", "金属矿物", "#d8b45a"),
    "redstone_machine":     ("盒装红石机", "红石粉×2-4、红石火把×1", 400, "红石粉", "红石火把", "金属矿物", "#d8b45a"),
    "lava_machine":         ("盒装岩浆机", "岩浆桶×1", 1200, "岩浆膏", "黑曜石", "熔岩烹饪", "#e8761f"),
    "lava_chicken_machine": ("盒装岩浆烤鸡机", "熟鸡肉×1-2、羽毛×1-2", 400, "生鸡肉", "岩浆膏", "熔岩烹饪", "#e8761f"),
    "beef_machine":         ("盒装烤牛肉机", "熟牛排×1、皮革×1", 400, "生牛肉", "皮革", "熔岩烹饪", "#e8761f"),
    "sugarcane_farm":       ("盒装甘蔗机", "甘蔗×1-2、糖×1", 600, "甘蔗", "糖", "农业植物", "#58a043"),
    "melon_farm":           ("盒装瓜机", "西瓜片×2-4、南瓜×1、南瓜种子×1-2", 600, "西瓜片", "南瓜", "农业植物", "#58a043"),
    "cactus_farm":          ("盒装仙人掌机", "仙人掌×1-2、绿色染料×1", 600, "仙人掌", "绿色染料", "农业植物", "#58a043"),
    "bamboo_farm":          ("盒装竹子机", "竹子×1-2、纸×1", 600, "竹子", "纸", "农业植物", "#58a043"),
    "moss_farm":            ("盒装苔藓机", "苔藓块×1、覆地苔藓×1-2、骨粉×1", 600, "苔藓块", "骨粉", "农业植物", "#58a043"),
    "mushroom_farm":        ("盒装蘑菇机", "棕蘑菇×1-2、红蘑菇×1-2、蘑菇煲×1", 600, "棕蘑菇", "红蘑菇", "农业植物", "#58a043"),
    "fishing_machine":      ("盒装自动钓鱼机", "生鳕鱼/生鲑鱼/河豚/热带鱼、骨头、线、附魔书", 900, "钓鱼竿", "线", "生物农场", "#5b4a78"),
    "mob_farm":             ("盒装刷怪机", "火药×1-2、骨头、腐肉×1-2、线×1-2、蜘蛛眼", 600, "腐肉", "骨头", "生物农场", "#5b4a78"),
    "honey_farm":           ("盒装刷蜜机", "蜂蜜瓶×1、蜜脾×1-2", 600, "蜂蜜瓶", "蜜脾", "生物农场", "#5b4a78"),
    "string_farm":          ("盒装刷线机", "线×1-3、白羊毛×1", 600, "线", "白羊毛", "生物农场", "#5b4a78"),
    "bone_farm":            ("盒装刷骨机", "骨头×1-2、骨粉×2-3", 600, "骨头", "骨粉", "生物农场", "#5b4a78"),
    "egg_farm":             ("盒装鸡蛋机", "鸡蛋×1-2、羽毛×1", 300, "鸡蛋", "羽毛", "生物农场", "#5b4a78"),
    "wool_farm":            ("盒装羊毛机", "白羊毛×1-2、线×1", 600, "白羊毛", "线", "生物农场", "#5b4a78"),
    "slime_farm":           ("盒装粘液机", "粘液球×1", 600, "粘液球", "粘液块", "生物农场", "#5b4a78"),
    "ender_pearl_farm":     ("盒装末影珍珠机", "末影珍珠×1、紫颂果×1", 900, "末影珍珠", "紫颂果", "特殊高级", "#1d6a63"),
    "xp_machine":           ("盒装经验机", "附魔之瓶×1", 300, "青金石", "萤石粉", "特殊高级", "#1d6a63"),
    "cobblestone_machine":  ("盒装刷石机", "圆石×1-2、石头×1", 100, "圆石", "石头", "特殊高级", "#1d6a63"),
}

CATS = ["金属矿物", "熔岩烹饪", "农业植物", "生物农场", "特殊高级"]


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def img_tag(mid, size=48):
    p = os.path.join(TEX, f"{mid}_side.png")
    if not os.path.exists(p):
        return ""
    return f'<img src="data:image/png;base64,{b64(p)}" width="{size}" height="{size}" alt="{mid}" style="image-rendering:pixelated;">'


def main():
    sections = []
    for cat in CATS:
        items = [(mid, v) for mid, v in M.items() if v[5] == cat]
        rows = "\n".join(
            f'''<div class="card"><div class="icon">{img_tag(mid, 44)}</div>
              <div class="name">{v[0]}</div><div class="out">{v[1]}</div>
              <div class="meta"><span class="t">每 {v[2] // 20}s</span><span class="r">{v[3]} + {v[4]}</span></div></div>'''
            for mid, v in items
        )
        sections.append(f'<h3 class="cat" style="border-left:6px solid {items[0][1][6]}">{cat} · {len(items)} 台</h3><div class="grid">{rows}</div>')

    chain_imgs = {
        "iron": '<img src="data:image/png;base64,{}" width="36" height="36" style="image-rendering:pixelated;">',
    }

    html = f"""<html style="margin:0;padding:0;">
<title>盒装机器图鉴 · Boxed Machines</title>
<style>
  body{{margin:0;padding:20px;background:#1a1d21;color:#e8e8e8;font-family:'PingFang SC','Microsoft YaHei',sans-serif;}}
  h1{{font-size:26px;margin:4px 0 6px;color:#ffd76a;}}
  .sub{{color:#9aa3ad;font-size:14px;margin-bottom:18px;}}
  h2{{font-size:19px;margin:26px 0 10px;color:#8ab4f8;border-bottom:1px solid #333;padding-bottom:6px;}}
  h3.cat{{font-size:15px;margin:20px 0 10px;padding-left:10px;color:#c9d1d9;}}
  .grid{{display:flex;flex-wrap:wrap;gap:10px;}}
  .card{{width:172px;background:#23272d;border:1px solid #343a41;border-radius:8px;padding:10px;box-sizing:border-box;}}
  .card .icon{{text-align:center;background:#181b1f;border-radius:6px;padding:6px 0;}}
  .card .name{{font-weight:600;font-size:14px;margin:8px 0 4px;}}
  .card .out{{font-size:12px;color:#9aa3ad;min-height:32px;}}
  .card .meta{{font-size:11px;color:#6b7682;border-top:1px dashed #343a41;margin-top:6px;padding-top:6px;}}
  .card .t{{color:#7fd37f;}}
  .chain{{background:#23272d;border:1px solid #343a41;border-radius:10px;padding:18px;overflow-x:auto;}}
  .chain table{{border-collapse:collapse;width:100%;}}
  .chain td{{text-align:center;padding:8px 6px;font-size:12px;vertical-align:top;}}
  .step{{display:inline-block;background:#181b1f;border:1px solid #4a5560;border-radius:8px;padding:8px 12px;min-width:96px;}}
  .step b{{display:block;font-size:13px;color:#ffd76a;margin-top:4px;}}
  .step .mat{{color:#9aa3ad;font-size:11px;}}
  .arrow{{font-size:22px;color:#ffd76a;}}
  .tip{{background:#2a2416;border:1px solid #5a4a20;border-radius:8px;padding:12px 16px;font-size:13px;color:#d8c9a0;line-height:1.8;}}
  .note{{font-size:12px;color:#6b7682;margin-top:10px;}}
</style>
<h1>🧰 盒装机器图鉴</h1>
<div class="sub">Boxed Machines · Fabric 1.21.11 · 25 台生电机器 · 自动产出 · 右键收取</div>

<h2>套娃合成链（共 3 层）</h2>
<div class="chain">
<table>
<tr>
  <td><div class="step"><span style="font-size:22px">🧱</span><b>基础材料</b><span class="mat">铁锭 / 红石 / 铜锭</span></div></td>
  <td class="arrow">→</td>
  <td><div class="step"><img src="data:image/png;base64,{b64(os.path.join(ROOT,'src/main/resources/assets/boxedmachines/textures/item/mechanism_gear.png'))}" width="36" height="36" style="image-rendering:pixelated;"><b>机械齿轮</b><span class="mat">铁锭×4 + 红石</span></div></td>
  <td class="arrow">→</td>
  <td><div class="step"><img src="data:image/png;base64,{b64(os.path.join(ROOT,'src/main/resources/assets/boxedmachines/textures/item/boxed_casing.png'))}" width="36" height="36" style="image-rendering:pixelated;"><b>盒装机壳</b><span class="mat">齿轮×4 + 铜锭×4 + 铁锭</span></div></td>
  <td class="arrow">→</td>
  <td><div class="step" style="min-width:120px"><span style="font-size:22px">📦</span><b>盒装机器 ×25</b><span class="mat">机壳 + 主题材料×8</span></div></td>
</tr>
</table>
</div>

<h2>机器一览</h2>
{''.join(sections)}

<h2>使用方法</h2>
<div class="tip">
① 放置机器后立即开始工作，按设定间隔自动把产出放入机器内部。<br>
② <b>右键</b>机器一键收取全部产出（背包满时物品掉落在身边）；内部最多囤 6 组。<br>
③ 机器后侧可接<b>红石比较器</b>读取储量（1–15 信号强度）。<br>
④ 用任意镐/徒手均可拆下（不会损坏，拆下时内部物品会掉落）。<br>
⑤ 全部机器在创造模式物品栏「<b>盒装机器</b>」分组；生存也可按合成链合成。
</div>
<div class="note">模组 id：boxedmachines · 需要 Fabric Loader ≥ 0.19.5 与 Fabric API · 贴图为 16×16 像素程序生成</div>
</html>
"""
    out = os.path.join(ROOT, "catalog.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("written", out, len(html), "bytes")


if __name__ == "__main__":
    main()
