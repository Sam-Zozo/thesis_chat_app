

from math import floor, ceil
import re

import regex

def jaro_distance(s1, s2):
    if (s1 == s2): # if s1 and s2 are the same return a score of 1
        return 1.0 
    # initialized length for both string
    len1 = len(s1) 
    len2 = len(s2)
    
    #get max distance 
    max_dist = floor(max(len1, len2) / 2) - 1
    match = 0
    hash_s1 = [0] * len(s1) 
    hash_s2 = [0] * len(s2)
    
    # Iterate through each character., check for matches
    #s1 = gago s2 = gaggoooo
    for i in range(len1):
        for j in range(max(0, i - max_dist),min(len2, i + max_dist + 1)):
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break
    # if no match found return a score of 0
    if (match == 0):
        return 0.0

    # number of characters that match but in the wrong order    
    transposition = 0
    point = 0
    # Compute for transpositions.
    for i in range(len1):
        if (hash_s1[i]): # 
            while (hash_s2[point] == 0):
                point += 1
            if (s1[i] != s2[point]):
                transposition += 1
            point += 1
    transposition = transposition//2
    return (match/ len1 + match / len2 + (match - transposition) / match)/ 3.0

def jaro_Winkler(s1, s2) :
    # compute for the jaro distance
    jaro_dist = jaro_distance(s1, s2)
    if (jaro_dist > 0.7) :
        prefix = 0
        # compute for the maximum prefix based on the minimum length of two string
        for i in range(min(len(s1), len(s2))) :
            if (s1[i] == s2[i]) :
                prefix += 1
            else :
                break
        prefix = min(4, prefix) # max of 4 characters to look 
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)
    return round(jaro_dist,2)

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

    print(jaro_Winkler('tangga', 'tanga'))
    # print(jaro_Winkler('gaaaaaagggggoooo', 'gago'))

    # gago      gaggoo
    # [0,0,0,0] [0,0,0,0,0,0]
    # 0
    # 0
    #            0   True               point=1
    #            0   True               point 6
    # if gago[0] !=  gaggoo[6]
    # if g != o     transpo=1           point=7
    # 

    # 0
    # 0
    # 

    # for i in range(len1):
    #     if (hash_s1[i]): // if 0
    #         while (hash_s2[point] == 0):
    #             point += 1
    #         if (s1[i] != s2[point]):
    #             transposition += 1
    #         point += 1
    # transposition = transposition//2
    # return (match/ len1 + match / len2 + (match - transposition) / match)/ 3.0

    # print(jaro_Winkler('gago', 'kagagohan'))
    # print(jaro_Winkler('Tarantado', 'tarantula'))
    # print(jaro_Winkler('karampot', 'kantot'))
    # print(jaro_Winkler('tamod', 'tatoo'))
    # print(jaro_Winkler('tarantado', 'tato'))
    # print(jaro_Winkler('tamod', 'totoo'))
    # print(jaro_Winkler('tarantado', 'totoo'))
    # print(jaro_Winkler('taong', 'tanga'))
    # print(jaro_Winkler('talong', 'tanga'))
    # print(jaro_Winkler('taon', 'tanga'))
    # print(jaro_Winkler('t', 'tae'))
    # print(jaro_Winkler('tsitsarong', 'timang'))
    # print(jaro_Winkler('tsitsarong', 'tigang'))
    # print(jaro_Winkler('rt', 'ratbu'))
    # print(jaro_Winkler('gago', 'ggaaggoo'))

    # print(jaro_Winkler('makitang', 'kantutan'))
    # print(jaro_Winkler('nitong', 'nognog'))
    # print(round(1.234, 2))
    # print(round(1.359, 2))

    # print(re.sub(r'[^\w]','','p-u-!!!!!!!!!!!-n-a-m-o'))
    # "p-u-t-a-n-g-i-n-a-m-o",'putanginamo'
    # [([a-z]),[(+*)]]
    # do regex: if profane, remove all chars then check ; if not check for pattern in string

    

    