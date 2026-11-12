G,R,Y,C,P="G","R","Y","C","P"

SCENES = [
    dict(
        name="hook",
        kind="hook",
        beats=[
            ("You type a prompt into an AI, press enter, and the first word appears almost instantly. Usually in under fifty milliseconds.", None, None),
            ("To put that in perspective, a human eye blink takes about three hundred milliseconds. The AI starts responding before your eye can physically close.", None, None),
            ("Yet to generate that single word, a model with seventy billion parameters has to run over one hundred and forty trillion math calculations.", None, None),
            ("So why doesn't it take several minutes? In the next five minutes, let's break down the hardware, the math, and the clever software tricks that make real-time AI possible. Without any hype.", None, None),
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
        name="tokens",
        kind="list",
        heading="1. The Token Problem",
        accent=C,
        panel="num",
        prefix="PART",
        beats=[
            ("First, let's look at how text generation actually works. Models do not write whole answers at once.", "Generates one token at a time", None),
            ("They predict one token at a time, where a token is a word or a small piece of a word.", "Tokens: small pieces of words", None),
            ("To pick that single token, your entire prompt is pushed through eighty or more transformer layers.", "80+ transformer layers per token", None),
            ("Then it appends the new token, and repeats the entire eighty layers for the next word. On a standard laptop CPU, this would take thirty seconds per word.", "Laptop CPU: 30s per token", "Standard CPU is 1000x too slow"),
        ]
    ),
    dict(
        name="silicon",
        kind="list",
        heading="2. The Silicon Advantage",
        accent=G,
        panel="good",
        beats=[
            ("The first breakthrough is hardware parallelism. A regular CPU has eight or sixteen powerful cores designed for one task at a time.", "CPUs: 8 to 16 general cores", None),
            ("An AI accelerator, like an NVIDIA H100 or a Google TPU, has tens of thousands of smaller cores working simultaneously.", "GPUs: 16,000+ parallel cores", None),
            ("Under the hood, transformer layers are almost entirely matrix multiplications. Grids of numbers multiplied and added together.", "Matrix multiplications: C = A x B", None),
            ("Dedicated Tensor Cores execute thousands of these multiplications in a single clock cycle, calculating trillions of operations in microseconds.", "Tensor Cores crunch ops in microseconds", "Specialized silicon for matrix math"),
        ]
    ),
    dict(
        name="bandwidth",
        kind="list",
        heading="3. Memory Bandwidth",
        accent=Y,
        panel="change",
        beats=[
            ("Raw calculation power, however, is not the hardest bottleneck. Memory bandwidth is.", "Real bottleneck: memory bandwidth", None),
            ("For every single token, the processor has to read over one hundred and forty gigabytes of model weights from memory.", "140 GB of weights read per token", None),
            ("Standard computer RAM transfers data at around sixty gigabytes per second, which would throttle the whole system.", "DDR5 RAM: ~60 GB per second", None),
            ("AI chips solve this with High Bandwidth Memory, stacked directly beside the processor, moving over three terabytes of data every second.", "HBM3e: 3.35 Terabytes per second", "50x faster than standard PC memory"),
        ]
    ),
    dict(
        name="tricks",
        kind="list",
        heading="4. The Software Tricks",
        accent=P,
        panel="num",
        prefix="TRICK",
        beats=[
            ("Even with fast hardware, three software techniques keep generation practical. The first is KV Caching.", "Trick 1: KV Caching", None),
            ("Instead of recalculating past words from scratch on every step, past attention keys and values are stored in fast cache memory.", "Saves past words in fast cache", None),
            ("The second trick is Speculative Decoding. A small one-billion model guesses five words ahead, and the large model verifies them in one pass.", "Trick 2: Speculative Decoding", None),
            ("The third trick is Quantization. Compressing weights from sixteen-bit numbers to eight or four-bit integers doubles memory throughput.", "Trick 3: INT4 Quantization", "Halves memory without losing quality"),
        ]
    ),
    dict(
        name="example",
        kind="list",
        heading="5. The Latency Breakdown",
        accent=Y,
        panel="num",
        prefix="STAGE",
        beats=[
            ("Let's look at the real-world numbers behind a single prompt, measured in actual milliseconds.", "Real-world latency budget", None),
            ("First: network roundtrip. Signals traveling over fiber optics take fifteen to twenty milliseconds to reach the data center.", "Network transit: 15-20 ms", None),
            ("Second: prompt prefill. The GPU ingests your question and computes the initial KV cache in about twenty milliseconds.", "Prompt prefill: ~20 ms", None),
            ("Third: token generation. Each subsequent token takes ten to fifteen milliseconds, streaming steadily back to your screen.", "Token sampling: 10-15 ms each", "Total time to first token: ~50 ms"),
        ]
    ),
    dict(
        name="myths",
        kind="list",
        heading="6. Common Myths",
        accent=R,
        panel="bad",
        beats=[
            ("Now, three common misconceptions about this speed. First: that the AI is searching a database. It is not. Nothing is pre-stored.", "Myth: searching a database", None),
            ("Second: that larger models must always feel slower. With pipeline parallelism, big models are distributed across multiple GPUs running in unison.", "Myth: larger models are slower", None),
            ("And third: that speed implies accuracy. An AI generates confident mistakes just as fast as facts, so human review remains essential.", "Speed does not equal truth", "Always verify code and numbers"),
        ]
    ),
    dict(
        name="streaming",
        kind="list",
        heading="7. Perceptual Speed",
        accent=C,
        panel="good",
        beats=[
            ("Finally, there is a design choice that makes AI feel instantaneous: Token Streaming.", "Token streaming via HTTP", None),
            ("If the server waited to finish all four hundred words before sending anything, you would wait four seconds and think it froze.", "Full answer: 4 seconds wait", None),
            ("Instead, it sends the first word the millisecond it is sampled, which is called Time To First Token.", "Time To First Token: under 50ms", None),
            ("Because humans read at roughly five words per second, and the AI outputs forty to eighty tokens per second, it easily stays ahead of your eyes.", "AI outpaces human reading speed", "Human: 5 words/sec | AI: 80 tokens/sec"),
        ]
    ),
    dict(
        name="recap",
        kind="list",
        heading="Quick Recap",
        accent=G,
        panel="good",
        beats=[
            ("To recap: AI answers aren't looked up in a database. They are calculated live.", "Calculated live, not retrieved", None),
            ("Tens of thousands of parallel cores and High Bandwidth Memory handle the raw data volume.", "Parallel cores + HBM memory", None),
            ("KV caching and speculative decoding eliminate redundant math.", "KV cache stops recalculations", None),
            ("And token streaming delivers words faster than you can physically read them.", "Streaming creates real-time flow", "Pure engineering, zero magic"),
        ]
    ),
    dict(
        name="verdict",
        kind="verdict",
        beats=[
            ("The result is what feels like magic: an answer that was nowhere on disk a second ago, mathematically generated in milliseconds.", None, None),
            ("Understanding the machinery helps you use these tools with the right expectations: powerful, fast, but fundamentally mathematical.", None, None),
        ]
    ),
    dict(
        name="outro",
        kind="outro",
        beats=[
            ("Subscribe to TechXKenil for more AI and tech, explained simply.", None, None),
        ]
    )
]
