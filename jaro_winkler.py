

from math import floor, ceil
import re

import regex

def jaro_distance(s1, s2):
    if (s1 == s2):
        return 1.0
    len1 = len(s1)
    len2 = len(s2)
    max_dist = floor(max(len1, len2) / 2) - 1
    match = 0
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)
    
    for i in range(len1):
        for j in range(max(0, i - max_dist),min(len2, i + max_dist + 1)):
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break
    if (match == 0):
        return 0.0
    t = 0
    point = 0
    for i in range(len1):
        if (hash_s1[i]):
            while (hash_s2[point] == 0):
                point += 1
            if (s1[i] != s2[point]):
                t += 1
            point += 1
    t = t//2
    return (match/ len1 + match / len2 + (match - t) / match)/ 3.0

def jaro_Winkler(s1, s2) :
    jaro_dist = jaro_distance(s1, s2)
    if (jaro_dist > 0.7) :
        prefix = 0
        for i in range(min(len(s1), len(s2))) :
            if (s1[i] == s2[i]) :
                prefix += 1
            else :
                break

        prefix = min(4, prefix) # max characters to look beside
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)
    return jaro_dist

if __name__ == '__main__':
    
    # ls = ['Viagorea',	'ViagDrHa',	'V l a g r a ',	'VyAGRA','via---gra',	'viagrga' ,
    #     'via-gra','\'V 1 @ G\' Ra',	'Viagzra',	'viagdra',	'via_gra',	'ViaZUgra',
    #     'Viargvra',	'ViagrYa',	'Vii-agra',	'ViagWra',	'vi(@)gr@',	'Viagvra',
    #     'V-I-A-G-R-A', 'Vi-ag.ra',	'vigra'	,'Vkiagra',	'via.gra',	'v-ii-a=g-ra',
    #     'V l A G R A'	,'VIA7GRA',	'V/i/a/g/r/a',	'VIxAGRA ',	'Viaggra',	'vi@gr|@|',
    #     'ViaTagra',	'ViaVErga',	'Viagr(a',	'Viagr^a','Vi�gr�',	'Viagara',
    #     'Viag@ra',	'Viag&ra',	'vi@g*r@', 'V-i.a-g*r-a',	'V1@grA'	'ViaaPrga',
    #     'Vi$agra',	'ViaJ1gra',	'Viag$ra',	'via---gra',	'Vi.ag.ra', 	'Viaoygra',
    #     'Vi/agra',	'Viag%ra',	'Viarga',	'V|i|a|g|r|a',	'Viag)ra',	'vi@|g|r@',
    #     'Viag&ra','byagra','Vvv&iiiaggggraaa',	'vi**agra',	'vi@gr*@',	'vi-@gr@', 'V iagr a','Vvvv&iagraaa', 'V&iagra', 'viaaaaagrrrraaaa']
    # mga_zero =['V-I-A-G-R-A','\'V 1 @ G\' Ra','VyAGRA','V l A G R A','VIA7GRA']
    
    # for v in ls:
    #     print(v,': ', jaro_Winkler(re.sub(r'[^\w]','',v.lower()),'viagra')) # uo ie mas maikli mas mababa threshhold mas hamaba mas mataas
   # txt = jaro_Winkler("p-u-t-a-n-g-i-n-a-m-o",'putanginamo')
    #print(txt) # monggoloid "aammppuuttaa",'amputa'
    #odd string gagos
    #every even index 
    #pag hindi pumasa sa threshold 
    # aaaaapuutta -> di leet -> di stopword -> di filipino -> jw
    # jw >= '0.5' -> remove repeating(2chars max na itira pag magkakatabi ang characters) -> check if filipino
    # kung kelan gagamitin yung leet translator o ireremove na lang yung mga special chars

    #re.sub(r'[^\w]', ' ',txt ) 
    # \abcd
    # V-I-A-G-R-A

    print(jaro_Winkler('ggaaggoo', 'gago'))
    # print(re.sub(r'[^\w]','','p-u-!!!!!!!!!!!-n-a-m-o'))
    # "p-u-t-a-n-g-i-n-a-m-o",'putanginamo'
    # [([a-z]),[(+*)]]
    # do regex: if profane, remove all chars then check ; if not check for pattern in string

    

    