import csv

x=0
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x+=0
print(x)