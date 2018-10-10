import numpy as np
import pandas
import codecs
import re

dataframe = pandas.read_csv("tmp.csv", delimiter=",")
dataset = dataframe.values
x = dataset[:,0:1]
y = dataset[:,1]

x_tokens = []

for data in x:
    text = str(data[0])
    tokenizer = re.compile('\W+')
    tokens = tokenizer.split(text)
    i = 0
    for token in tokens:
        tokens[i] = token.lower()
        i += 1

    x_tokens.append(tokens)

    print(tokens)

print(x_tokens)