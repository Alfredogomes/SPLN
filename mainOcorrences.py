import nltk
import fileinput, sys
import re
import numpy
import nomes as moreNames 

text = r'[A-Za-z](\.)?'
number = r'[0-9]+'

#dicionários com os nomes/localizacoes
names = dict()
places = dict()
organization = dict()
gpe = dict()

def anot(file):
    i=0
    anotado = []
    for line in file:
        if(re.findall(text,line)!=[]):
            anotado.append(line)
    return anotado

def findNames(file):
    s = anot(file)
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
                    elif chunk.label() == 'LOCATION':
                        name = ' '.join([c[0] for c in chunk])
                        if places.get(name):
                            places[name]+=1
                        else:
                            places[name]=1
                    elif chunk.label() == 'ORGANIZATION':
                        name = ' '.join([c[0] for c in chunk])
                        if organization.get(name):
                            organization[name]+=1
                        else:
                            organization[name]=1
                    elif chunk.label() == 'GPE':
                        name = ' '.join([c[0] for c in chunk])
                        if gpe.get(name):
                            gpe[name]+=1
                        else:
                            gpe[name]=1
                    # se não for do tipo person, ver se consta no dicionário
                    # e se constar incrementar a contagem dessa palavra
                    else : 
                        name = ' '.join([c[0] for c in chunk])
                        if names.get(name):
                            names[name] +=1
                # se for do tipo tuple e aparecer no dicionário que se está a construir
                #adicionar uma entrada
                if type(chunk) == tuple and chunk[1] != 'NN' and chunk[1] != 'VB':
                    if names.get(chunk[0]):
                            names[chunk[0]] +=1
                # Para descobrir os numeros
                if type(chunk) == tuple and chunk[1] == 'CD':
                    if re.match(number, chunk[0]):
                        print(chunk[0])
           
    return names

#junta o dicionário das personagens principais (findNames) com o dicionario
#properNameBag com mais nomes proprios não encontrados pelo primeiro dicionário
def joinWmoreNames(texto):
    more = moreNames.properNameBag(texto)
    for i in more:
        if i not in names:
            names.update({i : more.get(i)})
    return names

#imprime o nome dos "personagens" e as vezes que eles aparecem
def printPopularNames(names,type):
    for k,v in sorted(names.items(), key=lambda p:p[1], reverse=True):
        print(str(type) + ' -> ' + str(k) + ' has ' + str(v) + ' ocorrence(s)')

#_____Main______
file = fileinput.input()
texto = "".join(fileinput.input(sys.argv[1:]))

names = findNames(file)
joinWmoreNames(texto)
print("\n----------------NAMES----------------")
printPopularNames(names, "Name")
print("\n----------------LOCATIONS----------------")
printPopularNames(places, "Location")
print("\n----------------ORGANIZATIONS----------------")
printPopularNames(organization, "Organization")
print("\n----------------GEOPOLITICAL ENTITIES (CITIES,STATES,ETC)----------------")
printPopularNames(gpe, "GPE")