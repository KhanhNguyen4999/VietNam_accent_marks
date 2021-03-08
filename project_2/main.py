# MSSV: 1712525
# Họ tên: Nguyễn Ngọc Minh Khánh

## Mô tả cách chạy chương trình
#      --- Chương trình thực thi bằng tham số dòng lệnh với cấu trúc: python main.py file.txt

import re
import sys

special_token = ['Bc.', 'B.Sc.', 'B.A.', 'A.B.', 'B.Acy.', 'B.Acc.', 'M.S.',
                 'M.S.P.M.', 'M.', 'Fin.', 'D.Sc.', 'Prof.', 'Assoc.', 'Assist.',
                 'PGS.TS.', 'TS.', 'Th.s', 'a.m.', 'p.m.', 'KS.']

def split_sentences(s):
    '''
    Parameters:
        s: paragraph 

    return:
        list of sentence:
        type: list
    '''
    # REGEX to recognize where actually the end of the sentence
    regex = r'\.(?=\s[(A-Z)|\d])'

    list_index_termination = re.finditer(regex, s)
    # The list of the sentence
    ds_sentences = []
    start_idx = 0
    new_sentence=''
    # check if the seperation of sentence encounter the special case 
    flag = 0 
    for idx_ter in list_index_termination:
        end_idx = int(idx_ter.end())
        # potential sentence
        s_expect= s[start_idx:end_idx]
        # The right sentence
        new_sentence += s_expect
        # if it in a special case 
        if s_expect.split(' ')[-1] in special_token:
            start_idx = end_idx
            flag = 1
        else: # else it actually is a sentence
            ds_sentences.append(new_sentence)
            new_sentence = ''
            start_idx = end_idx+1
            flag = 0
    
    if flag == 1:
        ds_sentences.append(new_sentence + s[start_idx:])
    else:
        ds_sentences.append(s[start_idx:])

    return ds_sentences


def word_segmentation(ds_sentences, ds_word_token, max_token_len = 5):
    '''
    Paramaters:
        ds_sentences: The list of given sentence, type: list
        ds_word_token: the dictionary contains list of word, type: list
        max_token_len: the len of longest word in the dictionary

    return: The list of sentences that every sentence has been separated word
    '''
    # contain list of sentences that have been separated word
    ds_sentences_tokenizer = []
    for sentence in ds_sentences:
        # sentence_tokenizer contains seperated words
        sentence_tokenizer = []
        # Expected words that likely to combine to establish another word
        potential_maximum_match = []
        # slipt initial word in sentence
        list_terminate_by_space = sentence[:-1].strip().split(' ')
        # Total initial word split by space in sentence
        length = len(list_terminate_by_space)
        
        # Some variable in algorithm
        # The number of words can combine to create a meaning word in dictionary 
        n_word_match = 1
        # The index of position of the last word in meaning word 
        idx_n_word_match = 0
        # The index of currently word being reviewed 
        curr_idx = 0

        while(idx_n_word_match < length):
            word = list_terminate_by_space[curr_idx]
            # phải chuẩn hóa thêm
            if word[-1] in [',', '!', '?', ':', ';']:
                word = word[:-1]

            # Add word into 
            potential_maximum_match.append(word)

            if len(potential_maximum_match)>1:
                # Consider that the current word can combine with previously set of words to create a phrase
                # If can
                if ' '.join(potential_maximum_match).lower() in ds_word_token:
                    # update index of current as the lastest word in potential phrase
                    idx_n_word_match += len(potential_maximum_match) - n_word_match
                    # update the lenght of potential phrase
                    n_word_match = len(potential_maximum_match)# Chiều dài thỏa lớn nhất tới lúc này, tại sao không dùng n_word_match +=1 vì
                                                    # không phải lúc nào cũng liên tiếp

                # If the consideration that gain the longest of the word in the dictionary or have not enough word 
                # for building the longest possible word
                if (len(potential_maximum_match) == max_token_len) or (curr_idx == length-1):
                    sentence_tokenizer.append('_'.join(potential_maximum_match[:n_word_match]))
                    # Start again from here to consider the next meaning word
                    curr_idx = idx_n_word_match+1 
                    # update the index of position in the first word of next meaning word
                    idx_n_word_match += 1 # Bắt đầu tìm 1 cụm mới
                    # update the number of word in meaning word
                    n_word_match = 1 
                    # update 
                    potential_maximum_match = []                    
                else: # if not, continue to consider the next word has the ability to combine to generate the meaningful word
                    curr_idx += 1

                # If go through entirelly sentence, because the lastest word of meaningful word is at the end of the sentence
                if idx_n_word_match == length-1:
                    sentence_tokenizer.append('_'.join(list_terminate_by_space[-n_word_match:]))
                    break
            else:
                curr_idx+=1
                    
        # Add segmented sentence in a list
        ds_sentences_tokenizer.append(' '.join(sentence_tokenizer)+'.')

    return ds_sentences_tokenizer



if __name__ == "__main__":

    # Read file text
    file_text = open('input.txt', 'r', encoding = 'utf-8')
    ds_paragraph = file_text.readlines()

    # Read dictionary
    file_dict = open('VDic_uni.txt', 'r', encoding='utf-8')
    ds_word_token = file_dict.readlines()
    file_dict.close()
    # Find the longest string in dictionary and get the dictionary from file
    max_token_len = 0
    for i in range(len(ds_word_token)):
        ds_word_token[i] = ds_word_token[i].split('\t')[0]
        token_len = len(ds_word_token[i].split(' '))
        if token_len>max_token_len:
            max_token_len = token_len

    for idx, paragraph in enumerate(ds_paragraph):
        # Step 1: slip sentences
        ds_sentences = split_sentences(paragraph.rstrip('\n'))
        # Step 2: segment word that maximum matching in dict
        ds_sentences_tokenizer = word_segmentation(ds_sentences, ds_word_token, max_token_len)
        # print output on sentence separation and word separation
        # print('----Sentence separation and word separation in paragraph {}: '.format(idx))
        for s in ds_sentences_tokenizer:
            print(s)
    

