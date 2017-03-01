import os
import pdb
import json
import random
import re
import pickle
from collections import defaultdict, OrderedDict

dic = defaultdict(list)

def clean_text(text):
    # text = "<@U046T5KAN> logins are in LP"
    text = re.sub(r"<@[^ \|]+(\|)?([^>]*)>", r'\g<2>', text)
    text = re.sub(r"<http.*>", "here", text)
    text = re.sub(r"<#[^ ]*>", "", text)
    text = text.replace(">", "")
    return text.strip()

myvocab = pickle.load(open("models/reddit/chars_vocab.pkl", "rb"))

all_txts = []
for root, dirs, files in os.walk("WayBlazer Slack export Aug 24 2016"):
    for name in files:
        if name.endswith(".json") and not name.startswith("._"):
            dirname = root.rsplit("/", 1)[1]
            fp = os.path.join(root, name)
            myjson = json.load(open(fp))
            l = []
            for mj in myjson:
                text = mj.get("text", None)
                if text and len(text.split("\n")) < 3:
                    text = clean_text(text.encode("ascii","ignore"))
                    text = "".join([x for x in text if x in myvocab[0]])
                    if len(text) > 4 and len(text) < 200:
                        l.append(text.lower())
            l = [ii for n,ii in enumerate(l) if n == 0 or ii != l[n-1]]
            all_text = ">" + "\n>".join(l) + "\n"
            all_txts.append(all_text)
random.shuffle(all_txts)
fp = "data/wayblazer/input.txt"
with open(fp, "w") as f:
    f.write("\n".join(all_txts))