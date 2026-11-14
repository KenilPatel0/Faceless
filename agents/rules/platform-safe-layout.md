# Platform Safe Layout & Collision Rules

1. **YouTube Shorts & Reels (9:16 Vertical Safe Zones):**
   - **Top Boundary:** Keep critical text and watermarks below $y = 380\text{px}$ (4K) / $y = 190\text{px}$ (1080p).
   - **Bottom Platform UI Zone:** Keep interactive buttons, cards, and hero elements above $y = 3100\text{px}$ (4K) / $y = 1550\text{px}$ (1080p) to avoid collisions with like/comment buttons and sound metadata.
   - **Caption Anchor:** Burned-in karaoke subtitles must be centered at $y = 3120\text{px}$ (4K) / $y = 1560\text{px}$ (1080p).
2. **Horizontal Videos (16:9 Landscape Safe Zones):**
   - **Bottom Clearance Zone:** Subtitles centered at $y = 2020\text{px}$ (4K) / $y = 1010\text{px}$ (1080p).
   - **Content Hard Cap:** Content layers must NEVER exceed $y = 1830\text{px}$ (4K) / $y = 915\text{px}$ (1080p), preserving an $80\text{px}$ safe clearance zone.
3. **Flashing & Contrast Limits (WCAG 2.2 Baseline):**
   - No rapid alternating black/white cuts or strobe flashes exceeding 3 transitions per second.
   - All text must maintain $\ge 4.5:1$ contrast against dark surfaces.
