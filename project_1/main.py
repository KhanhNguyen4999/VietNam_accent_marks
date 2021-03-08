# MSSV: 1712525
# Họ tên: Nguyễn Ngọc Minh Khánh

## Mô tả cách chạy chương trình
#      --- Chương trình thực thi bằng tham số dòng lệnh với cấu trúc: python main.py file.txt


import re
import sys

def get_ls_infor(text):
    '''
    Parameters: 
        - str: string that constain informations
    
    return: tuple : list of tuple with structure (start_index, length, string_match)
    
    '''

    ds_tuple = []
    regex_email = r'[\w|\-|\_]+@(gmail|yahoo)\.com'
    regex_sdt = r'(\(?(\+?\d{1,2}\s?)\)?\s?)?(\d{2,3}(\s|\.|-)?)(\d{3}(\s|\.|-)?)\d{4}'
            # explain:
                # (\(?(\+?\d{1,2}\s?)\)?\s?)?: capture 84 | +84 | (+84) or not
                # (\d{2,3}(\s|\.|-)?): check the first two numbers if starting with 84 otherwise check the first three numbers
                # (\d{3}(\s|\.|-)?): check the next three numbers
                # \d{4}: check the last 4 numbers
                # (\s|\.|-)?: separate by space, '.', '-' or not

    regex_web_addr = r'((http:\/\/|https:\/\/)(www)?|(http:\/\/|https:\/\/)?(www))(\.?\w+)+'
            # explain:
                # (http:\/\/|https:\/\/)?: match with http:// or https:// or not
                # (www): match with 'www'
                # (\.?\w+)+: capture with content of url

    # find all emails
    matches_email = re.finditer(regex_email, text)
    for match in matches_email: 
        val_str = match.group()
        ds_tuple.append((match.start(), len(val_str), val_str))

    # find all phone numbers   
    matches_sdt = re.finditer(regex_sdt, text)
    print(matches_sdt)
    for match in matches_sdt:
        val_str = match.group()
        ds_tuple.append((match.start(), len(val_str), val_str))

    # find all web addresses    
    matches_web_addr = re.finditer(regex_web_addr, text)
    for match in matches_web_addr:
        val_str = match.group()
        ds_tuple.append((match.start(), len(val_str), val_str))
    
    return ds_tuple



if  __name__ == "__main__":

    print("so luong tham so: {} tham so ".format(len(sys.argv)))
    print("danh sach tham so: ", str(sys.argv))

    f = open(sys.argv[1], 'r', encoding='utf-8')
    text = f.readlines()
    
    entire_text = ""
    for idx, v in enumerate(text):
        if idx == len(text)-1:
            entire_text+=v
        else:
            entire_text+=v[:-1] + ' '
    
    # print(entire_text)

    ds_tp_infor = get_ls_infor(entire_text)
    print("Print list infor: ")
    print(ds_tp_infor)
    

    