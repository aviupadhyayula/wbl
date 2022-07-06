from parrot import Parrot
import torch
import warnings

warnings.filterwarnings("ignore")
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

def set_random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def random_state(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

def generate_paraphrases(phrase):
    do_diverse=False
    if len(phrase) > 10:
        do_diverse=True
    return parrot.augment(input_phrase=phrase, do_diverse=do_diverse, adequacy_threshold=0.70)

for phrase in generate_paraphrases("I cannot spend more than $7000."):
    print(phrase)
