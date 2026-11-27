# The World Today — 27 November 2026

[![news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/c/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/freezzard/news27-entry1/rank.svg)](https://make.fun/c/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/freezzard/news27-entry1/reward.svg)](https://make.fun/c/news-image-20261127)

One image that sums up the world's news of Friday 27 November 2026:
a dense broadsheet digest — 3 hero stories, a pinned world map with region
and subject tallies, 12 illustrated cards, a day-in-numbers strip, and 24
numbered briefs. 39 stories in all, across 7 regions.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The program copies `entry.png` to `/output/entry.png` (or
`$MAKEFUN_OUTPUT_DIR/entry.png`) after verifying it byte by byte: PNG
signature, 1024x1024 IHDR, 8-bit RGB/RGBA, every chunk CRC, an IDAT chunk,
and the 1 MiB cap. It runs twice with identical bytes and uses no network.

`build_paint.py` is the painter that drew `entry.png` (Pillow, deterministic).
It is kept in the repository so the image can be rebuilt and inspected.

## The day in the image

- **Heroes:** the Houthi strike on Saudi Arabia's Jazan refinery, Brent
  crude past $96 · the FCC clears SpaceX's plan for a million orbital
  AI data-centre satellites · Hong Kong marks a year since the tower
  fire that killed 168.
- **Cards:** Russian drone strikes on Ukraine, Ukraine's Neptune missile
  hit on a Su-34 base, 10 killed in Gaza strikes, Iran's denial over
  Kuwait, Kim Jong Un's nuclear-site tour, the EU budget deadlock, Asia's
  market rebound, the Bank of Korea's hike to 3.25%, the Thanksgiving
  storm, the Cairo tanker fire, Hera's DART crater survey, Gukesh's draw
  with Sindarov.
- **Briefs:** Trump's message to Putin, the tariff doubling-down, the
  $622m F-16 deal, the EU's Russian-import ban, Zelensky's warning, the
  London Tube strike, Depardieu's trial, New Zealand's count, Serbia's
  vote, Kenya's Ebola-centre ruling, the Congo outbreak, Iraq's life
  sentences, Mexico's protests, Brazil's finance pick, India's hockey
  win, the Idefix moon rover, SpaceX's $44bn Nvidia chip deal, and more.
