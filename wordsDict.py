#This includes many words.

from random import randint

WORDS_DIC_SUBJ_THIRDA = ['Apple','Ken','Banana','Jvvg','Everybody','Kaj','ST','She','He','The dog','Scratch Cat','Pico','Nano','Giga','Tera','Gobo','TemplatesFTW']
WORDS_FIRST="I"
WORDS_DIC_SUBJ_THIRDM = ['They','The dogs', 'The cats','My bags','The bots','Scratchers','People','You']

WORDS_SUBJ = []
for i in WORDS_DIC_SUBJ_THIRDA:
    WORDS_SUBJ.append(i)
for i in WORDS_DIC_SUBJ_THIRDM:
    WORDS_SUBJ.append(i)
WORDS_SUBJ.append(WORDS_FIRST)


WORDS_VERB = [
    {"name":"begin","third":"begins","past":"begun"},
    {"name":"break","third":"breaks","past":"broke"},
    {"name":"have","third":"has","past":"had","time":False},
    {"name":"want","third":"wants","past":"wanted","time":False},
    {"name":"need","third":"needs","past":"needed","time":False},
    {"name":"buy","third":"buys","past":"bought"},
    {"name":"read","third":"reads","past":"read"},
    {"name":"go to","third":"goes to","past":"went to"},
    {"name":"put","third":"puts","past":"put"},
    {"name":"sing","third":"sings","past":"sung"},
    {"name":"write","third":"writes","past":"wrote"},
    {"name":"know","third":"knows","past":"knew","time":False},
    {"name":"use","third":"uses","past":"used"},
    {"name":"make","third":"makes","past":"made"},
    {"name":"cook","third":"cooks","past":"cooked"},
]

WORDS_NOUN = [
    "a computer",
    "a book",
    "a clock",
    "a cup",
    "an eraser",
    "a pen",
    "a pencil",
    "a notebook",
    "a camera",
    "a cell phone",
    "an apple",
    "an orange",
    "a song",
    "a dictionary",
    "a card",
    "a ruler",
    "a bot",
    "a man",
    "a woman",
    "a student",
    "a teacher",
    "a Scratcher",
    "a textbook",
    "a TV",
    "a server",
    "a fish",
    "a head of lettuce",
    "a bun",
    "a ticket",
    "a lily",
    "a pancake",
    "an egg",
    "a carrot",
    "an eggplant",
    "a semicolon",
    "a faucet",
    "a bookstore",
    "a shop",
    "a store",
    "a bakery",
]

WORDS_HOW = ["well","very well","quickly","loudly","abroad","alone","later"]

WORDS_WHEN_NOW = ["every Wednesday","every Tuesday","every Monday","every Saturday","every Sunday","every Thursday","every Friday","every day","every weekend","every summer","every winter"]

WORDS_WHEN_PAST = ["then","yesterday","last night","last Wednesday","last Tuesday","last Monday","last Saturday","last Sunday","last Thursday","last Friday",]

def generate():
    subj = WORDS_SUBJ[randint(0,len(WORDS_SUBJ)-1)]
    verbdict = WORDS_VERB[randint(0,len(WORDS_VERB)-1)]
    if subj == WORDS_FIRST or subj in WORDS_DIC_SUBJ_THIRDM :
        verb = verbdict["name"]
    else:
        verb = verbdict["third"]
    obj = WORDS_NOUN[randint(0,len(WORDS_NOUN)-1)]
    if not randint(0,2):
        how = WORDS_HOW[randint(0,len(WORDS_HOW)-1)]
    else:
        how = ""
    if randint(0,1):
        verb = verbdict["past"]
        when = WORDS_WHEN_PAST[randint(0,len(WORDS_WHEN_PAST)-1)]
    elif verbdict.get("time",True):
        when = WORDS_WHEN_NOW[randint(0,len(WORDS_WHEN_NOW)-1)]
    else:
        when = ""
    return "{0} {1} {2}{3}{4}.".format(
        subj,
        verb,
        obj,
        (" " + how) if how != "" else how,
        (" " + when) if when != "" else when,
    )

