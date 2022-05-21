import re
import time
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
from data.raw_profanity import raw_profanity
from stemmer import CONSONANTS, stemmer_word
from jaro_winkler import jaro_Winkler
from nltk.tokenize import WhitespaceTokenizer

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
    tk = WhitespaceTokenizer()
    return dict.fromkeys(tk.tokenize(string.lower()))
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
    word = re.sub('[-.<>,`?}\]\[{=_\'\":]', '', word) 
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

def stopwords_checker(token):
    if len(token) < 3:
        return True
    if binary_search2(filipino_stopwords, token) > 0:
        return True
    return False

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

def check(word1, word2):
    count = 0
    for c in word1:
        if c in word2:
            count+=1
    if count == len(word1):
        return True
    else:
        return False

def clean_text(sentence):
    tokens = whitespace_tokenizer(sentence)
    newDict = tokens
    threshold = 0.8
    for key in tokens.keys():
        newDict[key] = {}
        if is_leet(key):
            newDict[key]['isLeet'] = True
            res = str(word_leet_to_tagalog(key))
            if (not res):
                res = key
            newDict[key]['originalWord'] = res 
        else:
            newDict[key]['isLeet'] = False
            newDict[key]['originalWord'] = key
        
        # if (len(key)<=4 or key.isnumeric() or check(key,'aeiou')) :
        #     newDict[key]['isStopword'] = True
        #     newDict[key]['rootWord'] = key
        #     newDict[key]['isDictionaryWord'] = False
        #     newDict[key]['isProfane'] = False   
        #     continue
        # if check(key,'-.<>,`?}\]\[{=_\'\"::'):
        #     newDict[key]['isStopword'] = True
        #     newDict[key]['rootWord'] = key
        #     newDict[key]['isDictionaryWord'] = False
        #     newDict[key]['isProfane'] = False 
        #     continue

        if len(newDict[key]['originalWord']) <= 4 and check(key,'-.<>,`?}\]\[{=_\'\"::') or newDict[key]['originalWord'].isnumeric():
            newDict[key]['isStopword'] = True
        else:
            newDict[key]['isStopword'] = stopwords_checker(newDict[key]['originalWord'])

        if newDict[key]['isStopword']:
            if newDict[key]['isLeet']:
                newDict[key]['rootWord'] = newDict[key]['originalWord']
            else:
                newDict[key]['rootWord'] = key
        else:
            if newDict[key]['isLeet']:
                res = stemmer_word(newDict[key]['originalWord'])  
                newDict[key]['rootWord'] = res[1][0]
            else:
                res = stemmer_word(key) 
                newDict[key]['rootWord'] =  res[1][0]

        toSearch = newDict[key]['rootWord']
        if not newDict[key]['isStopword'] and binary_search2(tagalog_words, toSearch) > 0 :
            newDict[key]['isDictionaryWord'] = True
        else:
            newDict[key]['isDictionaryWord'] = False
        
        if not (newDict[key]['isDictionaryWord'] or newDict[key]['isStopword']):
            profane_compare = [x for x in raw_profanity if jaro_Winkler(newDict[key]['rootWord'],x) >= threshold]
            if profane_compare:
                newDict[key]['isProfane'] = True
                newDict[key]['similarProfanity'] = profane_compare
            else:
                newDict[key]['isProfane'] = False
        else:
            newDict[key]['isProfane'] = False        
    return newDict


if __name__ == "__main__":
    # sentence = 'ang p3tsa g@g0 ay pebrero ng Tite-sais,  d@law@ng l!bo\'t kantotan dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
    # sentence = "    bu bu ???? bibilogan at ko pa p@ k@gandah@n kagandahan katangahan k@t@ngah@n umagang napakahusay tangina "#motta tae t@  ta e@ ea ae p3tsa g@g0  !* !@#$^&*() {O:WQESAD tang@"    
    # sentence = "pakyu kanilang ang ng T@nga pakyuu pakyooo paakyoo "#Pucha nakita b0bo!! t3ngene g@g0 t@ng@!! ko na kokey kapal si Binay. 131231 ???????'
    # sentence = '???? katangahan >>> <<< ... ,,, ]]] [[[  }}} {{{ ```' #lorya glukos grabe  granadilya atraso pakla pakyaw gripo syota bwaya granada bwiset klase globo grado grava swak swerte buweset"#kagandahan prin t@r@ntado 𝕥𝕒𝕟𝕘𝕚𝕟𝕒𝕞𝕠 kame ᴛᴀɴɢɪɴᴀ"
    # 'gl', 'gr', 'ng', 'kr', 'bw', 'kl', 'kw', 'ts', 'tr', 'pr', 'sw' ,'sy'
    # sentence = ' '.join(raw_profanity)
    #sentence  = 'kagastos nak@kasik@t ng tang!na ang napakasakit nakakaantok'
    sentence = '300 1234 123 !!! ??? -_- pota 30000 3000 222222 si Mar Roxas??!! palaki kadilaw'
    # tk = WhitespaceTokenizer()
    # print()
    # print('Sentence: ', sentence)
    # print('Tokenize: ',tk.tokenize(sentence))
    # print('Tokenize and Lowercase: ',tk.tokenize(sentence.lower()))
    
    # x = whitespace_tokenizer(sentence)
    # y=x
    # for z in x:
    #     y[z] = {}
    # print('Dictionary from Tokenize sentence: ',y)
    # print()
    start = time.time()  
    tokens = clean_text(sentence)
    
    end = time.time()
    for key, value in tokens.items():
        print(key, value)
    print('time: ', end - start)
  