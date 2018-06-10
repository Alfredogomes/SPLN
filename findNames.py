import fileinput, re, getopt, sys

palMai = r"(?:\b[A-ZÀ-Ý]\w+|[A-ZÀ-Ý]\.)"
preposicao = r"d[eao]s?"
fimDeFrase = r"([^A-ZÀ-Ý][.!?]\s+|\n{2,}(?:-\s*)?)([A-ZÀ-Ý])"

nomeProprio= palMai + "(?: (?:"+preposicao+" )?"+palMai+")*"

pont = r"[.!?:,]"

number = r'[0-9]+\.?[0-9]*'

# versão antiga para encontrar nomes começados com maiusculas
def findNames(numSub, sub, nomes):
    lst = []
    for line in sub:
        line = line.split(" ")
        for word in line:
            if(re.findall(nomeProprio, word) != []):
                newWord = re.split(pont,word)
                if len(newWord) > 1: #se foi retirado pontuação
                    lst.append(newWord[0])
                else: lst.append(word)
    if lst != []:
        nomes.update({numSub : lst})
    return nomes

def findNumbers(numSub, sub, numbers):
    lst = []
    for line in sub:
        line = line.split(" ")
        for word in line:
            if(re.findall(number, word) != []):
                for num in re.findall(number, word):
                    lst.append(num)
    if lst != []:
        numbers.update({numSub : lst})
    
    return numbers



#_____Main______
#subtitles = fileinput.input()  #ler o input
#findNames(teste)