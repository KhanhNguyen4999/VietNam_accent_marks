import flask
from nltk import ngrams
from collections import defaultdict
from underthesea import word_tokenize
from tqdm import tqdm
import pickle
from os import path
import argparse
import numpy as np
import re

from flask import Flask, request, jsonify, render_template


def _zero():
  return 0

def _ngram():
  return defaultdict(_zero)

# Load language model
with open('bi_letter.plk', 'rb') as fout:
    bigram_letter = pickle.load(fout)

# total word
total_word = 0
for k in bigram_letter.keys():
    total_word += sum(bigram_letter[k].values())

#
vocab_size = len(bigram_letter)

# tính xác suất dùng smoothing
def get_proba(current_word, next_word):
    if current_word not in bigram_letter:
        return 1 / total_word
    if next_word not in bigram_letter[current_word]:

        return 1 / (sum(bigram_letter[current_word].values()) + vocab_size)
    return (bigram_letter[current_word][next_word] + 1) / (sum(bigram_letter[current_word].values()) + vocab_size)


def remove_vn_accent(word):
    word = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', word)
    word = re.sub('[éèẻẽẹêếềểễệ]', 'e', word)
    word = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', word)
    word = re.sub('[íìỉĩị]', 'i', word)
    word = re.sub('[úùủũụưứừửữự]', 'u', word)
    word = re.sub('[ýỳỷỹỵ]', 'y', word)
    word = re.sub('đ', 'd', word)
    return word


def gen_accents_word(word):
    word_no_accent = remove_vn_accent(word.lower())
    all_accent_word = {word}
    for w in open('vn_syllables.txt', encoding="utf8").read().splitlines():
        w_no_accent = remove_vn_accent(w.lower())
        if w_no_accent == word_no_accent:
            all_accent_word.add(w)
    return all_accent_word

# hàm beam search


def beam_search(words, k=3):
  sequences = []
  for idx, word in enumerate(words):
    if idx == 0:
      sequences = [([x], 0.0) for x in gen_accents_word(word)]
    else:
      all_sequences = []
      for seq in sequences:
        for next_word in gen_accents_word(word):
          current_word = seq[0][-1]
          proba = get_proba(current_word, next_word)
          # print(current_word, next_word, proba, log(proba))
          proba = np.log(proba)
          new_seq = seq[0].copy()
          new_seq.append(next_word)
          all_sequences.append((new_seq, seq[1] + proba))
      # sắp xếp và lấy k kết quả ngon nhất
      all_sequences = sorted(all_sequences, key=lambda x: x[1], reverse=True)
      sequences = all_sequences[:k]
  return sequences

# initiate 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/vietnamAccent", methods=["POST"])
def api_process():
    """
    Required params:
        input_text: string
    """

    input_text = request.form["input_text"]

    print(input_text)
    print("Hello" , type(input_text))

    output_str = beam_search(input_text.split())[0][0]
    print(output_str)
    return jsonify({"output":' '.join(output_str)})


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
