G,R,Y,C,P="G","R","Y","C","P"
SCENES=[
dict(name="hook",kind="hook",beats=[
 ("Every week someone tells me coding is dead.",None,None),
 ("Every week someone else tells me nothing has changed.",None,None),
 ("I build apps and use AI every single day, with three years of experience. So here's my honest take.",None,None),
 ("I'm not here to hype AI, and I'm not here to scare you. I just want to tell you what I actually see.",None,None),
 ("And I'll tell you what I'd learn if I were starting today.",None,None)]),
dict(name="intro",kind="intro",beats=[("I'm Kenil, and this is TechXKenil.",None,None)]),
dict(name="good",kind="list",heading="What AI is great at",accent=G,panel="good",beats=[
 ("Let's be fair. AI is really good at boilerplate, the repetitive setup code that nobody enjoys writing.","Boilerplate code",None),
 ("It's good at building screens from a description. You say what you want, and you get a working first version.","Screens from a description",None),
 ("It's good at explaining code you don't understand. Honestly, this is one of the best uses of AI for a beginner.","Explaining unfamiliar code",None),
 ("It's good at writing first drafts of tests, which is something many of us skip when we're busy.","First drafts of tests",None),
 ("And it's good at converting things from one format to another, like turning a JSON response into a data model.","Converting between formats",None),
 ("Things that took me an hour now take minutes.",None,"1 hour  →  minutes"),
 ("What do all of these have in common? They follow clear patterns, and AI has seen those patterns many, many times.",None,"Clear patterns = AI is strong")]),
dict(name="example",kind="example",beats=[
 ("Here's a quick example from my own work. Take a login screen, with validation, error messages, and an API call.",None,None),
 ("Before AI, building that feature took me around three hours. I had to design the layout, write the validation rules, handle every error message, connect the API, and test it.",None,None),
 ("Now I describe what I want, let AI write the first draft, then review and fix it. That takes about twenty minutes.",None,None),
 ("The time I save goes into the parts that need real thinking, like what should happen when the network fails.",None,None),
 ("But the first draft is rarely perfect. Sometimes it misses an empty field, or handles errors in a way that doesn't match my app.",None,None),
 ("So I still check the security, the error handling, and the parts that touch real user data.",None,None),
 ("And I read every line, because if I ship it, it's mine.",None,None),
 ("That's the real change. Less typing, more judgment.",None,None)]),
dict(name="bad",kind="list",heading="What AI is still bad at",accent=R,panel="bad",beats=[
 ("Now, what is it still bad at? First, knowing what to build. AI will happily build whatever you ask for. It won't tell you that nobody needs that feature.","Knowing what to build",None),
 ("Second, judging tradeoffs. Should this be fast, cheap, or simple? Those choices depend on your users and your team, and the AI doesn't know either.","Judging tradeoffs",None),
 ("Third, debugging strange problems on one specific phone or setup. The bug that only happens on one device, with one system version, is still mostly yours to track down.","Debugging odd device issues",None),
 ("Fourth, keeping a codebase healthy for two years. Quick wins are easy. Structure, naming, and consistency over a long time take human care.","Keeping code healthy long-term",None),
 ("Fifth, understanding your actual business. It doesn't know your customers, your deadlines, or why that strange rule exists in your app.","Understanding your business",None),
 ("And it can't be responsible when something goes wrong. You are. If a bug reaches your users, nobody asks which tool wrote it.",None,"YOU are responsible")]),
dict(name="change",kind="list",heading="What changes for beginners",accent=Y,panel="change",beats=[
 ("Here's the honest part. Typing code quickly matters less. Speed used to be a real advantage, but now the typing is the cheap part.","↓  Typing code fast",None),
 ("What matters more is reading code, reviewing it, and describing problems clearly. If you can't tell whether the AI's answer is right, you can't use it safely.",["↑  Reading code","↑  Reviewing code","↑  Describing problems"],None),
 ("And the simplest jobs, like just build this basic form, are getting cheaper. Competing only on that is harder than it was a few years ago.","↓  Basic, simple tasks",None),
 ("Does that mean there are no opportunities? No. It means the entry point is different. You show value by understanding problems, not just by typing.",None,"The entry point is different"),
 ("Can I predict the job market? No. Nobody can. Anyone who sounds certain is selling something.",None,"Nobody can predict the job market")]),
dict(name="learn",kind="list",heading="What I'd learn today",accent=C,panel="num",prefix="",beats=[
 ("Here's what I'd learn today. Five things. One: fundamentals. How programs work, how data is stored, and how networks send information. When you know this, every new tool makes more sense.","Fundamentals",None),
 ("Two: debugging, because that's the skill AI helps with least. Learn to read error messages, reproduce a problem, and change one thing at a time.","Debugging",None),
 ("Three: one stack, deeply. For me that's Flutter. Pick yours, and go deep, instead of jumping between ten frameworks.","One stack, deeply",None),
 ("Four: git, testing, and how to read other people's code. Most real work is reading and changing code that already exists.","Git, testing, reading code",None),
 ("Five: how to explain a problem clearly, in writing. That last one makes you better with AI too, because a clear question gets a much better answer.","Explain problems in writing",None)]),
dict(name="plan",kind="list",heading="A 90-day plan",accent=P,panel="num",prefix="MONTH",beats=[
 ("Here's a simple ninety day plan. Month one: fundamentals and one language, with AI as a tutor. Ask it to explain, not to write everything. If it gives you code, ask why it works.","Month 1: Learn the basics",None),
 ("Month two: build one small app, using AI for help, but you must be able to explain every line. A to-do app or a budget tracker is enough. Keep it small, and finish it.","Month 2: Build one small app",None),
 ("Month three: finish it, put it on GitHub, and write a short post about what you learned. That is more convincing to an employer or a client than a certificate. It shows you can actually build something.","Month 3: Finish and publish",None)]),
dict(name="tutor",kind="list",heading="AI as a tutor, not a crutch",accent=G,panel="num",prefix="STEP",beats=[
 ("Use AI as a tutor, not a crutch. Try this: write your own solution first, even if it's messy.","Write your own solution",None),
 ("Then ask the AI to review it,","Ask AI to review it",None),
 ("and show you a better way. You'll learn faster than if you ask for the answer first.","Learn the better way",None),
 ("And finally, explain the better version in your own words. A simple rule: if you can't explain it, you don't own it yet.","Explain it in your own words",None)]),
dict(name="mistakes",kind="list",heading="Mistakes to avoid",accent=Y,panel="change",beats=[
 ("Before we wrap up, here are a few mistakes I'd avoid. First, copying code you don't understand. It works today, then breaks at the worst time, and you can't fix it.","Copying code you don't understand",None),
 ("Second, skipping fundamentals because AI can do it for you. Then you can't tell when the answer is wrong.","Skipping fundamentals",None),
 ("Third, watching tutorials forever and never shipping anything. One finished small project teaches more than ten half-watched courses.","Tutorials without building",None),
 ("Fourth, comparing yourself to the AI. It's fast, but it doesn't understand your goals. You're not trying to beat it. You're learning to direct it.","Competing with the AI",None),
 ("Avoid these four, and you're already on a much better path.",None,"Avoid these 4")]),
dict(name="verdict",kind="verdict",beats=[
 ("So, is it worth it? Yes, if you learn to think and to build, not just to memorize syntax.",None,None),
 ("AI makes average code cheap. Good judgment is still expensive.",None,None),
 ("To recap. Learn the fundamentals. Build real projects, and explain every line. And use AI as a tutor, not a crutch. That's my honest answer.",None,None)]),
dict(name="outro",kind="outro",beats=[("If you want more videos like this, subscribe to TechXKenil, and tell me in the comments what you're trying to build.",None,None)]),
]

_myths=dict(name="myths",kind="list",heading="Myths I keep hearing",accent=C,panel="change",beats=[
 ("Let me clear up a few myths I keep hearing. Myth one: AI will replace every programmer next year. In my daily work, AI speeds me up, but I still decide what to build, and why.","Myth: replaced next year",None),
 ("Myth two: nothing has changed, so you can learn the way people did ten years ago. That's not true either. The tools are different, and the way you learn should use them.","Myth: nothing has changed",None),
 ("Myth three: you need to memorize all the syntax before you start. You don't. Search, ask, and look things up. What you need is understanding, and that comes from building.","Myth: memorize all syntax",None),
 ("So the honest picture is somewhere in the middle. Coding is changing, not ending.",None,"Changing, not ending")])
_habits=dict(name="habits",kind="list",heading="4 habits for using AI well",accent=G,panel="num",prefix="HABIT",beats=[
 ("Let me share a few habits that make AI far more useful. First, be specific. Instead of saying build a login screen, say what fields it needs, what the validation rules are, and how you manage state.","Be specific",None),
 ("Second, give it context. Tell it your framework, your version, and what you already tried. A better question gets a better answer.","Give it context",None),
 ("Third, ask for small pieces instead of a whole app at once. Small pieces are easier to review, test, and fix.","Ask for small pieces",None),
 ("And fourth, review before you run. Read it, understand it, and test it. That one habit separates people who use AI well from people who just copy and paste.","Review before you run",None)])
_i=[s["name"] for s in SCENES].index("learn"); SCENES.insert(_i,_myths)
_i=[s["name"] for s in SCENES].index("mistakes"); SCENES.insert(_i,_habits)

_tips=dict(name="tips",kind="list",heading="If you're just starting",accent=P,panel="num",prefix="TIP",beats=[
 ("If you're just starting out and feeling worried, here's some honest encouragement. Start small. A tiny project you finish is worth more than a huge one you abandon.","Start small",None),
 ("Be patient with yourself. Everyone feels lost at the beginning, even people who have been coding for years when they pick up a new technology.","Be patient with yourself",None),
 ("And share your work. Post it on GitHub, write about it, and ask for feedback. That's how people start to notice you.","Share your work",None)])
_i=[s["name"] for s in SCENES].index("verdict"); SCENES.insert(_i,_tips)
