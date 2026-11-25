"""Tiny deterministic raster engine for the news front page.

Pure Python 3 standard library: draws into an RGB byte buffer and encodes
a PNG by hand (zlib + struct + binascii). No fonts on disk, no network, no
timestamps anywhere in the output, so two runs are byte-identical.
"""

import struct
import zlib

# ---------------------------------------------------------------- font ----
# A 5x7 pixel font, drawn from scratch for this page. Each glyph is seven
# rows of five cells; '#' is an inked cell. Only capitals are needed: the
# whole page is set in newspaper capitals.
_GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}

# Em dash and bullet are rendered from the hyphen / dot shapes at draw time.
_GLYPHS["\u2014"] = ("00000", "00000", "00000", "11111", "00000", "00000", "00000")
_GLYPHS["\u2022"] = ("00000", "00000", "01100", "01100", "01100", "00000", "00000")

CHAR_W = 5
CHAR_H = 7


def glyph_width(scale, gap=1):
    """Advance width of one character cell at a given scale."""
    return (CHAR_W + gap) * scale


def text_width(text, scale, gap=1):
    return len(text) * glyph_width(scale, gap) - gap * scale


def wrap_text(text, scale, max_width, gap=1):
    """Greedy word wrap. Returns a list of lines that fit max_width."""
    cell = glyph_width(scale, gap)
    per_line = max(1, (max_width + gap * scale) // cell)
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if len(trial) <= per_line:
                current = trial
            else:
                if current:
                    lines.append(current)
                # A single over-long word is hard-split.
                while len(word) > per_line:
                    lines.append(word[:per_line])
                    word = word[per_line:]
                current = word
        if current:
            lines.append(current)
    return lines


# -------------------------------------------------------------- canvas ----
class Page:
    """An RGB canvas with newspaper-drawing primitives."""

    def __init__(self, width, height, paper):
        self.width = width
        self.height = height
        self.buf = bytearray(paper) * (width * height)

    def _offset(self, x, y):
        return (y * self.width + x) * 3

    def px(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            off = self._offset(x, y)
            self.buf[off:off + 3] = color

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            off = self._offset(x0, yy)
            self.buf[off:off + len(row)] = row

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        """Bresenham line with square brush."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        half = thick // 2
        while True:
            self.rect(x0 - half, y0 - half, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            half = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
            self.rect(cx - half, yy, half * 2 + 1, 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if r - thick < d <= r:
                    self.px(xx, yy, color)

    def triangle(self, ax, ay, bx, by, cx, cy, color):
        """Filled triangle via scanline fill."""
        pts = sorted([(ax, ay), (bx, by), (cx, cy)], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        if y0 == y2:
            return
        for y in range(y0, y2 + 1):
            xs = []
            for (px, py), (qx, qy) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x0, y0), (x2, y2))):
                if py == qy:
                    continue
                if min(py, qy) <= y <= max(py, qy):
                    t = (y - py) / (qy - py)
                    xs.append(px + t * (qx - px))
            if len(xs) >= 2:
                xa, xb = int(min(xs)), int(max(xs))
                self.rect(xa, y, xb - xa + 1, 1, color)

    def poly(self, points, color):
        """Filled polygon (convex or simple) via scanline fill."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                (px, py), (qx, qy) = points[i], points[(i + 1) % n]
                if py == qy:
                    continue
                if min(py, qy) <= y < max(py, qy) or (y == max(ys) and y == max(py, qy)):
                    t = (y - py) / (qy - py)
                    xs.append(px + t * (qx - px))
            if len(xs) >= 2:
                xs.sort()
                for i in range(0, len(xs) - 1, 2):
                    xa, xb = int(xs[i]), int(xs[i + 1])
                    self.rect(xa, y, xb - xa + 1, 1, color)

    def frame(self, x, y, w, h, color, thick=2):
        self.hline(x, y, w, color, thick)
        self.hline(x, y + h - thick, w, color, thick)
        self.vline(x, y, h, color, thick)
        self.vline(x + w - thick, y, h, color, thick)

    # ------------------------------------------------------------ text ----
    def glyph(self, x, y, char, scale, color):
        rows = _GLYPHS.get(char.upper(), _GLYPHS["?"])
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                if cell == "1":
                    self.rect(x + c * scale, y + r * scale, scale, scale, color)

    def text(self, x, y, string, scale, color, gap=1):
        cx = x
        for ch in string:
            self.glyph(cx, y, ch, scale, color)
            cx += glyph_width(scale, gap)
        return cx

    def text_centered(self, cx, y, string, scale, color, gap=1):
        w = text_width(string, scale, gap)
        return self.text(cx - w // 2, y, string, scale, color, gap)

    def paragraph(self, x, y, string, scale, color, max_width, leading=None):
        """Draw wrapped text; returns the y just below the last line."""
        gap = 1
        line_h = CHAR_H * scale + (leading if leading is not None else scale + 2)
        for line in wrap_text(string, scale, max_width, gap):
            self.text(x, y, line, scale, color, gap)
            y += line_h
        return y

    def headline(self, x, y, string, scale, color, max_width, leading=None):
        """Wrapped headline; returns y below the last line."""
        return self.paragraph(x, y, string, scale, color, max_width, leading)

    # ------------------------------------------------------------- png ----
    def png_bytes(self):
        raw = bytearray()
        stride = self.width * 3
        for y in range(self.height):
            raw.append(0)  # filter: none
            start = y * stride
            raw += self.buf[start:start + stride]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(kind, data):
            out = struct.pack(">I", len(data)) + kind + data
            out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", comp)
                + chunk(b"IEND", b""))
