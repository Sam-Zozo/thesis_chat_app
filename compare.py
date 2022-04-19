

from data_cleaning import *
from data.filipino_stopwords import filipino_stopwords
from data.tagalog_words import tagalog_words
from data.raw_profanity import raw_profanity
from jaro_winkler import jaro_Winkler
import time
def binary_search(arr, lower_bound, upper_bound, word):
    if upper_bound >= lower_bound:
        mid = (upper_bound + lower_bound) // 2
        if arr[mid] == word:
            print('present: ',arr[lower_bound:upper_bound])
            return mid
        elif arr[mid] > word:
            print('lb: ', lower_bound, ' ub: ', mid - 1)
            return binary_search(arr, lower_bound, mid - 1, word)
        else:
            print('lb: ', mid+1, ' ub: ', upper_bound)
            return binary_search(arr, mid + 1, upper_bound, word)
    else:
        print('not present: ',arr[lower_bound:upper_bound])
        return -1

def clean_text(string):
    string = to_lowercase(string)
    tokens = whitespace_tokenizer(string)
    tokens = leet_checker(tokens)        
    tokens = stopwords_checker(tokens)
    tokens = init_default_values(tokens)
    for key, value in tokens.items():
        if value['isStopword'] == False:
            if value['isLeet'] == True:
                x = [x for x in raw_profanity if jaro_Winkler(value['originalWord'],x) > 0.84]
                if x:
                    tokens[key]['isProfane']  = True
                else:
                    tokens[key]['isProfane']  = False
            else:
                x = [x for x in raw_profanity if jaro_Winkler(key,x) > 0.84]
                if x:
                    tokens[key]['isProfane']  = True
                else:
                    tokens[key]['isProfane']  = False
        else:
            continue
    return tokens

def compare(tokens):
    x = [w for w in tokens if w in raw_profanity]
    print(x)


if __name__ == "__main__":
    # sentence = 'ang p3tsa g@g0 ay pebrero ng Tite-sais,  d@law@ng l!bo\'t kantotan dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
    sentence = 'ang mga puta ibon putang-!na mo na lumilipad ay t4rant@do odatnarat ogag G@go ka hinayup4k ka'
    start = time.time()    
    # sentence = 'puta ina mo olol'
    tokens = clean_text(sentence)
    
    
    end = time.time()
    print('time: ', end - start)
    for key, value in tokens.items():
        # if value['isProfane'] == True:
            print(key, value)

