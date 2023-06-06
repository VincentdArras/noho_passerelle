# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:57:11 2023
Version 1.1
@author: Vincent
"""
"""++++++++++importation bibliotheque++++++++++"""
#import datetime
from ftplib import FTP                                                  #pour communication avec serveur ftp
#import csv

#dateheure = str(datetime.datetime.now())                                #variable global horodatage de l'execution

"""++++++++++definition chemin d'acces document++++++++++"""
path = "D:\\Proshop\\Passerellepy\\"                                    #chemin pour serveur
#path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\"        #chemin test vincent

"""++++++++++connection au serveur ftp++++++++++"""
ftp = FTP('ftp0.aquitem.fr')                                            #adrrese du ftp
ftp.login('nohoWeb', 'nohoWeb2022!')                                    #login

"""++++++++++lecture et ecriture des references et commandes++++++++++"""
with open(path + "Py\\Lecture_ExportCSV.csv", 'wb') as fic_export_ftp:
    ftp.retrbinary('RETR /Export/ExportCSV.csv', fic_export_ftp.write)     #copie les données du fichier dans le ftp dans un fichier plus proche
fic_export_ftp.close()

"""++++++++++ecriture bon cadeau++++++++++"""
with open(path + 'Py\\Lecture_ExportCSV.csv','a+',encoding= 'ISO-8859-1') as ExportCSV:
    ExportCSV.write("NOHO;BAW;050321432;1;;;;;;;;;;;;;0;;;;;;;;;30.00;30.00;0;0;0;0\n")       #bon 30€
    ExportCSV.write("NOHO;BAW;050321433;1;;;;;;;;;;;;;0;;;;;;;;;50.00;50.00;0;0;0;0\n")       #bon 50€
    ExportCSV.write("NOHO;BAW;050321434;1;;;;;;;;;;;;;0;;;;;;;;;75.00;75.00;0;0;0;0\n")       #bon 75€
    ExportCSV.write("NOHO;BAW;050321435;1;;;;;;;;;;;;;0;;;;;;;;;100.00;100.00;0;0;0;0\n")     #bon 100€
    ExportCSV.write("NOHO;BAW;050321436;1;;;;;;;;;;;;;0;;;;;;;;;150.00;150.00;0;0;0;0\n")     #bon 150€
    ExportCSV.write("NOHO;BAW;050321437;1;;;;;;;;;;;;;0;;;;;;;;;200.00;200.00;0;0;0;0\n")     #bon 200€
    ExportCSV.write("NOHO;BAW;050321438;1;;;;;;;;;;;;;0;;;;;;;;;300.00;300.00;0;0;0;0\n")     #bon 300€
    ExportCSV.write("NOHO;BAW;050321439;1;;;;;;;;;;;;;0;;;;;;;;;400.00;400.00;0;0;0;0\n")     #bon 400€
    ExportCSV.write("NOHO;BAW;050321440;1;;;;;;;;;;;;;0;;;;;;;;;500.00;500.00;0;0;0;0\n")     #bon 500€
    ExportCSV.write("NOHO;BAW;050321441;1;;;;;;;;;;;;;0;;;;;;;;;0.01;0.01;0;0;0;0\n")         #bon 0€
ExportCSV.close()

with open(path + 'Py\\Lecture_ExportCSV.csv', 'rb') as fic_ftp_xml:               #creer le document a importer pour le ftp
    ftp.storbinary('STOR ' + "/Export/ExportCSVmod.csv", fic_ftp_xml)
fic_ftp_xml.close()

ftp.quit()


