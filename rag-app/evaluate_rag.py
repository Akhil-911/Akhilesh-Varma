import re
import time
from rag import answer

# (question, [acceptable keywords]) — the keywords must appear in a correct answer
TESTS = [
    ("How many attention heads does the base model use?", ["8", "eight"]),
    ("What is the model dimension d_model in the base model?", ["512"]),
    ("How many layers are in the encoder?", ["6", "six"]),
    ("What optimizer was used for training?", ["adam"]),
    ("What dropout rate does the base model use?", ["0.1"]),
    ("What BLEU score did the big model get on WMT 2014 English-to-German?", ["28.4"]),
    ("What kind of positional encoding is used?", ["sine", "sinusoid"]),
    ("What is the inner-layer dimensionality of the feed-forward network?", ["2048"]),
    ("How many warmup steps were used for the learning rate?", ["4000", "4,000"]),
    ("What hardware was used to train the models?", ["p100"]),
    # Not in the document: the correct behavior is to refuse
    ("What is the capital of France?", ["couldn't find"]),
    ("Who won the 2018 FIFA World Cup?", ["couldn't find"]),
]

def clean(text):
    text = text.lower().replace("’", "'")
    # remove page citations so "(p. 8)" doesn't count as the number 8
    return re.sub(r"[\(【\[]\s*pp?\.?\s*[\d,\s–-]+[\)】\]]", "", text)

correct = 0
for q, keywords in TESTS:
    try:
        text, pages = answer(q)
    except Exception as e:
        text = f"ERROR: {e}"
    ok = any(k in clean(text) for k in keywords)
    correct += ok
    print(("PASS  " if ok else "FAIL  ") + q)
    if not ok:
        print("      ->", text[:200].replace("\n", " "))
    time.sleep(3)   # stay under the free tier rate limit

print(f"\nScore: {correct}/{len(TESTS)} = {correct / len(TESTS):.0%}")