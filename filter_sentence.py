from array import array
from operator import indexOf
import re
from tokenize import Special
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
import nltk
from jaro_winkler import jaro_Winkler
from data.raw_profanity import raw_profanity

alt_chars = {
    'a':['4','@','λ','∂'],
    'b':['8','|3','6','13','l3',']3','|o','1o','lo','ß',']]3','|8','l8','18',']8'],
    'd':['|]','l]','1]','|)','l)','1)','[)','|}','l]','1}','])','i>','|>','l>','1>','cl','o|','o1','ol','Ð','∂','ð'],
    'e':['3','&','[-','€','ii','ə','£','iii'],
    'f':['|=',']=','}','(=','[=','ʃ'],
    'g':['6','9','&','(_+','C-','cj','[','(γ,','(_-'],
    'h':['|-|','#','[-]','{-}',']-[',')-(','(-)',':-:','}{','}-{','aych','╫',']]-[['],
    'i':['!','1','|'],
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
    'y':['j','`/','Ψ','φ','λ','Ч','¥'],
}

def whitespace_tokenizer(sentence):
    white_space_tokenizer = nltk.WhitespaceTokenizer()
    return white_space_tokenizer.tokenize(sentence)

def to_lowercase(string):
    return string.lower()

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
def is_stopword(word):
    if word in filipino_stopwords:
        return True
    else:
        return False

#mag binary dito 
def is_filipino_word(word):
    if binary_search(tagalog_words, 0, len(tagalog_words), word) < 0:
        return False
    else:
        return True

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

if __name__ == '__main__':
    sentence2 = 'ang mga puta ibon putang-!na mo na lumilipad ay t4rant@do odatnarat ogag G@go ka hinayup4k ka'
    sentence1 = "gago kaba the quick brown fox gago ka puta"
    
    tokens = whitespace_tokenizer(sentence2.lower())

    toPrint = list()
    leet_value =None
    for word in tokens:
        if(is_stopword(word)):
            # toPrint.append(word)
            # print("stop words: ",word)
            continue
        if (is_filipino_word(word)):
            # toPrint.append(word)
            # print("Filipino words: ",word)
            continue
        if is_leet(word):
            # print(word)
            leet_value = word_leet_to_tagalog(word)
        for profanity in raw_profanity:
            if leet_value is not None:
                jw =jaro_Winkler(leet_value, profanity) 
                print(leet_value,': ',jw)

            jw =jaro_Winkler(word, profanity) 
            # if jw > 0.6 and jw <0.93:
            if jw > 0.93:
                # x= ''.join(['*' for x in word])
                # print('>93')
                # toPrint.append('('+word+')')
                x = ''.join(['*' for x in word])
                tokens[tokens.index(word)] = word.replace(word,x)
                break
        leet_value = None
        # toPrint.append(word)
    
    print(' '.join(tokens))
    #"gago kaba the quick brown fox gago ka puta"
    # { 
    # 1 : {'gago': { 'isProfane': True },}

    # 
    # }
    
    ls = ['ang', 'gago', 'mo', 'gago', 'ka']
    dict = {
        'ang': {'isProfance': False, 'isStopword': False, 'isLeet': False, 'isDictionary': False},
        'gago': {'isProfance': True, 'isStopword': False, 'isLeet': False,'isDictionary': False},
        'mo': {'isProfance': False, 'isStopword': False, 'isLeet': False, 'isDictionary': False },
        'ka': {'isProfance': False, 'isStopword': False, 'isLeet': False, 'isDictionary': False},
    }
    backup = []
    for word in ls:
        for key, value in dict.items():
            if word == key and value['isProfance'] == True:
                x = ''.join(['*' for x in word])
                # ls[ls.index(word)] = word.replace(word,x)
                backup.append(x)
                break
            elif word == key and value['isProfance'] == False: 
                backup.append(word)
                break
                
    print(' '.join(backup))
    print(backup)
                
#

    
