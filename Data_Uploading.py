import json
import Tokenization as TK
from pathlib import Path

def load_vntc_split(root_dir):
    texts = []
    for label_dir in Path(root_dir).iterdir():
        if not label_dir.is_dir():
            continue


        for file in label_dir.glob("*.txt"):
            text = file.read_text(encoding= "utf-16").strip()
            if text:
                Tokens = TK.Tokenization(text)
                texts.append(Tokens)
    return texts

texts = load_vntc_split("Train_Full/Train_Full")
data = texts

with open("vntc_train.json1", "w", encoding ="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False)+"\n")



