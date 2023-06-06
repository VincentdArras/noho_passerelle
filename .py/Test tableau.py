# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:04:22 2022

@author: Vincent
"""
import pandas
import os
import datetime
"""
fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders11.csv",'r',encoding='UTF-8')
fic2 = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders.csv",'w',encoding='UTF-8')

ligne = fic.readline()
fic2.write(ligne)                              #récupère la première ligne(important pour le sort)

#print(len(ligne))
while len(ligne) != 0:
    ligne = fic.readline()
    if len(ligne) == 0:
        break
    print("*",ligne)
    print(ligne[len(ligne)-3])
    while ligne[len(ligne)-3].isdigit()==False :
        #print(ligne[len(ligne)-2])
        ligne = ligne[:len(ligne)-2]+ " " + fic.readline()
    #print(type(ligne))
    fic2.write(ligne)
    #print("\n\n +",ligne)

 
fic.close()
fic2.close()
data = pandas.read_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders.csv",sep ='|', dtype="string")

data = data.sort_values(by=['Numéro de facture'], ascending=True)

#print(data)
data.to_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders11 - Copie.csv", index=False, encoding='UTF-8', sep ='|')


dateheure = str(datetime.datetime.now())
date_proshop = dateheure[:10]+'T'+dateheure[11:19]
date_export = date_proshop[0:4] + date_proshop[5:7] + date_proshop[8:10] + date_proshop[11:13] + date_proshop[14:16] + date_proshop[17:19]

#deplacer du rep 1 vers rep 2 en changeant le chemin// changer le nom est possible en meme temps
doca_traiter = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders11 - Copie.csv"
doc_traiter = "C:\\Users\\Vincent\\Desktop\\Entreprise\\exported_orders"+date_export+".csv"
os.rename(doca_traiter, doc_traiter)
"""
fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders12.csv",'r',encoding='UTF-8')
fic2 = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\Commande_en_traitement.csv",'w',encoding='UTF-8')

ligne = fic.readline()
fic2.write(ligne)                              #récupère la première ligne(important pour le sort)

#print(len(ligne))
while len(ligne) != 0:
    ligne = fic.readline()
    if len(ligne) == 0:
        break
    #print("*",ligne)
    #print(ligne[len(ligne)-2])
    while ligne[len(ligne)-2].isdigit()==False :
        #print(ligne[len(ligne)-2])
        ligne = ligne[:len(ligne)-1]+ " " + fic.readline()
    #print(type(ligne))
    fic2.write(ligne)
    #print("\n\n +",ligne)

 
fic.close()
fic2.close()

data = pandas.read_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\Commande_en_traitement.csv",sep ='|', dtype="string")
data = data.sort_values(by=['Numéro de facture'], ascending=True)
#print(data)
data.to_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')

data = pandas.read_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\Commande_en_traitement.csv",sep ='|', dtype="string")
data = data.sort_values(by=['Credit Slip Number'], ascending=False)
#print(data)
data.to_csv("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')