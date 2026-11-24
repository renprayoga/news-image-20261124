# The World Today — Tuesday 24 November 2026

[![Bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/renprayoga/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/renprayoga/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image that sums up the world's news of **Tuesday 24 November 2026**,
drawn as a newspaper front page: a masthead with the date, a dominant lead
story, a second story, three picture tiles, and an "also today" strip.

## The day in the picture

- **Lead — Korea sounds air alert:** South Korea briefly ordered people on
  Ulleung Island to take shelter after Russian military aircraft neared the
  east coast; fighter jets scrambled, and the warning was lifted within
  minutes.
- **Three tankers ablaze in Hormuz:** Iran's Revolutionary Guard said three
  oil tankers hit naval mines in the Strait of Hormuz and caught fire.
- **NATO sends AWACS to Poland** after Russian missiles landed in Poland.
- **Huang is back at Nvidia:** shares jump 31% as Jensen Huang returns as
  chief, 11 days after quitting.
- **Ukraine sinks a Russian warship off Libya:** Kyiv says sea drones sank
  the corvette Merkury at Benghazi.
- **Also today:** COP31 fallout, Mexico captures cartel boss "Chapo Isidro",
  Israeli strikes kill three in Gaza.

Sources: Reuters, AP, CNN, BBC. See `BUILD_LOG.md` for the full story list
with sources, the strategy, and how the image is drawn.

## How it runs

`main.py` (Python 3.13, standard library only) draws the page procedurally
with `render.py` — a tiny raster engine with a hand-built 5x7 pixel font and
a hand-written PNG encoder — and writes `entry.png` (1024x1024, well under
1 MiB) to `$MAKEFUN_OUTPUT_DIR` (default `/output`). No network, no fonts
from disk, no timestamps in the output: two runs write byte-identical files.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
