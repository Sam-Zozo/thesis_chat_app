import re
import time
from tokenize import Special
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
from data.raw_profanity import raw_profanity
# from data.tagalog_words2 import tagalog_words as t2
from nltk import regexp_tokenize
import nltk
from stemmer import stemmer
from jaro_winkler import jaro_Winkler
from nltk.tokenize import WhitespaceTokenizer
import unicodedata

alt_chars = {
    'a':['à', '4', 'ᴀ', '@', '^', 'á', 'λ', '∂', 'æ', 'ä', '*'],
    'b':['8', '⒝', '൫', 'ß', 'ḃ', 'v'],
    'd':['ḋ', 'ď', 'ḋ', 'ḏ', 'ḓ', 'cl', 'ð', '∂', 'ð', 'ɗ', 'ḋ', 'ð'],
    'e':['3', '&', 'é', '€',  'ə', '£', '*', 'ɇ'],
    'f':['ƒ', '}', 'f', 'ƒ', 'ḟ', 'ḟ', 'ⓕ'],   
    'g':['6', '9', 'q','ɢ', 'ĝ', 'ǧ', 'ḡ', 'ģ', 'ǥ', 'ɠ'],
    'h':['卄', '#', 'ḥ', 'ḫ', 'ⱨ', 'ḣ', 'ĥ', 'ȟ', 'ħ'], 
    'i':['!', '1','ɪ', '|', '*', '‡', '𝓲', '/','\\'],
    'j':['dy', 'ĵ', 'ĵ', 'ǰ', 'ɉ', 'ɉ', ';'],
    'k':['q', 'ɮ', 'c'],
    'l':['ł', '1', '|', '£', '¬'],
    'm':['ḿ', 'ṁ', 'ṃ', 'm̀', 'ᵯ'],
    'n':['ñ', 'ń', 'ņ', 'ɴ' ,'ɲ', 'ŋ', 'ṅ', '~', '₪'],
    'o':['ô', 'ö', 'ò', 'ó', 'œ', 'ø', 'ō', 'õ', '0', '¤', 'ω', 'ω', '*'],
    'p':['f', 'q', '₱', '℗', 'þ', '¶'],
    'r':['2', '®', 'я', 'ʁ'],
    's':['5', 'ß', 'ś', 'ş', '$', 'z', 'es', 'ʃ', '§', 'š'],
    't':['7', 'ł', '+', '丅', '1', '†', 'ᴛ'],
    'u':['v', 'û', 'ù', 'ū', 'ú', 'ü'],
    'v':['ʌ', '√',],
    'w':['ш', 'ɰ'],
    'y':['ỷ', 'ψ', 'φ', 'λ', 'ч', '¥', 'ÿ']
}

def whitespace_tokenizer(string):
    # white_space_tokenizer = string.split(' ')
    tk = WhitespaceTokenizer()
    # string = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode()
    return dict.fromkeys(tk.tokenize(string))

def to_lowercase(string):
    return string.lower()

def leet_checker(tokens):
    temp = tokens
    for key in temp:
        if is_leet(key): # if not normal word
            temp[key] = {'isLeet':  True, 'originalWord': str(word_leet_to_tagalog(key))}
        else:
            temp[key] = {'isLeet':  False}
    return temp

def is_leet(word):
    c = 'wertyuiopasdghklbnm'
    if word.isnumeric():
        return False
    for char in word:
        if not char in c:
            return True
    return False

# character level translation of leet to tagalog
def word_leet_to_tagalog(word):
    
    word = re.sub('[-.<>,?}\]\[{=_\'\":]', '', word) 
    word = word.replace('()','o')
    bWord = word
    for char in word:
        char_leet_equivalent_dict = filter_the_dict(alt_chars, lambda elem: char in elem[1])
        # print(char_leet_equivalent_dict)
        if char_leet_equivalent_dict: # if not empty
            key = [k for k,v in char_leet_equivalent_dict.items() if char in v]
            bWord = bWord.replace(char,key[0])

    return bWord

def filter_the_dict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict


def tagalog_stemmer(tokens):
    l = list()
    temp = tokens
    for key, value in temp.items():
        if value['isStopword']:
            continue
        if not value['isLeet']:
            l.append(key)
        elif not value.get('originalWord'):
            continue
        else:
            l.append(value['originalWord'])
    ls = stemmer('3', l)
    for key, value in tokens.items():
        for dictionary in ls[0]:
            if dictionary['word'] == key: 
                temp[key]['rootWord'] = dictionary['root']
            elif value.get('originalWord') and dictionary['word'] == value['originalWord']:
                temp[key]['rootWord'] = dictionary['root']
            else: temp[key]['rootWord'] = key
    return temp

def stopwords_checker(tokens):
    temp=tokens
    for key in tokens.keys():
        if binary_search2(filipino_stopwords,key) > 0:
            temp[key]['isStopword'] = True
        else:
            temp[key]['isStopword'] = False
    return temp

def filipino_word_checker(tokens):
    temp=tokens
    for key, value in tokens.items():
        isWordToSearch = key
        if value['isStopword']:
            temp[key]['isDictionaryWord'] = False
            continue
        if binary_search2(tagalog_words,isWordToSearch) > 0: 
            temp[key]['isDictionaryWord'] = True
            continue
        # if value.get('originalWord'):
        isWordToSearch = value['rootWord']
        if binary_search2(tagalog_words,isWordToSearch) > 0: 
            temp[key]['isDictionaryWord'] = True
        else:
            temp[key]['isDictionaryWord'] = False
    return temp 

def binary_search2(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

def init_default_values(tokens):
    for key in tokens.keys():
        tokens[key]['isProfane'] = False
    return tokens

def isAllVowels(word):
    count = 0
    for c in word:
        if c in "aeiou":
            count+=1
    if count == len(word):
        return True
    else:
        return False

def clean_text(string):
    threshold = 0.8
    string = to_lowercase(string)
    tokens = init_default_values(filipino_word_checker(tagalog_stemmer(stopwords_checker(leet_checker(whitespace_tokenizer(string))))))
    # tokens = init_default_values(filipino_word_checker(stopwords_checker(leet_checker(whitespace_tokenizer(string)))))
    for key, value in tokens.items():
        if value['isStopword'] == False and value['isDictionaryWord'] == False: #if not stopword AND not in dictionary
            if isAllVowels(key) or key.isnumeric():
                continue
            
            x = [x for x in raw_profanity if jaro_Winkler(value['rootWord'],x) >= threshold]
            if x:
                tokens[key]['isProfane']  = True
                print(x)
            else:
                tokens[key]['isProfane']  = False
        else:
            continue
    return tokens

if __name__ == "__main__":
    # sentence = 'ang p3tsa g@g0 ay pebrero ng Tite-sais,  d@law@ng l!bo\'t kantotan dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
    sentence = "?????? tangina mo p3tsa g@g0  !* !@#$^&*() {O:WQESAD tang@"    
    # sentence = "pakyu kanilang ang ng T@nga pakyuu pakyooo paakyoo "#Pucha nakita b0bo!! t3ngene g@g0 t@ng@!! ko na kokey kapal si Binay. 131231 ???????'
    # sentence = " kahit Ş卄𝓲丅 tangina kapangggitan pikpik pekpek katanggggahan nognog 𝕥𝕒𝕟𝕘𝕚𝕟𝕒 𝕞𝕠"#kagandahan prin t@r@ntado 𝕥𝕒𝕟𝕘𝕚𝕟𝕒𝕞𝕠 kame ᴛᴀɴɢɪɴᴀ"
    # sentence = ' '.join(raw_profanity)
    
    #sentence  = 'kagastos nak@kasik@t ng tang!na ang napakasakit nakakaantok'
    start = time.time()    
    # sentence = 'puta ina mo olol'
    tokens = clean_text(sentence)
    
    end = time.time()
    for key, value in tokens.items():
        print(key, value)
    print('time: ', end - start)
    # x = 'Ako ay magaling sumayaw sab ni PRRD'
    # print('Sentence: ',x)
    # print('Tokenized: ', whitespace_tokenizer(x.lower()))
   # print(sentence)
   # for key, value in tokens.items():
        # if value['isProfane'] == True:
         #   print(key, value)

    # bWord = re.sub('[.,?\'\"]', '', 'bWord"')
    # print(bWord)
    # word = 'katalinuhan?'
    # # if word[word-1]:
    # print(word[len(word)-1])
# aeiou aaaaa oo aoie 
# print('817'.isnumeric())
# print(string.punctuation)
# print(word_leet_to_tagalog('pu7@n6!na'))
# title = 'es and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
# sample = 'puta qaqo yayamanin jakol hhhh mahal pakiskis pakita g@go'
# tokens = whitespace_tokenizer(sample)
# tokens = leet_checker(tokens)
# tokens = stopwords_checker(tokens)
# tokens = filipino_word_checker(tokens)
# tokens = init_default_values(tokens)
# for key, value in tokens.items():
#         if value['isStopword'] == False and value['isDictionaryWord'] == False:
#             if value['isLeet'] == True:
#                 x = [x for x in raw_profanity if jaro_Winkler(value['originalWord'],x) > 0.78]
#                 if x:
#                     tokens[key]['isProfane']  = True
#                     print(x)
#                 else:
#                     tokens[key]['isProfane']  = False
#             else:
#                 x = [x for x in raw_profanity if jaro_Winkler(key,x) > 0.78]
#                 if x:
#                     tokens[key]['isProfane']  = True
#                     print(x)
#                 else:
#                     tokens[key]['isProfane']  = False
#         else:
#             continue
# for key ,value in tokens.items():
#     print(key, value)

