from parrot import Parrot
import warnings
import torch
from nltk import tokenize
import string

warnings.filterwarnings("ignore")
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

def set_random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def paraphrase(text):
    has_offer = False
    if "$session.params" in text:
        has_offer = True
        text = text.replace("$$session.params.counter_offer", "my counter offer")
    sentences = tokenize.sent_tokenize(text)
    t_paraphrases = []
    max = 0
    for sentence in sentences:
        paras_diverse = parrot.augment(input_phrase=sentence, do_diverse=True)
        paras_undiverse = parrot.augment(input_phrase=sentence, do_diverse=False)
        if paras_diverse and not paras_undiverse:
            paras = paras_diverse
        elif paras_undiverse and not paras_diverse:
            paras = paras_undiverse
        elif not paras_undiverse and not paras_diverse:
            paras = [(sentence, 0)]
        else:
            if len(paras_diverse) <= len(paras_undiverse):
                paras = paras_diverse 
            else: 
                paras = paras_undiverse
        paras = [para[0] for para in paras]
        if len(paras) > max:
            max = len(paras)
        t_paraphrases.append(paras)
    results = []
    for i in range(max):
        sentence = ""
        for j in range(len(t_paraphrases)):
            try:
                sentence += t_paraphrases[j][i] + ". "
            except:
                pass
        if has_offer:
            sentence = sentence.replace("my counter offer", "$$session.params.counter_offer")
            if "$session.params.counter_offer" not in sentence:
                sentence += "How about $$session.params.counter_offer?" + ". "
        results.append(sentence[: len(sentence) - 2])
    return results
