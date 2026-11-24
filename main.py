"""News front page for Tuesday 24 November 2026.

Draws one 1024x1024 PNG that sums up the day's world news as a newspaper
front page: a masthead with the date, a dominant lead story, a second story,
three picture tiles and an "also today" strip. Pure standard library; the
picture is drawn procedurally by render.py, so the program needs no network,
no files besides its own code, and no fonts from disk. Running it twice
writes byte-identical output.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import Page, text_width  # noqa: E402

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (22, 22, 22)
RED = (178, 34, 30)
NAVY = (27, 58, 88)
SKY = (176, 214, 232)
SEA = (38, 84, 124)
DEEPSEA = (24, 58, 92)
GREEN = (46, 110, 58)
GOLD = (198, 138, 44)
ORANGE = (232, 110, 30)
FLAME = (244, 164, 40)
DARK = (30, 30, 34)
WHITE = (255, 255, 255)
GREY = (120, 120, 116)
CLOUD = (250, 250, 246)


def draw_korea_scene(p, x, y, w, h):
    """Ulleung island, the sea, and two Russian jets in a pale morning sky."""
    p.rect(x, y, w, h, SKY)
    p.circle(x + w - 42, y + 30, 18, GOLD)
    p.rect(x + 18, y + 26, 74, 12, CLOUD)
    p.rect(x + 120, y + 52, 60, 10, CLOUD)
    p.rect(x + 210, y + 18, 66, 10, CLOUD)
    sea_y = y + h - 58
    p.rect(x, sea_y, w, 58, SEA)
    p.hline(x, sea_y, w, WHITE, 2)
    for wy in (sea_y + 16, sea_y + 34):
        p.hline(x + 12, wy, w - 90, (120, 180, 210), 2)
        p.hline(x + 70, wy + 8, w - 140, (120, 180, 210), 2)
    # The island: a steep green hill rising out of the sea.
    p.poly([(x + 96, sea_y + 58), (x + 150, sea_y - 34),
            (x + 236, sea_y - 6), (x + 268, sea_y + 58)], (52, 96, 62))
    p.poly([(x + 150, sea_y - 34), (x + 168, sea_y - 8),
            (x + 132, sea_y - 8)], (74, 122, 78))
    # Lighthouse on the hill.
    p.rect(x + 176, sea_y - 26, 10, 26, WHITE)
    p.rect(x + 174, sea_y - 32, 14, 6, RED)
    # Two jets crossing the sky, with contrails.
    for jx, jy in ((x + 40, y + 78), (x + 96, y + 58)):
        p.line(jx - 46, jy + 10, jx - 8, jy + 2, WHITE, 2)
        p.poly([(jx, jy), (jx + 34, jy + 6), (jx, jy + 12)], (60, 60, 64))
        p.poly([(jx + 8, jy), (jx + 20, jy - 12), (jx + 26, jy)], (60, 60, 64))
        p.poly([(jx + 8, jy + 12), (jx + 20, jy + 22), (jx + 26, jy + 12)],
               (60, 60, 64))
    p.frame(x, y, w, h, INK, 2)


def draw_tanker_scene(p, x, y, w, h):
    """A tanker burning in the Strait of Hormuz at dusk."""
    for i, band in enumerate(((232, 150, 80), (226, 120, 62),
                             (214, 96, 52), (190, 76, 52))):
        p.rect(x, y + i * (h // 4), w, h // 4 + 1, band)
    p.circle(x + w - 40, y + 26, 16, (250, 220, 140))
    sea_y = y + h - 56
    p.rect(x, sea_y, w, 56, DEEPSEA)
    p.hline(x, sea_y, w, (90, 140, 180), 2)
    # The tanker: long dark hull, red waterline, white bridge tower.
    hull_y = sea_y - 26
    p.rect(x + 14, hull_y, w - 28, 26, (28, 28, 30))
    p.rect(x + 14, hull_y + 20, w - 28, 6, RED)
    p.rect(x + w - 78, hull_y - 34, 34, 34, WHITE)
    p.rect(x + w - 78, hull_y - 40, 34, 6, RED)
    for wy in (hull_y - 28, hull_y - 18):
        p.rect(x + w - 72, wy, 22, 3, NAVY)
    # Flames licking up from the mid-deck.
    fx = x + w // 2 - 30
    for dx, fh, col in ((-28, 44, ORANGE), (-8, 62, FLAME),
                        (12, 50, ORANGE), (30, 38, FLAME)):
        p.triangle(fx + dx, hull_y, fx + dx + 12, hull_y - fh,
                   fx + dx + 24, hull_y, col)
    # Smoke drifting up and away.
    for sx, sy, r in ((x + 70, y + 52, 14), (x + 92, y + 34, 18),
                      (x + 120, y + 22, 12)):
        p.circle(sx, sy, r, (90, 88, 84))
    # A naval mine, spiked and half-submerged, in the foreground water.
    mx, my = x + 44, sea_y + 32
    p.circle(mx, my, 9, (16, 16, 18))
    for dx, dy in ((-12, 0), (12, 0), (0, -12), (-9, -9), (9, -9)):
        p.line(mx, my, mx + dx, my + dy, (16, 16, 18), 2)
    p.frame(x, y, w, h, INK, 2)


def draw_awacs_scene(p, x, y, w, h):
    """A NATO AWACS radar plane over a pale sky."""
    p.rect(x, y, w, h, SKY)
    p.rect(x + 14, y + 14, 60, 9, CLOUD)
    p.rect(x + w - 90, y + 30, 66, 9, CLOUD)
    p.rect(x + 40, y + 58, 54, 8, CLOUD)
    cx, cy = x + w // 2, y + h // 2 + 10
    # Radar dome on its stalk, fuselage, nose, tail and wings.
    p.rect(cx - 6, cy - 26, 12, 14, GREY)
    p.circle(cx, cy - 30, 18, (225, 225, 220))
    p.rect(cx - 108, cy - 8, 216, 16, (228, 228, 224))
    p.poly([(cx + 108, cy - 8), (cx + 128, cy), (cx + 108, cy + 8)],
           (228, 228, 224))
    p.poly([(cx - 108, cy - 8), (cx - 128, cy - 26), (cx - 112, cy - 8)],
           (200, 200, 196))
    p.poly([(cx - 20, cy + 8), (cx + 6, cy + 34), (cx + 26, cy + 8)],
           (200, 200, 196))
    p.poly([(cx - 30, cy - 8), (cx - 6, cy - 34), (cx + 6, cy - 8)],
           (200, 200, 196))
    for wx in (cx - 84, cx - 52, cx + 44, cx + 76):
        p.rect(wx, cy - 2, 12, 5, NAVY)
    p.frame(x, y, w, h, INK, 2)


def draw_nvidia_scene(p, x, y, w, h):
    """A chip on dark green, with a steep green arrow and +31%."""
    p.rect(x, y, w, h, (16, 42, 28))
    cx, cy = x + 74, y + h // 2 + 4
    for side in range(4):
        for i in range(3):
            if side == 0:
                p.rect(cx - 38 + i * 26, cy - 48, 10, 10, GOLD)
            elif side == 1:
                p.rect(cx - 38 + i * 26, cy + 38, 10, 10, GOLD)
            elif side == 2:
                p.rect(cx - 48, cy - 26 + i * 26, 10, 10, GOLD)
            else:
                p.rect(cx + 38, cy - 26 + i * 26, 10, 10, GOLD)
    p.rect(cx - 36, cy - 36, 72, 72, (24, 64, 40))
    p.frame(cx - 36, cy - 36, 72, 72, GOLD, 3)
    p.rect(cx - 20, cy - 20, 40, 40, (16, 42, 28))
    p.frame(cx - 20, cy - 20, 40, 40, GOLD, 2)
    p.text(cx - 14, cy - 7, "AI", 2, GOLD)
    # The market's verdict: a steep climbing arrow, clear of the +31% label.
    ax, ay = x + 170, y + h - 14
    p.line(ax, ay, ax + 45, ay - 28, (64, 200, 110), 5)
    p.poly([(ax + 45, ay - 28), (ax + 28, ay - 26), (ax + 45, ay - 42)],
           (64, 200, 110))
    p.text(x + 222, y + 8, "+31%", 3, (64, 200, 110))
    p.frame(x, y, w, h, INK, 2)


def draw_libya_scene(p, x, y, w, h):
    """A corvette at Benghazi, hit by a sea drone: burst and smoke."""
    p.rect(x, y, w, h, SKY)
    p.rect(x + 16, y + 12, 64, 9, CLOUD)
    p.rect(x + w - 96, y + 22, 70, 9, CLOUD)
    sea_y = y + h - 30
    p.rect(x, sea_y, w, 30, SEA)
    p.hline(x, sea_y, w, WHITE, 2)
    for wy in (sea_y + 12, sea_y + 22):
        p.hline(x + 16, wy, w - 60, (120, 180, 210), 2)
    # The corvette, low in the water.
    hull_y = sea_y - 14
    p.rect(x + 52, hull_y, 190, 14, (90, 92, 96))
    p.rect(x + 52, hull_y + 9, 190, 5, (40, 40, 44))
    p.poly([(x + 242, hull_y), (x + 266, hull_y + 6), (x + 242, hull_y + 14)],
           (90, 92, 96))
    p.rect(x + 130, hull_y - 18, 44, 18, (120, 122, 126))
    p.rect(x + 146, hull_y - 28, 6, 10, (120, 122, 126))
    p.rect(x + 88, hull_y - 10, 20, 10, (120, 122, 126))
    # Explosion burst above the bow, smoke above it, all inside the frame.
    bx, by = x + 232, hull_y - 8
    for dx, dy in ((-16, -4), (-11, -14), (0, -17), (11, -13), (16, -3),
                   (-8, 4), (8, 4)):
        p.triangle(bx, by, bx + dx, by + dy, bx + dx + 6, by + dy + 3, FLAME)
    p.circle(bx, by - 2, 9, ORANGE)
    p.circle(bx - 20, by - 12, 8, (90, 88, 84))
    p.circle(bx + 8, by - 18, 10, (110, 108, 104))
    # The sea drone: a small dark hull racing in, white wake behind it.
    dx0, dy0 = x + 30, sea_y + 12
    p.line(x + 6, dy0 + 6, dx0 - 4, dy0, WHITE, 2)
    p.line(x + 10, dy0 + 10, dx0 - 2, dy0 + 4, WHITE, 2)
    p.rect(dx0, dy0, 26, 8, (20, 20, 22))
    p.rect(dx0 + 8, dy0 - 5, 8, 5, (20, 20, 22))
    p.frame(x, y, w, h, INK, 2)


def tile(p, x, y, w, h, scene, kicker, headline, body):
    p.frame(x, y, w, h, INK, 2)
    scene(p, x + 6, y + 6, w - 12, 84)
    ty = y + 96
    p.text(x + 10, ty, kicker, 2, RED)
    ty = p.headline(x + 10, ty + 20, headline, 2, INK, w - 20)
    p.paragraph(x + 10, ty + 4, body, 2, INK, w - 20)


def build():
    p = Page(W, H, PAPER)
    # Outer double border.
    p.frame(6, 6, W - 12, H - 12, INK, 3)
    p.frame(12, 12, W - 24, H - 24, INK, 1)

    # ---- top bar ----
    p.rect(16, 16, W - 32, 26, INK)
    p.text(26, 22, "TUESDAY 24 NOVEMBER 2026", 2, WHITE)
    right = "WORLD NEWS IN ONE IMAGE"
    p.text(W - 26 - text_width(right, 2), 22, right, 2, WHITE)

    # ---- masthead ----
    p.text_centered(W // 2, 56, "THE WORLD TODAY", 7, INK)
    p.text_centered(W // 2, 122, "THE DAY'S WORLD NEWS, IN ONE PAGE", 2, INK)
    p.hline(28, 146, W - 56, INK, 3)
    p.hline(28, 152, W - 56, INK, 1)

    # ---- lead story: Korea ----
    p.text(28, 166, "LEAD STORY  •  ASIA  •  SEOUL", 2, RED)
    y = p.headline(28, 192, "KOREA SOUNDS AIR ALERT AS RUSSIAN JETS NEAR ISLAND",
                   4, INK, 612)
    draw_korea_scene(p, 668, 164, 328, 176)
    # Alert box under the lead picture.
    p.rect(668, 348, 328, 100, RED)
    p.text(682, 360, "AIR-RAID WARNING", 2, WHITE)
    p.text(682, 382, "ULLEUNG ISLAND", 2, WHITE)
    p.text(682, 404, "07:52 KST", 2, WHITE)
    p.text(682, 426, "LIFTED IN MINUTES", 2, WHITE)
    body = ("SEOUL - SOUTH KOREA BRIEFLY ORDERED PEOPLE ON ULLEUNG ISLAND "
            "TO TAKE SHELTER ON TUESDAY AFTER RUSSIAN MILITARY AIRCRAFT "
            "NEARED THE EAST COAST. FIGHTER JETS SCRAMBLED TO MEET THEM. "
            "THE WARNING WAS LIFTED WITHIN MINUTES, AND SEOUL SAID ITS "
            "AIRSPACE WAS NOT ENTERED.")
    y = p.paragraph(28, 296, body, 2, INK, 612)
    p.hline(28, 462, W - 56, INK, 3)
    p.hline(28, 468, W - 56, INK, 1)

    # ---- second story: Hormuz tankers ----
    draw_tanker_scene(p, 28, 482, 302, 168)
    p.text(350, 484, "MIDDLE EAST  •  THE GULF", 2, RED)
    y = p.headline(350, 510, "THREE TANKERS ABLAZE IN HORMUZ AFTER MINE BLASTS",
                   3, INK, 646)
    p.paragraph(350, 576,
                "IRAN'S REVOLUTIONARY GUARD SAID THREE OIL TANKERS HIT "
                "NAVAL MINES IN THE STRAIT OF HORMUZ AND CAUGHT FIRE. THE "
                "WATERWAY CARRIES ABOUT A FIFTH OF THE WORLD'S OIL AND GAS.",
                2, INK, 646)
    p.hline(28, 664, W - 56, INK, 3)
    p.hline(28, 670, W - 56, INK, 1)

    # ---- three picture tiles ----
    tile(p, 28, 680, 312, 212, draw_awacs_scene, "EUROPE",
         "NATO SENDS AWACS TO POLAND",
         "AFTER RUSSIAN MISSILES LANDED IN POLAND, NATO DEPLOYS ITS "
         "RADAR PLANE.")
    tile(p, 356, 680, 312, 212, draw_nvidia_scene, "BUSINESS",
         "HUANG IS BACK AT NVIDIA",
         "SHARES JUMP 31% AS HUANG RETURNS AS CHIEF, 11 DAYS AFTER "
         "QUITTING.")
    tile(p, 684, 680, 312, 212, draw_libya_scene, "WAR AT SEA",
         "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         "KYIV SAYS SEA DRONES SANK THE CORVETTE MERKURY AT BENGHAZI.")

    # ---- also today ----
    p.hline(28, 902, W - 56, INK, 3)
    p.text(28, 910, "ALSO TODAY", 2, RED)
    p.paragraph(28, 932,
                "COP31 FALLOUT: ERDOGAN SAYS THE FAILED CLIMATE TALKS LAID "
                "GROUNDWORK FOR MORE  •  MEXICO CAPTURES CARTEL BOSS "
                "'CHAPO ISIDRO' AFTER A BLOODY RAID  •  ISRAELI STRIKES "
                "KILL THREE IN GAZA",
                2, INK, W - 56)

    # ---- footer: sources ----
    p.hline(28, 990, W - 56, INK, 1)
    p.text_centered(W // 2, 996,
                    "SOURCES: REUTERS - AP - CNN - BBC", 2, INK)
    return p


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    page = build()
    data = page.png_bytes()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
