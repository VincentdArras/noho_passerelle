# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 10:07:33 2022

@author: Vincent
"""

def lire_csv():
    liste_info = []
    fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Vincent\\request_sql_5 (4).csv",'r',encoding='UTF-8')
    fic.readline()
    ind1 = 0
    ind2 = -1
    for i in range(70):
        ligne = fic.readline()
        while ligne[len(ligne)-2].isdigit()==False :
            ligne= ligne + fic.readline()
        print("\n\n",ligne)
        liste_info = []
        ind1=0
        ind2=-1
        while len(liste_info) < 25 :
            if ligne[ind1] == ';':
                liste_info.append(ligne[ind2+1:ind1])
                ind2=ind1
            ind1 = ind1 + 1
        print(liste_info)
    
    return liste_info

lire_csv()