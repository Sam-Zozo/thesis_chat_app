import re
from tokenize import Special
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
from nltk import regexp_tokenize
import nltk


alt_chars = {
    'a':['4','@','λ','∂','*'],
    'b':['8','|3','6','13','l3',']3','|o','1o','lo','ß',']]3','|8','l8','18',']8'],
    'd':['|]','l]','1]','|)','l)','1)','[)','|}','l]','1}','])','i>','|>','l>','1>','cl','o|','o1','ol','Ð','∂','ð'],
    'e':['3','&','[-','€','ii','ə','£','iii','*'],
    'f':['|=',']=','}','(=','[=','ʃ'],
    'g':['6','9','&','(_+','C-','cj','[','(γ,','(_-'],
    'h':['|-|','#','[-]','{-}',']-[',')-(','(-)',':-:','}{','}-{','aych','╫',']]-[['],
    'i':['!','1','|','*'],
    'j':['dy','ĵ','Ĵ','ǰ','ɉ','Ɉ'],
    'k':['|<','|x','|{','/<','\\<','/x','\\x','ɮ','c'],
    'l':['1','7','|_','1_','l_','lJ','£','¬','el'],
    'm':['/\/\\','|\\/|','em','|v|','[v]','^^','nn','//\\\\//\\\\','/|\\','/|/|','.\\\\','/^^\\','/V\\','|^^|'],
    'n':['|\\|','/\\/','//\\\\//','[\\]','<\\>','{\\}','//','[]\\[]',']\\[','~','₪','/|/','in'],
    'o':['0','()','oh','[]','¤','Ω','ω','*','[[]]','oh'],
    'p':['|o','lo','1o','|>','|7','l7','17','q','|d','ld','1d','℗','|º','1º','lº','þ','¶'],
    'r':['|2','l2','12','2','/2','I2','|^','l^','1^','|~','l~','1~','lz','[z','|`','l`','1`','.-','®','Я','ʁ','|?','l?','1?','arr'],
    's':['5','$','z','es','2','§','š'],
    't':['7','+','-|-','-l-','-1-','1','†'],
    'u':['|_|','l_l','1_1','(_)','[_]','{_}','y3w','\\_/','\\_\\','/_/','µ','yew','yoo','yuu'],
    'v':['\\/','\\\\//','√'],
    'w':['\\/\\/','vv','\\^/','\\x/','\\|/','\\_|_/','\\_l_/','\\//\\//','\\_:_/',']i[','uu','Ш','ɰ','\\/1/','1/1/'],
    'y':['`/','Ψ','φ','λ','Ч','¥'],
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
    
    for key ,value in temp.items():
        print(key, value)
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
        # print("char leet equivalent: ",char_leet_equivalent_dict)
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

# removing stopwords check if pwede mag binary search
def stopwords_checker(tokens):
    temp=tokens
    for key in tokens:
        if key in filipino_stopwords:
            temp[key]['isStopword'] = True

        else:
            temp[key]['isStopword'] = False

    return temp

#mag binary dito 
def filipino_word_checker(tokens):
    
    temp=tokens
    for key, value in tokens.items():
        if value['isStopword']:
            continue
        isWordToSearch = key
        if value['isLeet']:
            isWordToSearch = value['originalWord']
        if binary_search(tagalog_words, 0, len(tagalog_words), isWordToSearch) < 0:
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

def remove_special_chars(word): 
    return re.sub(r'[^\w]','',word.lower())

def init_default_values(tokens):
    for key, value in tokens.items():
        tokens[key]['isProfane'] = False
    return tokens


# title = 'ang p 3 t s a  ng@yon ay pebrero ng bente-sais,  d@law@ng l!bo\'t bente dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
# sample = 'puta yayamanin jakol hhhh mahal pakiskis pakita g@go'
# tokens = whitespace_tokenizer(sample)
# tokens = leet_checker(tokens)
# tokens = stopwords_checker(tokens)
# tokens = filipino_word_checker(tokens)
# tokens = init_default_values(tokens)
# for key ,value in tokens.items():
#     print(key, value)





    