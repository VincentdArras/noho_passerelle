# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:57:11 2023
Version 1.3
@author: Vincent d'Arras
"""
"""++++++++++importation bibliotheque++++++++++"""
import datetime
import pandas                                                           #pour trier les csv
from ftplib import FTP                                                  #pour communication avec serveur ftp
#import csv

dateheure = str(datetime.datetime.now())                                #variable global horodatage de l'execution

"""++++++++++definition chemin d'acces document++++++++++"""
path = "D:\\Passerellepy\\"                                             #chemin pour serveur
#path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\"        #chemin test vincent

"""++++++++++connection au serveur ftp++++++++++"""
ftp = FTP('ftp0.aquitem.fr')                                            #adrrese du ftp
ftp.login('nohoWeb', 'nohoWeb2022!')                                    #login

"""++++++++++lecture et ecriture des references et commandes depuis le ftp++++++++++"""
def lecture_ftp():
    with open(path + "Py\\Lecture_ExportCSV.csv", 'wb') as fic_export_ftp:
        ftp.retrbinary('RETR /Export/ExportCSV.csv', fic_export_ftp.write)     #copie les données du fichier dans le ftp dans un fichier plus proche
    fic_export_ftp.close()
    
    with open(path + "Py\\Lecture_ftp.csv", 'wb') as fic_orders_ftp:
        ftp.retrbinary('RETR exported_orders_prestashop.csv', fic_orders_ftp.write)     #copie les données du fichier dans le ftp dans un fichier plus proche
    fic_orders_ftp.close()
    return None

"""++++++++++ecriture bon cadeau++++++++++"""
def ecriture_baw():
    with open(path + 'Py\\Lecture_ExportCSV.csv','a+',encoding= 'ISO-8859-1') as ExportCSV:     #ecriture des bon dans le fichier pour eviter les erreurs
        ExportCSV.write("NOHO;BAW;050321432;1;;;;;;;;;;;;;0;;;;;;;;;30.00;30.00;0;0;0;0\n")     #bon 30€
        ExportCSV.write("NOHO;BAW;050321433;1;;;;;;;;;;;;;0;;;;;;;;;50.00;50.00;0;0;0;0\n")     #bon 50€
        ExportCSV.write("NOHO;BAW;050321434;1;;;;;;;;;;;;;0;;;;;;;;;75.00;75.00;0;0;0;0\n")     #bon 75€
        ExportCSV.write("NOHO;BAW;050321435;1;;;;;;;;;;;;;0;;;;;;;;;100.00;100.00;0;0;0;0\n")   #bon 100€
        ExportCSV.write("NOHO;BAW;050321436;1;;;;;;;;;;;;;0;;;;;;;;;150.00;150.00;0;0;0;0\n")   #bon 150€
        ExportCSV.write("NOHO;BAW;050321437;1;;;;;;;;;;;;;0;;;;;;;;;200.00;200.00;0;0;0;0\n")   #bon 200€
        ExportCSV.write("NOHO;BAW;050321438;1;;;;;;;;;;;;;0;;;;;;;;;300.00;300.00;0;0;0;0\n")   #bon 300€
        ExportCSV.write("NOHO;BAW;050321439;1;;;;;;;;;;;;;0;;;;;;;;;400.00;400.00;0;0;0;0\n")   #bon 400€
        ExportCSV.write("NOHO;BAW;050321440;1;;;;;;;;;;;;;0;;;;;;;;;500.00;500.00;0;0;0;0\n")   #bon 500€
        ExportCSV.write("NOHO;BAW;050321441;1;;;;;;;;;;;;;0;;;;;;;;;0.01;0.01;0;0;0;0\n")       #bon 0€
    ExportCSV.close()
    return None

"""++++++++++reecriture des commandes sans erreurs++++++++++"""
def maj_forme_com():
    with open(path+"Py\\Lecture_ftp.csv",'r',encoding='UTF-8') as fic:
        with open(path +"Py\\Commande_en_traitement.csv",'w',encoding= 'UTF-8') as fic2:
            ligne = fic.readline()                                      #ligne prend la valeur d'une ligne du fichier
            fic2.write(ligne)                                           #récupère la première ligne(important pour le sort)
        
            #print(len(ligne))
            while len(ligne) != 0:                                      #boucle jusqu'à la fin du fichier
                ligne = fic.readline()                                  #ligne prend la valeur d'une ligne du fichier
                if len(ligne) == 0:                                     #2eme check de fin de fichier
                    break
                #print("*",ligne)
                #print(ligne[len(ligne)-2])
                while ligne[len(ligne)-2].isdigit()==False :            #verifie que la derniere valeur soit un chiffre sinon ajoute la ligne suivante
                    #print(ligne[len(ligne)-2])
                    ligne = ligne[:len(ligne)-1]+" " + fic.readline()
                #print(type(ligne))
                fic2.write(ligne)                                       #ecrie la ligne complete dans le fichier
                #print("\n +",ligne)
    fic.close()
    fic2.close()
    
    #Tri les data par numero de facture en ordre decroissant
    data = pandas.read_csv(path +"Py\\Commande_en_traitement.csv",sep ='|', dtype="string")
    data = data.sort_values(by=['Numéro de facture'], ascending=False)
    data.to_csv(path +"Py\\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')
    return None

"""++++++++++lecture de la dernière commande++++++++++"""
def gestion_commande():
    with open(path +"Py\\last_order.txt", 'r') as fic_lor:              #lecture .txt
        last_order = int(fic_lor.readline())                            #enregistrement derniere commande dans une variable
    fic_lor.close()
    
    """++++++++++verification de la dernière commande et ecriture sur fichier++++++++++"""
    with open(path +"Py\\Commande_en_traitement.csv",'r',encoding= 'UTF-8') as fic_order:
        fic_order.readline()
        ligne = fic_order.readline()
        #print(type(ligne), ligne[3:9])
        if int(ligne[3:9]) != last_order:                               #si la derniere commande du fichier est differente de la derniere enregistre
            print("Commande non traité")                                #commande non traite donc essaye de mettre a 0 les produits pendant 30 minutes
            trace.write("\nCommande non traité")
            liste_ref = []
            while (int(ligne[3:9]) != last_order):                      #recupere les gencods des produits commandes
                liste_com = ligne.split(sep = '|')
                if liste_com[25] != '':                                 #enleve les gencods vide (bon cadeau)
                    liste_ref.append(liste_com[25])
                ligne = fic_order.readline()
            #print(liste_ref)                                           #liste_ref contient tous les produits
            
            """++++++++++cherche les produits++++++++++"""
            with open(path +"Py\\Lecture_ExportCSV.csv",'r',encoding= 'ISO-8859-1') as fic_export1:
                with open(path +"Py\\ExportCSV_en_traitement.csv",'w',encoding= 'ISO-8859-1') as fic_export2:
                    ligne_export = fic_export1.readline()               #lecture fichier export de base dans une variable
                    ligne_export2 = fic_export1.readline()              #lecture fichier export de base dans une autre variable
                    fic_export2.write(ligne_export)                     #reecriture 1ere ligne
                    #print(ligne_export)
                    while len(ligne_export2) != 0 :
                        ligne_export = ligne_export2
                        ligne_export2 = fic_export1.readline()
                        liste_ligne = ligne_export.split(sep = ";")
                        #print(liste_ligne)
                        flag = False
                        for i in range(len(liste_ref)):
                            if len(liste_ligne) > 25:                       #bloque les erreurs d'export proshop
                                if liste_ligne[23] == liste_ref[i]:         #si le gencod est dans la liste des refs il le saute sinon il reecrit la ligne dans le fichier
                                    print("Produit trouvé", liste_ligne[23])
                                    trace.write("\nProduit retiré pendant 1 export " + str(liste_ligne[23]))
                                    flag = True
                        if flag == False and len(liste_ligne) > 25:
                            fic_export2.write(ligne_export)
    
            fic_export1.close()
            fic_export2.close()
            
            with open(path + 'Py\\ExportCSV_en_traitement.csv', 'rb') as fic_ftp_xml:       #copie les donnees du fichier modifie
                ftp.storbinary('STOR ' + "/Export/ExportCSVmod.csv", fic_ftp_xml)           #maj document sur le ftp
            fic_ftp_xml.close()
        else:
            trace.write("\nPas de commande en retard")
            with open(path + 'Py\\Lecture_ExportCSV.csv', 'rb') as fic_ftp_xml:             #copie les donnees du fichier de base
                ftp.storbinary('STOR ' + "/Export/ExportCSVmod.csv", fic_ftp_xml)           #maj document sur le ftp
            fic_ftp_xml.close()
    fic_order.close()
    return None

"""++++++++++global pour gestion des erreurs et du code entier++++++++++"""
with open(path+"Py\\Trace2.txt", "a") as trace:                         #ouvre le document trace qui permet un suivi des executions
    trace.write("\n\n***Export du "+str(datetime.datetime.now()))       #ecrit la date et l'heure d'execution dans le trace
  
    try:                                                                #execute sauf exeption
        lecture_ftp()                                                   #execute un programme qui copie les docs du ftp
        ecriture_baw()                                                  #execute un programme qui ajoute les bon cadeaux
        maj_forme_com()                                                 #execute un programme qui met à jour le fichier commande
        gestion_commande()                                              #execute un programme qui gère les commandes pas traiter et récris les données sur le ftp
        ftp.quit()                                                      #ferme la liaison au ftp
        trace.write("\nExport terminé")                                 #balise la fin du processus dans le fichier trace
        
    except Exception as e:                                              #exeption si erreur
        ftp.quit()                                                      #ferme la liaison au ftp
        print('Error occurred : ' + str(e))
        trace.write('\nError occurred : ' + str(e))                     #reporte la ou les erreurs dans le fichier trace
