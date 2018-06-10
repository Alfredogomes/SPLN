#!/usr/bin/python3.6
import sys

def whichLang(sub):
    subName = sub.split(".")
    lang = subName[len(subName)-2]
    print("Lingua:" ,lang)
    return lang


#__Main
