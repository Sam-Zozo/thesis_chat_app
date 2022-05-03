

from data_cleaning import *
from data.filipino_stopwords import filipino_stopwords
from trashfiles.tagalog_words import tagalog_words
from data.raw_profanity import raw_profanity
from jaro_winkler import jaro_Winkler
import time

def clean_text(string):
    string = to_lowercase(string)
    tokens = init_default_values(filipino_word_checker(stopwords_checker(leet_checker(whitespace_tokenizer(string)))))
    for key, value in tokens.items():
        if value['isStopword'] == False and value['isDictionaryWord'] == False:
            if value['isLeet'] == True:
                x = [x for x in raw_profanity if jaro_Winkler(value['originalWord'],x) > 0.78]
                if x:
                    tokens[key]['isProfane']  = True
                    # print(x)
                else:
                    tokens[key]['isProfane']  = False
            else:
                x = [x for x in raw_profanity if jaro_Winkler(key,x) > 0.78]
                if x:
                    tokens[key]['isProfane']  = True
                    # print(x)
                else:
                    tokens[key]['isProfane']  = False
        else:
            continue
    return tokens



if __name__ == "__main__":
    # sentence = 'ang p3tsa g@g0 ay pebrero ng Tite-sais,  d@law@ng l!bo\'t kantotan dos Unshaded votes and votes for Mayor Duterte goes to Mar Roxas according to some reports of ballot tests.  #AyawSaDILAW,1Na-Binay ??????'
    # sentence = 'ang mga puta ibon putang-!na mo na lumilipad ay t4rant@do odatnarat ogag G@go ka hinayup4k ka'
    sentence  = 'tsitsaron chicharon t tsitsa ang tupa taong... t4ng!n@ sikat boracay vivo bygon tungo bleach bahay bureau demolition lagot hotdog hayahay hinlalaki hugasan haiti iowa sayo jackenpoy kangaroo natakot centaur callalily cycle madamo queen lapagam letson checking nakakabagot alias pinocchio peccan pakulay tiktok bacha balangga punching lake pamangkin peanut pasa antigun guitar bukal tsina sierra buko kalye pahina atom bangka makina teargas tartana semplang bati tanglaw tagak ulap hugas bungal'
    start = time.time()    
    # sentence = 'puta ina mo olol'
    tokens = clean_text(sentence)
    
 
    end = time.time()
    for key, value in tokens.items():
        print(key, value)
    print('time: ', end - start)
    # for key, value in tokens.items():
    #     # if value['isProfane'] == True:
    #         print(key, value)

