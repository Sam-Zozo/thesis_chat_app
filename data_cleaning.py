import re
from tokenize import Special
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
from data.raw_profanity import raw_profanity
# from data.tagalog_words2 import tagalog_words as t2
from nltk import regexp_tokenize
import nltk

from jaro_winkler import jaro_Winkler
alt_chars = {
    'a':["à","4","@","^","ci","λ","∂","ae","ä","*"],
    'b':['8','⒝','13','൫','ß','|8','l8','18','ḃ','v'],
    'd':['ḋ','ď','Ḋ','|)','])','cl','Ð','∂','ð','[)'],
    'e':['3','&','é','€','ii','ə','£','iii','*','ɇ'],
    'f':['ƒ',']=','}','(=','[=','ph','Ƒ','ḟ','Ḟ','ⓕ'],   
    'g':['6','9','q','(_-','ĝ','ǧ','ḡ','ģ','ǥ','ɠ'],
    'h':['|-|','#',']-[',')-(','}{','}-{','ḣ','ĥ','ȟ','ħ'], 
    'i':['!','1','|','*','‡'],
    'j':['dy','ĵ','Ĵ','ǰ','ɉ','Ɉ'],
    'k':['q','|<','|x','|{','/<','\\<','/x','\\x','ɮ','c'],
    'l':['ł','1','|','1_','l_','lJ','£','¬','el'],
    'm':['/\/\\','|\\/|','em','|v|','[v]','^^','nn','//\\\\//\\\\','/|\\','/|/|','.\\\\','/^^\\','/V\\','|^^|'],
    'n':['ñ','ń','|\\|','/\\/','//\\\\//','[\\]','<\\>','{\\}','//','[]\\[]',']\\[','~','₪','/|/','in'],
    'o':['ô','ö','ò','ó','œ','ø','ō','õ','0','()','oh','[]','¤','Ω','ω','*','[[]]','oh'],
    'p':['|o','lo','1o','|>','|7','l7','17','q','|d','ld','1d','℗','|º','1º','lº','þ','¶'],
    'r':['|2','l2','12','2','/2','I2','|^','l^','1^','|~','l~','1~','lz','[z','|`','l`','1`','.-','®','Я','ʁ','|?','l?','1?','arr'],
    's':['5','ß','ś','$','z','es','ʃ','§','š'],
    't':['7','ł','+','-|-','-l-','-1-','1','†'],
    'u':['v','l_l','1_1','(_)','[_]','{_}','y3w','\\_/','\\_\\','/_/','v','yew','yoo','yuu'],
    'v':['ʌ','\/','√','l/','|/'],
    'w':['\\/\\/','vv','\\^/','\\x/','\\|/','\\_|_/','\\//\\//','\\_:_/','Ш','ɰ'],
    'y':['ỷ','`/','Ψ','φ','λ','Ч','¥','ÿ'],
}

def whitespace_tokenizer(string):
    white_space_tokenizer = nltk.WhitespaceTokenizer()
    return dict.fromkeys(white_space_tokenizer.tokenize(string), {})

def to_lowercase(string):
    return string.lower()

def leet_checker(tokens):
    temp = tokens
    for key in temp:
        if is_leet(key): # if not normal word
            temp[key] = {'isLeet':  True, 'originalWord': str(word_leet_to_tagalog(key))}
            
        else:
            temp[key] = {'isLeet':  False}
    
    # for key ,value in temp.items():
    #     print(key, value)
    return temp

def is_leet(word):
    if not word.isalpha():
        return True
    return False

# character level translation of leet to tagalog
def word_leet_to_tagalog(word):
    bWord = word
    for char in word:
        char_leet_equivalent_dict = filter_the_dict(alt_chars, lambda elem: char in elem[1])
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

# marking stopwords
def stopwords_checker(tokens):
    temp=tokens
    for key in tokens:
        if key in filipino_stopwords or len(key) < 3:
            temp[key]['isStopword'] = True
        else:
            temp[key]['isStopword'] = False
    return temp

def filipino_word_checker(tokens):
    temp=tokens
    for key, value in tokens.items():
        if value['isStopword']:
            temp[key]['isDictionaryWord'] = True
            continue
        isWordToSearch = key
        if value['isLeet']:
            isWordToSearch = value['originalWord']
        if binary_search2(tagalog_words,isWordToSearch) < 0: #binary_search(tagalog_words, 0, len(tagalog_words), isWordToSearch) < 0:
            temp[key]['isDictionaryWord'] = False
        else:
            temp[key]['isDictionaryWord'] = True
    return temp

def binary_search(arr, lower_bound, upper_bound, word):
    if upper_bound >= lower_bound:
        mid = (upper_bound + lower_bound) // 2
        if arr[mid] == word:
            return mid
        elif arr[mid] > word:
            return binary_search(arr, lower_bound, mid - 1, word)
        else:
            return binary_search(arr, mid + 1, upper_bound, word)
    else:
        return -1   

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
def remove_special_chars(word): 
    return re.sub(r'[^\w]','',word.lower())

def init_default_values(tokens):
    for key, value in tokens.items():
        tokens[key]['isProfane'] = False
    return tokens

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

