import requests as r
from html2json import collect
import json
from bs4 import BeautifulSoup

def sem_espaco(string):
    s=[]
    i=0
    j=0
    stop =False
    while not stop:
        
        while string[i] == ' ' and not stop:
            if i < len(string)-1:
                i += 1
            if i == len(string)-1:
                stop=True
        
        s.append('')
        
        while string[i] != ' ' and not stop:
            s[j] = s[j]+string[i]
            if i < len(string)-1:
                i += 1
            if i==len(string)-1:
                if string[i] != ' ':
                    s[j] = s[j]+string[i]
                stop=True
        j +=1
    return s

def padrao(p,string):
    
    ind = []
    i=0
    while i+len(p) <= len(string): 
        if string[i:i+len(p)] == p:
            ind.append([i,i+len(p)])
        i += 1
    return ind

def padrao_inicio_fim(inicio,fim,string):
    padrao1 = padrao(inicio,string)
    padrao2 = padrao(fim,string)
    
    padraoif = []
    
    padrao1.append([len(string),len(string)])
    for p2 in padrao2:
        for i in range(len(padrao1)-1):
            if p2[0]>=padrao1[i][0] and p2[1]<=padrao1[i+1][0] :
                if (len(padraoif)>0 and padrao1[i][0]>padraoif[len(padraoif)-1][0]) or len(padraoif)==0:
                    padraoif.append([padrao1[i][0],p2[1]])
    return padraoif

def mes(x): 
    
    dict_mes = {'Janeiro': 1,
                'Fevereiro': 2,
                'Março': 3,
                'Abril': 4, 
                'Maio': 5,
                'Junho': 6,
                'Julho': 7,
                'Agosto': 8,
                'Setembro': 9,
                'Outubro': 10,
                'Novembro': 11,
                'Dezembro': 12
               }
    
    return dict_mes[x]