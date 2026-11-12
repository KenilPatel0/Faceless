# short-13 · AI Architecture — "Why AI Answers in 15 Milliseconds"

Format: 1080×1920 @ 30fps, 42s. 100% TSX.

## The truth on screen

A real prompt streams tokens at 80 tokens/sec while an operations meter tracks the 140 trillion FLOPs per word. The comparison visualizes standard DDR5 RAM (64 GB/s) versus High-Bandwidth Memory (3,350 GB/s) and shows the KV-cache locking in memory so past tokens never recalculate.

## Beat sheet

| Beat | Time | On screen | VO |
|------|------|-----------|-----|
| HOOK | 0–3.4s | Neon stopwatch ticks 0ms to 15ms. Glitch title: "140 TRILLION MATH OPS IN 15ms". | "AI answers before your eye can physically blink. Here is how." |
| SETUP | 3.4–14s | Chat prompt box: "Tell me a joke". Token probability roulette spins: `mat (94%)`. | "Every word requires passing your prompt through eighty transformer layers and seventy billion parameters." |
| HARDWARE | 14–26s | CPU vs GPU race. CPU crawls at 30 seconds per word. GPU HBM3e transfers 3.3 terabytes per second. | "A normal computer takes thirty seconds per word. But AI chips use High Bandwidth Memory moving over three terabytes of data every single second." |
| KV-CACHE | 26–36s | Green memory blocks lock in place: KV Cache active. Compute time drops to a flat line. | "Add the KV Cache, which saves past words so the model never recalculates them, and you get instant streaming." |
| LOOP | 36–42s | Payoff card: "NOT STORED. CALCULATED." Dissolves back to frame 0 stopwatch. | "That is why AI feels like reading your mind. It is pure math at the speed of light." |

