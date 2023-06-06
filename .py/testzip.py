# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:16:27 2023

@author: Vincent
"""

import os
import zipfile
import datetime

path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\"

"""dateheure = str(datetime.datetime.now())                                #variable global horodatage de l'execution
date_export = dateheure[0:4] + dateheure[5:7] + dateheure[8:10] +"_"+ dateheure[11:13] + dateheure[14:16] + dateheure[17:19]    #format de la date pour le nom du fichier

path_T1 = path + "Py\\Trace1.txt"
path_T2 = path + "Py\\Trace2.txt"

file_size_T1 = os.path.getsize(path_T1)                   #verifie la taille, attention au path
file_size_T2 = os.path.getsize(path_T2)                   #verifie la taille, attention au path

name_T1 = "Trace1_"+date_export+".txt"
name_T2 = "Trace2_"+date_export+".txt"
print(file_size_T1, file_size_T2)"""
"""if file_size_T1 > 300000 or file_size_T2 > 300000:
    output_path = os.path.join(path+"Py\\ArchiveTrace.zip")             #chemin d'acces pour archive en zip
    with zipfile.ZipFile(output_path, 'a', zipfile.ZIP_DEFLATED) as myzip:                #enregistrement dans un zip
        myzip.write(path_T1, os.path.basename(name_T1))
        myzip.write(path_T2, os.path.basename(name_T2))
    with open(path+"Py\\Trace1.txt", "w") as trace1:
        trace1.write("Début du fichier (vérifier ArchiveTrace pour données antérieurs)")
    trace1.close()
    with open(path+"Py\\Trace2.txt", "w") as trace2:
        trace2.write("Début du fichier (vérifier ArchiveTrace pour données antérieurs)")
    trace2.close()"""
    
"""output_path = os.path.join(path+"ArchiveExportTest.zip")             #chemin d'acces pour archive en zip
path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\1\\"
with zipfile.ZipFile(output_path, 'a', zipfile.ZIP_DEFLATED) as myzip:                #enregistrement dans un zip
    for i in range(72):
        t = path+str(i)+".xml"
        myzip.write(t, os.path.basename(str(i)+".xml"))"""
        
zoe = '4.900000'
car = 4.9500-float(zoe)
print(car)

if car !=0:
    print("ahah")
