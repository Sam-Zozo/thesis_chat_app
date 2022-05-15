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

VOWELS = "aeiouAEIOU"
CONSONANTS = "bdghklmnngprstwyBDGHKLMNNGPRSTWY"
NUMBERS = "1234567890"

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
    'm':['ḿ','ṁ','ṃ','m̀','ᵯ'],
    'n':['ñ','ń','ņ','ɲ','ŋ','ṅ','~','₪'],
    'o':['ô','ö','ò','ó','œ','ø','ō','õ','0','¤','Ω','ω','*'],
    'p':['|o','lo','1o','f','|>','|7','l7','17','q','|d','ld','1d','℗','|º','1º','lº','þ','¶'],
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
    c = 'wertyuiopasdghklvbnm'
    if word.isnumeric():
        return False
    for char in word:
        if not char in c:
            return True
    return False
    # if not word.isalpha(): 
    #     return True
    # return False

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

# list -> check if leet -> if leet translate -> perform stemming -> tag stopwords -> tag tagalog words -> jaro
def is_tagalog_characters(word):
    tag_char = 'wertyuiopasdghklvbnm'
    isAllTagChar = False
    for i in word:
        if i in tag_char:
            isAllTagChar = True
    return isAllTagChar

def tagalog_stemmer(tokens):
    l = list()
    temp = tokens
    for key, value in temp.items():
        if not value['isLeet']:
            l.append(key)
        else:
            l.append(value['originalWord'])
    # print(l)
    ls = stemmer('3', l, '1')
    # print("ls:",ls[1])
    for key, value in tokens.items():
        for dictionary in ls[0]:
            
            if dictionary['word'] == key: #nakapa typo?
                temp[key]['rootWord'] = dictionary['root']
            elif value.get('originalWord') and dictionary['word'] == value['originalWord']:
                temp[key]['rootWord'] = dictionary['root']
            # elif value.get('originalWord') and dictionary['word'] != value['originalWord']:
            #     temp[key]['rootWord'] = value['originalWord']
            # else:
            #     temp[key]['rootWord'] = ''
    return temp

def stopwords_checker(tokens):

    temp=tokens
    # print("test",temp)
    for key, value in tokens.items():
        toSearch = key
        # print('r = ',value['rootWord'])
        if toSearch in filipino_stopwords or len(toSearch) <= 3:
            temp[key]['isStopword'] = True
            continue
        if value['rootWord'] and value['rootWord'] != key:
            toSearch = value['rootWord']
        if toSearch in filipino_stopwords or len(toSearch) <= 3:
            temp[key]['isStopword'] = True
        else:
            temp[key]['isStopword'] = False
    return temp
def isAllVowels(word):
    count = 0
    for c in word:
        if c in VOWELS:
            count+=1
    if count == len(word):
        return True
    else:
        return False

def filipino_word_checker(tokens):
    temp=tokens

    for key, value in tokens.items():
        isWordToSearch = key
        if isAllVowels(key):
            temp[key]['isStopword'] = True
            continue
        if value['isStopword']:
            temp[key]['isDictionaryWord'] = True
            continue
        if binary_search2(tagalog_words,isWordToSearch) > 0: 
            temp[key]['isDictionaryWord'] = True
            continue
        # if value.get('orignalWord') and (binary_search2(tagalog_words,value.get('orignalWord')) )> 0: 
        #     temp[key]['isDictionaryWord'] = True
        #     continue
        isWordToSearch = value['rootWord']
        if binary_search2(tagalog_words,isWordToSearch) < 0: 
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

def init_default_values(tokens):
    for key in tokens.keys():
        # tokens[key]['isLeet'] = False
        # tokens[key]['originalWord'] = ''
        # tokens[key]['isStopword'] = False
        # tokens[key]['isDictionaryWord'] = False
        # tokens[key]['rootWord'] = ''
        tokens[key]['isProfane'] = False

    return tokens

def clean_text(string):
    threshold = 0.8
    string = to_lowercase(string)
    tokens = init_default_values(filipino_word_checker(stopwords_checker(tagalog_stemmer(leet_checker(whitespace_tokenizer(string))))))
    # tokens = init_default_values(filipino_word_checker(stopwords_checker(leet_checker(whitespace_tokenizer(string)))))
    for key, value in tokens.items():
        if value['isStopword'] == False and value['isDictionaryWord'] == False: #if not stopword AND not in dictionary
            x = [x for x in raw_profanity if jaro_Winkler(value['rootWord'],x) >= threshold]
            if x:
                tokens[key]['isProfane']  = True
                print(x)
            else:
                tokens[key]['isProfane']  = False
            # if value['isLeet'] == True:
            #     x = [x for x in raw_profanity if jaro_Winkler(value['originalWord'],x) >= threshold]
            #     if x:
            #         tokens[key]['isProfane']  = True
            #         print(x)
            #     else:
            #         tokens[key]['isProfane']  = False
            # else:
            #     x = [x for x in raw_profanity if jaro_Winkler(key,x) >= threshold]
            #     if x:
            #         tokens[key]['isProfane']  = True
            #         print(x)
            #     else:
            #         tokens[key]['isProfane']  = False
        else:
            continue
    return tokens

if __name__ == "__main__":
    # sentence = 'ang p3tsa g@g0 ay pebrero ng Tite-sais,  d@law@ng l!bo\'t kantotan dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
    sentence = 'aking bagong. p.. kamusta? nakakabaliw.. maglaba mag-aliw nakakabaliw. magaling? napakagaling! napakagastos@ kagalingan kagaguhan kahayupan kagastusan katangahan ttttaannggiiinnaa ppppppuuuttaaa '# bbm 88m ibon putang-!na mo na lumilipad ay t4rant@do odatnarat ogag G@go ka hinayup4k ka'
    # sentence = "Maka hugot ka, ha. Lagot ka kay Mar Roxas. ?? https://t.co/U29f1MDqv2"
    # stopwords = ' '.join(filipino_stopwords)
    
    #sentence  = 'kagastos nak@kasik@t ng tang!na ang napakasakit nakakaantok'
    start = time.time()    
    # sentence = 'puta ina mo olol'
    tokens = clean_text(sentence)
    
    end = time.time()
    # for key, value in tokens.items():
    #     print(key, value)
    print('time: ', end - start)
    for key, value in tokens.items():
        # if value['isProfane'] == True:
            print(key, value)

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

