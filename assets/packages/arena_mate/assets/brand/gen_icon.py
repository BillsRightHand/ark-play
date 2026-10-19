# ⚠️ 2026-08-30 起這支腳本**不再是圖示的來源**。
# DOJO 的圖示改用品牌素材包：
#   /Users/ciro/Downloads/ChefsMate POS Logo设计.zip → assets/dojo/
#   （app-icon-ios-1024.svg / android-foreground.svg / lockup-horizontal.svg）
# 換設計＝拿新的 SVG 用 qlmanage 重算三個母檔，再 dart run flutter_launcher_icons。
# ⚠️ SVG 轉點陣一律用 qlmanage(WebKit)：ImageMagick 畫不出挖空字母那條 arc stroke。
# 名冊與規則見 memory app-brand-registry。這支保留只為了歷史對照，不要再跑。

# ArenaMate App icon 產生器(v1,2026-07-18 上架衝刺 P1-2)
# 設計語言:App 現行 token — 深底 #0C0D0F、土耳其藍 #35D6C4、金 #E6B980。
# 產出:
#   arena_icon_1024.png      — 商店/iOS 用滿版 icon(不透明)
#   arena_icon_fg_1024.png   — Android adaptive foreground(透明底,標誌縮在安全區)
#   arena_launch_logo.png    — 啟動畫面 logo(透明底 512)
# 重跑:python3 gen_icon.py(老闆想換設計改這支再跑 flutter_launcher_icons 即可)
from PIL import Image, ImageDraw

BG = (12, 13, 15, 255)        # 0C0D0F
ACC = (53, 214, 196, 255)     # 35D6C4
GOLD = (230, 185, 128, 255)   # E6B980
S = 1024


def stroke(d, p1, p2, w, color):
    """圓頭粗線(PIL line 無 round cap,自己補端點圓)。"""
    d.line([p1, p2], fill=color, width=w)
    r = w / 2
    for p in (p1, p2):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


def draw_mark(size, scale=1.0, with_glow=False, bg=None):
    """A 字標(雙腿+橫槓)+ 右上金球。以 1024 座標系設計,依 scale 縮放置中。"""
    img = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))

    if with_glow:  # 標誌後方柔和藍綠光暈,深色桌布上不死黑
        glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        cx, cy, rmax = size * 0.50, size * 0.44, size * 0.52
        steps = 160
        for i in range(steps, 0, -1):
            r = rmax * i / steps
            a = int(26 * (1 - i / steps) ** 2)
            gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(53, 214, 196, a))
        img = Image.alpha_composite(img, glow)

    d = ImageDraw.Draw(img)

    def pt(x, y):
        # 1024 設計座標 → 目標尺寸,繞中心縮放
        return ((x - 512) * scale * size / 1024 + size / 2,
                (y - 512) * scale * size / 1024 + size / 2)

    w = int(104 * scale * size / 1024)
    apex = pt(512, 232)
    stroke(d, apex, pt(308, 792), w, ACC)          # 左腿
    stroke(d, apex, pt(716, 792), w, ACC)          # 右腿
    stroke(d, pt(398, 606), pt(626, 606), int(w * 0.82), ACC)  # 橫槓(球網線)
    br = int(56 * scale * size / 1024)             # 金球(發球位,右上)
    bx, by = pt(766, 300)
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=GOLD)
    return img


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))

    # 1) 滿版 icon(iOS 需不透明、無圓角——系統自己遮罩)
    icon = draw_mark(S, scale=0.92, with_glow=True, bg=BG).convert("RGB")
    icon.save(os.path.join(here, "arena_icon_1024.png"))

    # 2) Android adaptive foreground:內容要落在中央約 62% 安全區
    fg = draw_mark(S, scale=0.55)
    fg.save(os.path.join(here, "arena_icon_fg_1024.png"))

    # 3) 啟動畫面 logo(透明底)
    logo = draw_mark(512, scale=0.9)
    logo.save(os.path.join(here, "arena_launch_logo.png"))
    print("done: arena_icon_1024 / arena_icon_fg_1024 / arena_launch_logo")
