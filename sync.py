#!/usr/bin/python3
import fileinput, re, collections, sys
import nltk
import findNames as fN

numSub = r"^([0-9])+(?!.)"   #expressão regular para o número da legenda no formato srt
time = r"([0-9]+[:])+[0-9]+[,][0-9]+" #exp regular para o tempo da legenda no formato srt 
text = r"[0-9]*['\s']?[A-Za-z]+" #exp. regular para o texto da legenda no formato srt

palMai = r"(?:\b[A-ZÀ-Ý]\w+|[A-ZÀ-Ý]\.)"
preposicao = r"d[eao]s?"
fimDeFrase = r"([^A-ZÀ-Ý][.!?]\s+|\n{2,}(?:-\s*)?)([A-ZÀ-Ý])"

nomeProprio = f"({palMai}(?: (?:{preposicao} )?{palMai})*)"

def createDicTextTime(subtitles): #cria um dicionário com o número da legenda e o texto da mesma
	listText = [] #lista com todas as ocorrências de frases 
	numText=0 #indica o número 
	dicTime = {} #dicionario com {numero da legenda: tempo da legenda}
	numTime=1 #indica o número do tempo

	for line in subtitles:
		if(re.findall(time, line) != []):
			dicTime.update({numTime : line[0:8]})
			numTime += 1
		elif(re.findall(text, line) != []):
				listText.append(line)
				numText +=1
		elif(re.findall(numSub,line) !=[]):
			pass
		else: 
			listText.append(line) 
			numText +=1

	j = 0
	eachSub = {}
	sub = 1	
	nomes = {}
	numbers = {}
	num = 1

	for sentence in listText:
		if j < numText-1:
			z=0
			string = []
			if listText[j] != "\n":
				while listText[j+z] != "\n":
					string.append(listText[j+z])
					z += 1
				eachSub.update({sub : string})
				sub += 1
			fN.findNames(num, string, nomes)
			fN.findNumbers(num, string, numbers)
			num += 1
			j = j+z+1

	print(eachSub)
	
	finalDic = {}

	for keyText,keyTime in zip(eachSub,dicTime):
		finalDic.update({dicTime.get(keyTime) : eachSub.get(keyText)})
	od = collections.OrderedDict(sorted(finalDic.items()))
	return od

def createDicNamesOrder(subtitles): # cria um dicionário com todos os nomes próprios por número de legenda
	listText = [] #lista com todas as ocorrências de frases 
	numText=0 
	dicOrder = {} #dicionario com {numero da legenda: tempo da legenda}
	numTime=1 #indica o número do tempo
	for line in subtitles:
		if(re.findall(time, line) != []):
			numTime +=1
		elif(re.findall(text, line) != []):
			for nome in re.findall(nomeProprio,line):
				
				tokens = nltk.tokenize.word_tokenize(nome)
				tag = nltk.pos_tag(tokens)[0]
				if tag[1] in ['NNP','CD']:
					if numTime in dicOrder:
						dicOrder[numTime].append(nome)
					else:
						dicOrder[numTime]=[nome]
		elif(re.findall(numSub,line) !=[]):
			pass
	return dicOrder

def sublist(ls1, ls2): # diz se ls1 é sublista de ls2 ou vice-versa
	def get_all_in(fst, sec): #devolve todos os elementos de fst que estão em sec
		for element in fst:
			if element in sec:
				yield element
	if ls1 == ls2:
		return 3
	for x1, x2 in zip(get_all_in(ls1, ls2), get_all_in(ls2, ls1)):
		if x1 != x2:
			return 0
		elif len(ls1) < len(ls2): # todos os elementos de ls1 estão em ls2
			return 1
		else:			# todos os elementos de ls2 estão em ls1
			return 2
	
def addToDict(dictionary,key,val):
	if key in dictionary:
		dictionary[key].append(val)
	else:
		dictionary[key]=[val]
	

def intersectDicts(dict1,dict2):
	inter1 = {}
	inter2 = {}

	compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

	for key in dict1.keys():
		for key2 in dict2.keys():
			intersect = sublist(dict1[key],dict2[key2]);
			if intersect == 3:
				if key not in inter1 and key2 not in inter2:
					addToDict(inter1,key,key2)
					addToDict(inter2,key2,key)
					break
			elif intersect == 1:	# se dict1[key] é uma sublista de dict2[key2]
				auxkey = str(int(key)+1)
				
				if auxkey in dict1.keys():
					auxList = dict1[key]+dict1[auxkey]
					if compare(auxList,dict2[key2]):
						if key not in inter2 and auxkey not in inter2:
							addToDict(inter2,key2,key)
							addToDict(inter2,key2,auxkey)
							break
			elif intersect == 2:	# se dict2[key] é uma sublista de dict1[key2]
				auxkey = str(int(key2)+1)				
				if auxkey in dict2.keys():
					auxList = dict2[key2]+dict2[auxkey]
					if compare(auxList,dict1[key]):
						if key2 not in inter1 and auxkey not in inter1:	
							addToDict(inter1,key,key2)
							addToDict(inter1,key,auxkey)
							break

	
	return (inter1,inter2)

#_____Main______
subs1 = fileinput.input(sys.argv[1])  #ler o input
subs2 = fileinput.input(sys.argv[2])
#createDicTextTime(subtitles)
dict1 = createDicNamesOrder(subs1)

dict2 = createDicNamesOrder(subs2)

#dict1 = {"1":["Manuel","Anthony"],"2":["Laura"] ,"3":["Bob", "Joe", "Texas"]}
#dict2 = {"1":["Manuel"],"2":["Anthony"], "3":["Laura"] ,"4":["Bob", "Joe"],"5":["Texas"]}
print(dict1)
print(dict2)
inter1,inter2 = intersectDicts(dict1,dict2)

print(inter1)
print(inter2)








		


















	


