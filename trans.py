#!/usr/bin/python3.6
import fileinput, sys, collections
import sync as f

sub1 = fileinput.input(sys.argv[1])
sub2 = fileinput.input(sys.argv[2])
dic1= f.createDicTextTime(sub1)
dic2= f.createDicTextTime(sub2)

set1 = set(dic1)
set2 = set(dic2)

dicTrans = {}

# o dicionario é tempo: legenda
for n in set1.intersection(set2):
	line = ""
	for i in dic1[n]:
		line = line + "".join(str(i).replace("\n", " "))
	line = line + "---> " 
	for i in dic2[n]:
		line = line + "".join(str(i).replace("\n", " "))
	line = line + "\n"
	line.replace(" ", "")
	dicTrans.update({n : line})

#para ordenar o dicionario pelo "tempo"
od = collections.OrderedDict(sorted(dicTrans.items()))

# vamos colocar o dicionario numLegenda:legenda
numSub = 1

# e vamos colocar este dicionario n

for i in od:
	print(str(numSub) + ":\n", od[i])
	numSub +=1


#line= str(numSub) + "\n"
	#numSub +=1