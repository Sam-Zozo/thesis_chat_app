
tagalog = []
with open('/Users/samorozco/Documents/thesis/profanity_filter/data/tagalog_dict.txt') as f:
    contents = f.read().split('\n')
    for line in contents:
        tagalog.append(line)
# print(tagalog)

# t = open('/Users/samorozco/Documents/thesis/profanity_filter/data/surena.txt',mode="a+",encoding="utf-8")

with open('/Users/samorozco/Documents/thesis/profanity_filter/data/tagalog_words.py', 'w') as f:
    for line in tagalog:
        f.write('"') 
        f.write(line)
        f.write('",\n')