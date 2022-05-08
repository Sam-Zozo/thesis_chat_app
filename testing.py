
from enum import unique
import pandas as pd
from compare import clean_text
import re

raw_data = pd.read_csv('test.csv')
# print(raw_data.head())
# df = pd.DataFrame(raw_data.head(), columns = ['text','init_eng_trans','fin_eng_trans','profanity_count','label2'])
# print(df)
# for columns in raw_data:
#     print(columns)

# data1 = raw_data.loc[raw_data["label2"] == 4]
# print(data1)

# for row in data1.iterrows():
#    test = clean_text(row)
# print(test)

def testing(string):
    profane_ctr = 0
    non_profane_ctr = 0
    x = clean_text(string)
    for value in x.values():
        if value['isProfane']:
            profane_ctr+=1
        else:
            non_profane_ctr+=1
                
    return profane_ctr, non_profane_ctr
    

profane_ctr = 0
total_ctr = 0
non_profane_ctr = 0

for column_name, column_value in raw_data.head(50).iterrows():
    print(column_name,column_value)
    # ctr = unique(column_value["label2"])
    # print(column_value["label2"])

    
    # if column_value["label2"] == 2 or column_value["label2"] == 3:
    #     text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",column_value["fin_eng_trans"]).split())
    #     x,y = testing(text)
    #     profane_ctr+=x
    #     non_profane_ctr+=y
    #     total_ctr = profane_ctr + non_profane_ctr
    # elif column_value["label2"] == 0 or column_value["label2"] == 1:
    #     # text = re.sub(r'^https?:\/\/.*[\r\n]*', '', column_value["fin_eng_trans"], flags=re.MULTILINE)
    #     text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",column_value["text"]).split())
    #     x,y = testing(text)
    #     profane_ctr+=x
    #     non_profane_ctr+=y
    #     total_ctr = profane_ctr + non_profane_ctr
    # elif column_value["label2"] == 4:
    #     text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",column_value["init_eng_trans"]).split())
    #     x,y = testing(text)
    #     profane_ctr+=x
    #     non_profane_ctr+=y
    #     total_ctr = profane_ctr + non_profane_ctr

        

print("Profane Words: ", profane_ctr)
print("Non Profane Words: ", non_profane_ctr)
      