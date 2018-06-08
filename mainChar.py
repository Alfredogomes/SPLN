import nltk
import fileinput
import re

text = r'[A-Za-z]'

def anot(file):
    i=0
    anotado = []
    for line in file:
        if(re.findall(text,line)!=[]):
            anotado.append(line)
    return anotado

def findNames(file):
    s = anot(file)
    names = dict()
    for line in s:
        for sent in nltk.sent_tokenize(line):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if type(chunk) == nltk.tree.Tree:
                    if chunk.label() == 'PERSON':
                        name = ' '.join([c[0] for c in chunk])
                        if names.get(name):
                            names[name]+=1
                        else:
                            names[name]=1
    return names

def printPopularNames(names):
    for k,v in sorted(names.items(), key=lambda p:p[1], reverse=True):
        print(k,v)

#_____Main______
file = fileinput.input()
names = findNames(file)
printPopularNames(names)