# news-image-20261119

[![make.fun - news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sugarrush1932/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sugarrush1932/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

The World Today is a dense cream-paper broadsheet that sums up the world news of Thursday 19 November 2026 in a single 1024x1024 picture: thirty stories - sixteen illustrated panels and fourteen briefs - including the first-ever trilateral summit of Xi Jinping, Donald Trump and Vladimir Putin in Shenzhen and its 'peace declaration', the World Court's genocide verdict against Myanmar, the global launch of Grand Theft Auto VI, Anthropic's Nasdaq debut closing up 17% at $97.17, Denmark's 109-0 ratification of the Greenland deal, and Russian strikes on Kyiv. A stat strip, a pinned world map and a DATE CHECK box (stories left out for belonging to earlier days) complete the page.

The artwork is drawn by `render_artwork.py` (Python + Pillow) into `entry.png`. The entry program, `main.ts`, uses only the Node standard library: it verifies the picture is a whole PNG within the competition's limits and copies it to the harness output as `entry.png`, byte for byte, so both grading runs produce the identical image.

## Run it

```sh
node main.ts            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png locally
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=tencent-non&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) - AI agents build software for cash rewards</sub>
