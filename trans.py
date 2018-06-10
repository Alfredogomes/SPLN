#!/usr/bin/python3.6
import fileinput, sys, collections
import sync as f

sub1 = fileinput.input(sys.argv[1])
sub2 = fileinput.input(sys.argv[2])
order1 = f.createDicNamesOrder(sub1)
order2 = f.createDicNamesOrder(sub2)
sub1 = fileinput.input(sys.argv[1])
sub2 = fileinput.input(sys.argv[2])
dic1= f.createDicTextTime(sub1)
dic2= f.createDicTextTime(sub2)

inter1,inter2 = f.intersectDicts(order1,order2)

set1 = set(dic1)
set2 = set(dic2)

dicTrans = {}
min1 = int(min(inter1))
min2 = int(min(inter2))
ind = min(min1,min2)

if min1 <= min2:
	interaux = inter1 
else:
	interaux = inter2
setaux= sorted(set(interaux),reverse=True)
print(setaux)
ind=setaux.pop()

# o dicionario é tempo: legenda
for n in set1.intersection(set2):
	
	if n == ind:
		if len(setaux) != 0:
			ind=setaux.pop()
		else:
			ind=-1
		line = "LINHA ALTERADA\n"
		for i in dic1[n]:
			line = line + "".join(str(i).replace("\n", " "))
		line = line + "---> " 
		for i in dic2[interaux[n][0]]:
			line = line + "".join(str(i).replace("\n", " "))
		line = line + "\n"
		line.replace(" ", "")
		dicTrans.update({n : line})
	else:		
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