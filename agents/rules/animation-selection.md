# Animation Selection Rules

1. **Meaning-First Selection:** Every animation must explain, emphasize, or connect semantic ideas. Never add motion merely to fill empty frames.
2. **Registry Constraint:** Only select animation IDs declared in `tools/animation_registry.py`. Never invent ad-hoc animation names or inline procedural hacks.
3. **Real UI Rule:** When demonstrating code or terminal commands, select `ui.code_line_focus` or `ui.terminal_exec` with genuine assets generated via `tools/capture_code.py`. Never draw synthetic Pillow mockups.
4. **Data Fidelity:** When visualizing metrics, select `data.counter` or `data.bar_grow` only if exact numbers/units are verified in scene data. Never animate unverified or made-up numbers.
5. **Conservative Transitions:** Use `transition.cut` by default. Only use `transition.directional_wipe` or `transition.dissolve` at explicit chapter boundaries.
6. **Fallback Requirement:** Every selected animation must declare a valid `fallback_animation_id` supported by the renderer.
7. **Topic-Specific Visual World:** Apart from the official channel Intro and Outro cards (which are strictly fixed for brand recognition), the entire visual world (background environment, color palette, card styling, and visual metaphors) must adapt dynamically to the subject matter. Choose from `blueprint`, `silicon`, `terminal`, `studio`, `minimal`, `obsidian`, or custom procedural themes. Never reuse the exact same background for every video.
