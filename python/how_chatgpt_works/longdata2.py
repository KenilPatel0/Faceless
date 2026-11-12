G,R,Y,C,P="G","R","Y","C","P"
SCENES=[
dict(name="hook",kind="hook2",beats=[
 ("Ask an AI a question, and it answers like a person.",None,None),
 ("So what's really happening inside? Is it thinking? Searching the internet? Understanding you?",None,None),
 ("The real answer is simpler, and a bit weirder, than you'd expect.",None,None),
 ("In the next eight minutes, you'll understand how these chatbots work, why they sometimes lie with total confidence, and how to use them better. No math. I promise.",None,None)]),
dict(name="intro",kind="intro",beats=[("I'm Kenil, and this is TechXKenil.",None,None)]),
dict(name="auto",kind="auto",beats=[
 ("Idea one: it's autocomplete. You know the suggestion bar on your phone keyboard? You type, I'm on my, and it suggests, way.",None,None),
 ("A chatbot is that same idea, scaled up enormously.",None,None),
 ("Given all the text so far, it predicts the next small piece of text. Then it adds that piece, and predicts the next one. And the next.",None,None),
 ("That's it. Every answer you've ever read from a chatbot was built one piece at a time.",None,None),
 ("It doesn't write a whole answer in one go. It writes piece by piece, and each new piece depends on everything that came before it.",None,None)]),
dict(name="probs",kind="probs",beats=[
 ("Here's what that guess actually looks like. For a sentence like, the capital of France is, the model gives every possible next piece a score.",None,None),
 ("Paris gets a very high score. Other options get tiny ones.",None,None),
 ("Then it picks one, usually a likely one, with a little randomness. That's why you can ask the same question twice and get slightly different answers.",None,None),
 ("The pick gets added to the text, and then the whole process runs again for the next piece.",None,None)]),
dict(name="tok",kind="tok",beats=[
 ("Idea two: tokens. Those pieces are called tokens. Not letters, and not exactly words. Chunks.",None,None),
 ("A common word might be one token. A rare or long word might be split into several.",None,None),
 ("Here's a tokenizer-style demo. The exact split depends on the model, so treat this one as an example.",None,None),
 ("This matters later. The AI doesn't see letters the way you do, which is why some chatbots have famously stumbled on simple things, like counting the letters in a word.",None,None),
 ("Newer models are better at this, often because they spell the word out step by step. But it shows that a model reads text in a very different way than you do.",None,None)]),
dict(name="train",kind="list",heading="Idea 3: Training",accent=C,panel="num",prefix="STEP",beats=[
 ("Idea three: training. So how does it know what comes next? It's trained. Researchers feed it an enormous amount of text: books, websites, code, and conversations.","Feed it huge amounts of text",None),
 ("Then they play one game, billions of times. Hide the next token, and let the model guess.","Hide the next token, let it guess",None),
 ("Next, tell it how wrong the guess was.","Measure how wrong it was",None),
 ("Then adjust it, a tiny bit, so it does better next time. And repeat. Nobody types in rules about grammar or facts. The patterns come out of the guessing game.","Adjust a little, then repeat",None)]),
dict(name="params",kind="params",beats=[
 ("Inside the model are billions of numbers, called parameters. Think of them as dials.",None,None),
 ("Training is just tuning those dials, over and over, until the guesses get good.",None,None),
 ("And once training is done, the dials are fixed. In a normal chat, the model isn't changing while you talk to it. It's using what it already learned.",None,None)]),
dict(name="smart",kind="list",heading="Why it feels smart",accent=G,panel="good",beats=[
 ("So why does it feel like it understands you? To predict text well, the model has to pick up a lot of patterns. It picks up grammar patterns.","Grammar and style patterns",None),
 ("It picks up facts that appeared often in its training text.","Facts it saw often",None),
 ("And it picks up the patterns of reasoning, like how an explanation or a solution is usually laid out.","How explanations are laid out",None),
 ("Is that real understanding? Researchers still debate it. What we can say is that it's very good at patterns, and underneath, it's still predicting the next piece of text.",None,"Debated by researchers")]),
dict(name="assist",kind="list",heading="From autocomplete to assistant",accent=Y,panel="num",prefix="STAGE",beats=[
 ("Idea four: from autocomplete to assistant. But raw autocomplete isn't a helpful assistant. Ask it a question, and it might continue with more questions, like a list on a web page.","Raw autocomplete",None),
 ("So there's a second stage. The model is trained on examples of good answers.","Examples of good answers",None),
 ("Then people rate its responses, and it's adjusted to prefer the ones that are clear, helpful, and safe. That's why it talks like an assistant, instead of a random corner of the internet.","People rate its answers",None)]),
dict(name="desk",kind="desk",beats=[
 ("Idea five: the context window. A chatbot doesn't remember you the way a friend does. Everything it knows about this conversation is the text sent along with each message.",None,None),
 ("That's the context window. Think of it as a desk. Only so many pages fit.",None,None),
 ("If the conversation gets too long, older pages fall off the desk, and the model simply can't see them anymore.",None,None),
 ("Some products add a memory feature that saves notes between chats. But that's extra machinery added on top. The model itself still only sees what's on the desk.",None,None)]),
dict(name="hallu",kind="hallu",beats=[
 ("Now, the big one: why it makes things up. The model isn't looking facts up in a database. It's generating the most plausible next piece of text.",None,None),
 ("Most of the time, plausible and true are the same thing. So it's right a lot.",None,None),
 ("But when the model doesn't actually know, nothing in the basic process forces it to stop. It keeps going, and produces something that sounds right.",None,None),
 ("That's called a hallucination: fluent, confident, and wrong. And it isn't lying on purpose. The model doesn't know it's wrong. It just generated text that fits the pattern of a good answer.",None,None),
 ("Models are getting better at saying, I'm not sure. But it still happens, so the habit of checking matters.",None,None)]),
dict(name="tips",kind="list",heading="How to use this",accent=G,panel="num",prefix="TIP",beats=[
 ("So how do you use this? Three tips. One: give it the source text, and tell it to answer only from that. That's far more reliable than asking from memory.","Give it the source text",None),
 ("Two: for hard questions, ask it to work step by step. Writing out the steps gives it more room to reach a good answer.","Ask it to go step by step",None),
 ("Three: verify anything important. Names, numbers, links, and code. Many chatbots can now search the web or run code too. When they do, they're reading real pages and putting them into the context window. That helps, but you should still check the sources.","Verify important details",None)]),
dict(name="recap",kind="list",heading="Quick recap",accent=C,panel="good",beats=[
 ("So, a quick recap. Chatbots predict the next token.","Predict the next token",None),
 ("Training on huge amounts of text taught them patterns.","Trained on huge amounts of text",None),
 ("A second stage made them helpful.","A second stage made them helpful",None),
 ("They only see what's in the context window.","They only see the context window",None),
 ("And they can be confidently wrong.","They can be confidently wrong",None),
 ("None of that makes them useless. It just means you should use them like a fast, smart assistant that sometimes guesses, not like an oracle.",None,"A fast assistant, not an oracle")]),
dict(name="outro",kind="outro",beats=[("Next video, I'll show you how I use AI to write code without shipping garbage. Subscribe to TechXKenil so you don't miss it.",None,None)]),
]

_myths=dict(name="myths",kind="list",heading="Three common misunderstandings",accent=R,panel="bad",beats=[
 ("Let's clear up a few common misunderstandings. First, by default it isn't searching the internet while it answers. It's generating text from patterns it learned during training. Some products add web search on top, but that's a separate feature.","Not searching the web by default",None),
 ("Second, it isn't copying and pasting answers from a hidden library. It generates new text, piece by piece, which is why the same question can come back with different wording each time.","Not copy-pasting stored answers",None),
 ("Third, treat the confident tone carefully. A confident voice doesn't mean it's right. It's trained to sound fluent and helpful, whether or not it actually knows the answer.","Confident tone does not mean correct",None)])
_cut=dict(name="cutoff",kind="list",heading="One more thing: the cutoff",accent=Y,panel="change",beats=[
 ("One more thing worth knowing. A model's knowledge has a cutoff. It learned from text collected up to a certain date.","Learned up to a cutoff date",None),
 ("So it doesn't automatically know about recent events, new software versions, or this week's news.","Recent events? Not known by default",None),
 ("Search tools can fill that gap, but when it matters, double-check anything time-sensitive.","Search tools can help",None)])
_ex=dict(name="ex",kind="ex",beats=[
 ("Let me show you what that looks like in practice. Here's a weak way to ask. Tell me about the report. The model has nothing to anchor on, so it guesses what a report like that would probably say.",None,None),
 ("Here's a better way. Paste in the report text, and say, using only this text, list the three main risks. If the answer isn't in the text, say so.",None,None),
 ("Now the answer is grounded in the text you gave it, and you've given it permission to say, I don't know.",None,None),
 ("It takes a few extra seconds, and it removes a lot of guessing.",None,None)])
_n=lambda x:[s["name"] for s in SCENES].index(x)
SCENES.insert(_n("tips"),_cut); SCENES.insert(_n("cutoff"),_myths)
SCENES.insert(_n("recap"),_ex)

_use=dict(name="useful",kind="list",heading="What chatbots are great for",accent=G,panel="good",beats=[
 ("Before we finish, let's be fair about what chatbots are genuinely good at. They're great at drafting and rewriting text, when you give them the facts.","Drafting and rewriting",None),
 ("They're good at explaining ideas in simple terms, and you can keep asking follow-up questions until it clicks.","Explaining ideas simply",None),
 ("They're good at brainstorming options, when you don't need every option to be correct.","Brainstorming options",None),
 ("And they're good at summarizing text that you paste in. Notice the pattern: these are all jobs where the answer is shaped by the text in front of it.",None,"Strong when the text is in front of it")])
SCENES.insert([s["name"] for s in SCENES].index("recap"),_use)
