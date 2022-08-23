from transformers import *
import sys

logging.set_verbosity(logging.FATAL)
model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")

def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
  inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
  outputs = model.generate(**inputs, num_beams=num_beams, num_return_sequences=num_return_sequences)
  return tokenizer.batch_decode(outputs, skip_special_tokens=True)

def paraphrase_sentence(sentence):
    return get_paraphrased_sentences(model, tokenizer, sentence, num_beams=10, num_return_sequences=5)

def main():
    print(paraphrase_sentence(sys.argv[1]))
    sys.stdout.flush()
