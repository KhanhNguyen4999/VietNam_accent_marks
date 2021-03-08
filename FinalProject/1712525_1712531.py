# -*- coding: utf-8 -*-
from nltk import ngrams
from collections import Collection, defaultdict
from underthesea import word_tokenize
from tqdm import tqdm
from pickle import load, dump
from os import path
import argparse

def is_alpha_space(s):
  for i in s.split():
    if not i.isalpha():
      return False
  return True

def clean_doc_level_word(s):
  # B1: Chuyển thành chữ thường
  s_lower=s.lower()
  # B2: Tách từ
  s_word_token= word_tokenize(s_lower)
  # B3: Xóa các kí tự không phải là latin
  s_latin=[]
  for ss in s_word_token:
    if is_alpha_space(ss):
      s_latin.append(ss)
  # B4: Trả về
  return s_latin

def load_data_level_word(filename):
  super_token=[]
  with open(filename, encoding='utf-8') as file:
    for line in tqdm(file):
      super_token+=clean_doc_level_word(line)
  return super_token

# Phải dùng định nghĩa hàm chứ không được dùng lambda 
# vì sẽ không thể lưu dưới dạng file pickle được
def _zero():
  return 0

def _ngram():
  return defaultdict(_zero)

def compute_uni_gram(list_token):
  # Khai báo mô hình uni_gram mức từ.
  uni_gram=defaultdict(_zero)
  # Đếm số lần xuất hiện
  for w in list_token:
    uni_gram[w]+=1
  return uni_gram

# Nguồn: https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-language-model-nlp-python-code/
# Create a placeholder for model
def compute_bi_gram(list_token):
  bi_gram = defaultdict(_ngram)

  # Count frequency of co-occurance  
  for w1, w2 in ngrams(list_token,2):
      bi_gram[w1][w2] += 1

  return bi_gram


def compute_tri_gram(list_token):
  # Create a placeholder for model
  tri_gram = defaultdict(_ngram)

  # Count frequency of co-occurance  
  for w1, w2, w3 in ngrams(list_token,3):
    tri_gram[(w1, w2)][w3] += 1

  return tri_gram


def compute_four_gram(list_token):
  # Create a placeholder for model
  four_gram = defaultdict(_ngram)

  # Count frequency of co-occurance  
  for w1, w2, w3,w4 in ngrams(list_token,4):
    four_gram[(w1, w2, w3)][w4] += 1

  return four_gram


def compute_five_gram(list_token):
  # Create a placeholder for model
  five_gram = defaultdict(_ngram)

  # Count frequency of co-occurance  
  for w1, w2, w3,w4, w5 in ngrams(list_token,5):
    five_gram[(w1, w2, w3, w4)][w5] += 1

  return five_gram

def clean_doc_level_letter(s):
  """
  Tách câu s thành từng chữ (tách theo khoảng trắng)
  Đồng thời, xóa đi các kí tự không là chữ cái latin
  trong chuỗi s.
  --- INPUT ---
  s {string}: chuỗi cần tách

  --- OUTPUT ---
  {list} : danh sách các chữ trong chuỗi s.
  """
  new_s=[]
  
  for w in s.lower().split():
    w_iter = list(w)
    w_remove = w_iter.copy()
    for c in w_iter :
      if not c.isalpha():
        w_remove.remove(c)
    if w_remove:
      new_s.append(''.join(w_remove))

  return new_s

def load_data_level_letter(filename):
  super_token=[]
  with open(filename,encoding='utf-8') as file:
    for line in tqdm(file,desc="Time to load corpus: ", ascii=True):
      super_token+=clean_doc_level_letter(line)

  return super_token


# Tách từ từ theo khoảng trằng
def get_letter_token(super_token):
  letter_token=[]
  for w in super_token:
    letter_token+= w.split()

  return letter_token

# tải dữ liệu cho mô hình ngôn ngữ mức kí tự
def load_data_level_character(filename):
  char_token=[]
  with open(filename, encoding='utf-8') as file:
    for line in tqdm(file):
      char_token+=list(line.lower())

  return char_token

# Tiền xử lí trước khi đưa vào 2 - 5 gram
def preprocess_char(list_token):
  new_list_token = []
  for w in list_token:
    if w.isalpha():
      new_list_token.append(w)

  return new_list_token


# Tiến hành huấn luyện mô hình 
def train_language_model(corpus, level, n):
  """
  Huấn luyện mô hình ngôn ngữ mức kí tự, chữ, từ.
  Mô hình sẽ huấn luyện từ 1 - 5 gram.
  ---- INPUT ----
  + corpus (string) : đường dẫn đến file chứa ngữ liệu.
  + token (list)    : danh sách chứa token của theo mức cần huấn luyện.
  + level (string)  : gồm word (từ), letter (chữ) và char (kí tự).
  + n     (string)  : dạng số nguyên từ 1 - 5, chỉ số n trong n-gram cần huấn luyện. 

  ---- OUTPUT ----
  (defaultdict)     : thống kê số lượng n-gram trong ngữ liệu.

  """
  # Check tham số nhập vào:
  if not path.exists(corpus):
    print("Err: File not found!")
    return False
  if level not in ['char', 'word', 'letter']:
    print("Err: level only can be 'word' , 'letter' or 'char'.")
    return False
  if not n in ['1','2','3','4','5']:
    print("Err: n only can be 1 to 5.")
    return False    
  # Huấn luyện mô hình ngôn ngữ
  if (level=='char'):
    # B1: tải dữ liệu
    char_token = load_data_level_character(corpus)
    # B2: Huấn luyện mô hình
    # B2.1: Nếu là uni-gram (n = 1)
    if n=='1':
      return compute_uni_gram(char_token)
    # B2.2: Huấn luyện cho 2,3,4,5 gram
    else:
      #B2.2.1: Tiền xử lí trước khi đưa vào 2,3,4,5 gram
      new_char_token = preprocess_char(char_token)
      #B2.2.2: Huấn luyện mô hình 2,3,4,5 gram
      if n == '2':
        return compute_bi_gram(new_char_token)
      elif n == '3':
        return compute_tri_gram(new_char_token)
      elif n == '4':
        return compute_four_gram(new_char_token)
      elif n == '5':
        return compute_five_gram(new_char_token)
  elif level == 'letter':
    # B1: tải dữ liệu
    letter_token = load_data_level_letter(corpus)
    # B2: Huấn luyện mô hình
    if n == '1':
      return compute_uni_gram(letter_token)
    elif n == '2':
      return compute_bi_gram(letter_token)
    elif n == '3':
      return compute_tri_gram(letter_token)
    elif n == '4':
      return compute_four_gram(letter_token)
    elif n == '5':
      return compute_five_gram(letter_token)
  elif level =="word":
    # B1: tải dữ liệu
    word_token = load_data_level_word(corpus)
    # B2: Huấn luyện mô hình
    if n == '1':
      return compute_uni_gram(word_token)
    elif n == '2':
      return compute_bi_gram(word_token)
    elif n == '3':
      return compute_tri_gram(word_token)
    elif n == '4':
      return compute_four_gram(word_token)
    elif n == '5':
      return compute_five_gram(word_token)
  
    
if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--corpus", required=False,
    	help="path to corpus to train language model")
    ap.add_argument("-l", "--level", required=True,
    	help="level need to train (char, letter or word)")
    ap.add_argument("-n", "--ngram", required=True,
    	help="number n in n- grams")
    ap.add_argument("-t", "--token", required = False,
    	help="path to file pickle save list of token")
    ap.add_argument("-f", "--filemodel", required = True,
    	help="path to save file")
    args = vars(ap.parse_args())

    model = train_language_model(args['corpus'],args['level'],args['ngram'])
    print(model)
    # Save model
    with open(args['filemodel'],'wb') as fin:
        dump(model,fin)
    
    





