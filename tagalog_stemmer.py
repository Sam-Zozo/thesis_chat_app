from data.tagalog_words import tagalog_words
VOWELS = "aeiouAEIOU"
CONSONANTS = "bdghklmnngprstwyBDGHKLMNNGPRSTWY"

PREFIX_SET = [
	'nakikipag', 'pakikipag',
	'pinakama', 'pagpapa',
	'pinagka', 'panganga', 
	'makapag', 'nakapag', 
	'tagapag', 'makipag', 
	'nakipag', 'tigapag',
	'pakiki', 'magpa',
	'napaka', 'pinaka',
	'ipinag', 'pagka', 
	'pinag', 'mapag', 
	'mapa', 'taga', 
	'ipag', 'tiga', 
	'pala', 'pina', 
	'pang', 'naka',
	'nang', 'mang',
	'sing',
	'ipa', 'pam',
	'pan', 'pag',
	'tag', 'mai',
	'mag', 'nam',
	'nag', 'man',
	'may', 'ma',
	'na', 'ni',
	'pa', 'ka',
	'um', 'in',
	'i',
]

INFIX_SET = [
	'um', 'in',
]

SUFFIX_SET = [
	'syon',
	'dor', 'ita',
	'han', 'hin', 
	'ing', 'ang', 
	'ng', 'an', 
	'in',
]
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

def check_validation(word):
    return binary_search2(tagalog_words, word)
    
def clean_prefix(token,	 PREFIX):
	"""
		Checks token for prefixes. (ex. naligo = ligo)
			token: word to be stemmed for prefixes
		returns STRING
	"""

	if check_validation(token):
		return token

	for prefix in PREFIX_SET:
		if len(token) - len(prefix) >= 3 and \
			count_vowel(token[len(prefix):]) >= 2:

			if prefix == ('i') and check_consonant(token[2]):
				continue

			if '-' in token:	
				token = token.split('-')

				if token[0] == prefix and check_vowel(token[1][0]):
					PREFIX.append(prefix)
					return token[1]

				token = '-'.join(token)

			if token[0: len(prefix)] == prefix:
				if count_vowel(token[len(prefix):]) >= 2:
					# if check_vowel(token[len(token) - len(prefix) - 1]):
				# 	continue

					if prefix == 'panganga':
						PREFIX.append(prefix)
						return 'ka' + token[len(prefix):]
					
					PREFIX.append(prefix)
					return token[len(prefix):]

	return token

def check_vowel(substring):
	"""
		Checks if the substring is a vowel.
			letters: substring to be tested
		returns BOOLEAN
	"""

	return all(letter in VOWELS for letter in substring)


def check_consonant(substring):
	"""
		Checks if the letter is a consonant.
			letter: substring to be tested
		returns BOOLEAN
	"""

	return all(letter in CONSONANTS for letter in substring)



def count_vowel(token):
	"""
		Count vowels in a given token.
			token: string to be counted for vowels
		returns INTEGER
	"""

	count = 0

	for tok in token:
		if check_vowel(tok):
			count+=1

	return count


def count_consonant(token):
	"""
		Count consonants in a given token.
			token: string to be counted for consonants
		returns INTEGER
	"""

	count = 0

	for tok in token:
		if check_consonant(tok):
			count+=1

	return count