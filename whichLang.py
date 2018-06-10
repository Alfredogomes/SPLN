#!/usr/bin/python3.6
import sys

def whichLang():
    res = []

    if len(sys.argv) == 2:
        sub1 = sys.argv[1]
        subName = sub1.split(".")
        lang = subName[len(subName)-2]
        print("Lingua:" ,lang)
        res.append(lang)
        return res

    elif len(sys.argv) > 2:
        for i in range(1,len(sys.argv)):
            sub = sys.argv[i]
            subName = sub.split(".")
            lang = subName[len(subName)-2]
            print("Lingua:" ,lang)
            res.append(lang)
        return res

#__Main
print(whichLang())
