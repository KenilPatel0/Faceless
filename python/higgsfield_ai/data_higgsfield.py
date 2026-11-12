# data_higgsfield.py
# TechXKenil: Faceless Video Production Data for Open Higgsfield AI Tutorial
# Covers: Mac & Windows setup, links in description, and real Open-Higgsfield app usage

G, R, Y, C, P = "G", "R", "Y", "C", "P"

SCENES = [
    dict(
        name="hook",
        kind="hook",
        heading="Open Higgsfield AI",
        beats=[
            (
                "Higgsfield AI became famous for cinematic camera moves and high-end video generation, but locked behind expensive monthly plans.",
                "Higgsfield: Cinematic Video AI",
                "Locked behind $30-$50/month"
            ),
            (
                "Now, an open-source alternative called Open Higgsfield AI has been released on GitHub, completely free for everyone.",
                "100% Free & Open Source",
                "Community MIT Release on GitHub"
            ),
            (
                "In this video, let's walk through how to install it on Mac and Windows, set it up, and generate your first video with the real open-source app. All links are in the description below.",
                "Mac & Windows Setup Guide",
                "Links in description below ⬇"
            ),
        ]
    ),
    dict(
        name="intro",
        kind="intro",
        beats=[
            ("I'm Kenil, and this is TechXKenil.", None, None)
        ]
    ),
    dict(
        name="install",
        kind="install_multiplatform",
        heading="1. Download & Installation (Mac & Windows)",
        accent=C,
        beats=[
            (
                "First, let's download the installer. All links are in the description. Head over to the official Open Higgsfield AI releases page on GitHub.",
                "Visit GitHub Releases",
                "Links in description ⬇"
            ),
            (
                "If you're on Mac with Apple Silicon, download the ARM64 DMG. If you're on an Intel Mac, grab the standard DMG. And if you're on Windows, download the Windows Setup EXE installer.",
                "Download for Mac or Windows",
                "Mac DMG (ARM/Intel) & Windows EXE"
            ),
            (
                "On Mac, drag the app into your Applications folder. Because it's open-source and unnotarized, macOS Gatekeeper may show a warning. To fix it in five seconds, open Terminal and run x-attr minus c-r followed by the app path.",
                "macOS Gatekeeper Terminal Fix",
                "xattr -cr '/Applications/Open Higgsfield AI.app'"
            ),
            (
                "On Windows, run the installer. If Windows Defender SmartScreen pops up saying Windows protected your PC, simply click More Info, and select Run Anyway.",
                "Windows SmartScreen Fix",
                "Click 'More info' → 'Run anyway'"
            ),
        ]
    ),
    dict(
        name="setup",
        kind="setup_local",
        heading="2. Setup & Configuration",
        accent=G,
        beats=[
            (
                "When you launch the app, you get a clean studio dashboard running locally on your laptop, supporting both image and video generation.",
                "Local Studio Dashboard",
                "Image • Video • Cinema Modes"
            ),
            (
                "Open Higgsfield is local-first, meaning you don't pay a monthly subscription. Instead, you bring your own free or pay-as-you-go API key, or connect your local ComfyUI runner.",
                "Local-First & BYOK Architecture",
                "No middleman subscription fees"
            ),
            (
                "Under settings, configure your provider like Muapi, Runware, or Google Vertex. Once connected, your studio is fully operational.",
                "Configure Model Provider",
                "BYOK: Muapi / Runware / ComfyUI"
            ),
        ]
    ),
    dict(
        name="example",
        kind="real_app_demo",
        heading="3. Hands-On Real App Demo",
        accent=P,
        beats=[
            (
                "Now let's see how to use the real app with an example. Inside the studio, click the Model selector. You can choose state-of-the-art models like Flux Dev, Nano Banana, or Kling.",
                "Real Model Selector",
                "Flux Dev • Nano Banana • Kling"
            ),
            (
                "Next, in the prompt box, enter your scene description, specifying atmospheric details, lighting, and camera perspective.",
                "Describe Scene & Prompt",
                "Cinematic lighting • 35mm lens"
            ),
            (
                "Select your aspect ratio—one-by-one square, sixteen-by-nine landscape for YouTube, or nine-by-sixteen for vertical shorts.",
                "Select Aspect Ratio",
                "1:1 Square • 16:9 Landscape • 9:16 Shorts"
            ),
            (
                "Click Generate. The engine orchestrates the model in real time, giving you cinematic, high-aesthetic results without paying thirty dollars a month.",
                "Real Real-Time Generation",
                "High-aesthetic output • $0 subscriptions"
            ),
        ]
    ),
    dict(
        name="verdict",
        kind="verdict_summary",
        heading="4. The Honest Verdict",
        accent=Y,
        beats=[
            (
                "Here is the honest verdict. Open Higgsfield gives you the exact multi-model studio experience without subscription lock-in.",
                "Exact Studio Experience",
                "Zero monthly subscription locks"
            ),
            (
                "Whether you run it on Mac or Windows, you pay only for the compute you actually use, or run completely free on local hardware.",
                "Mac & Windows Flexibility",
                "Pay pennies for compute or 100% free local"
            ),
            (
                "For creators and developers who want full control over their visual pipeline, it's one of the best open-source tools available today.",
                "Essential Open Creator Tool",
                "Full ownership of your creative stack"
            ),
        ]
    ),
    dict(
        name="outro",
        kind="outro",
        beats=[
            ("All links and commands are in the description below. Subscribe to TechXKenil for more honest AI and tech tutorials.", None, None)
        ]
    ),
]
