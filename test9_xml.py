# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:49:17 2022
Version 1.1
@author: Vincent d'Arras
"""
#input()                                                                #pour test en exe
"""++++++++++importation bibliotheque++++++++++"""
import datetime
from lxml import etree                                                  #pour creer les arbres xml
import pandas                                                           #pour trier les csv
import os, sys
import zipfile
from ftplib import FTP                                                  #pour communication avec serveur ftp

dateheure = str(datetime.datetime.now())                                #variable global horodatage de l'execution

"""++++++++++definition chemin d'acces document++++++++++"""
path = "D:\\Passerellepy\\"                                             #chemin pour serveur
#path = "D:\\Entreprise\\Passerelle\\Passerellepy\\"                    #chemin pour test

"""++++++++++connection au serveur ftp++++++++++"""
ftp = FTP('ftp0.aquitem.fr')                                            #adrrese du ftp
ftp.login('nohoWeb', 'nohoWeb2022!')                                    #login

"""++++++++++lecture et ecriture des commandes++++++++++"""
with open(path + "Py\\Lecture_ftp.csv", 'wb') as fic_orders_ftp:
    ftp.retrbinary('RETR exported_orders_prestashop.csv', fic_orders_ftp.write)     #copie les données du fichier dans le ftp dans un fichier plus proche
fic_orders_ftp.close()


"""++++++++++mise en forme du csv pour lire les retours++++++++++"""
def maj_forme_retour():
    data = pandas.read_csv(path +"Py\\Commande_en_traitement.csv",sep ='|', dtype="string")     
    data = data.sort_values(by=['Credit Slip Number'], ascending=False) #tri les data par numéro de retour décroissant
    #print(data)
    data.to_csv(path+"Py\\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')

    return None
"""++++++++++mise en forme du csv pour lire les commandes++++++++++"""
"""Commandes triées par numéro de facture croissant, lecture et récriture dans un autre .csv, mise en forme en cas d'erreur"""
def maj_forme_commande():
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
    
    #Tri les data par numero de facture en ordre croissant
    data = pandas.read_csv(path +"Py\\Commande_en_traitement.csv",sep ='|', dtype="string")
    data = data.sort_values(by=['Numéro de facture'], ascending=True)
    #print(data)
    data.to_csv(path +"Py\\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')
    return None                                                         #ne retourne rien(la data est le fichier)

"""++++++++++prise en compte des articles bon achat++++++++++"""
def BAW(produits,liste_info):
    article = etree.SubElement(produits,"article")                      #creation d'un article bon cadeau
    article.set("libelle",str(liste_info[13]))                          
    type1 = etree.SubElement(article,"type")                            #type pour choisir entre vente, retour, prestation...
    type1.text = "R"
    
    gencod = etree.SubElement(article,"gencod")
    gencod.text = "BBAW"                                                #BBAW car premier caractere retire par Proshop
    taille = etree.SubElement(article,"taille")
    taille.text = ""
    
    pvttc= etree.SubElement(article,"pvttc")
    pvttc.text = liste_info[16]
    quantite= etree.SubElement(article,"quantite")
    quantite.text = liste_info[14]
    
    return None

"""++++++++++verification de la derniere commande et du dernier retour traite++++++++++"""
def order_limit():
    #last_order = 0
    with open(path +"Py\\last_order.txt", 'r') as fic_lor:              #lecture du  .txt
        last_order = int(fic_lor.readline())                            #enregistrement derniere commande dans une variable
        last_return = int(fic_lor.readline())                           #enregistrement dernier retour dans une variable
    fic_lor.close()
    #print(last_order,type(last_order))
    return last_order,last_return                                       #retourne les 2 donnees

"""++++++++++fonction pour reecrire la derniere commande et du dernier retour traite++++++++++"""
def rewrite_LO(last_o, last_r):
    with open(path +"Py\\last_order.txt", 'w') as fic_low:              #ouverture .txt en ecriture
        fic_low.write(str(last_o)+"\n")                                 #ecriture derniere commande dans le fichier
        fic_low.write(str(last_r))                                      #ecriture dernier retour dans le fichier 
    fic_low.close()
    print("Done Rewriting!")
    trace.write("\nRéecritre terminée")                                 #ecriture dans le fichier trace
    return None

"""++++++++++fonction pour lire les lignes du csv et les enregister dans une liste++++++++++"""
def lire_csv(fic):
    liste_info = []                                                     #cree une liste vide
    ind1 = 0                                                            #variable incrementation
    ind2 = -1                                                           #variable incrementation
    ligne = fic.readline()
    if len(ligne) == 0:                                                 #retourne une liste vide si derniere ligne du fichier
        return liste_info 
    #print("\n\n 1",ligne)

    while ind1 < len(ligne) :#len(liste_info) < 34 :                    #boucle jusqu'a la fin de la ligne
        if ligne[ind1] == '|':                                          #separe les donnees a chaque |
            liste_info.append(ligne[ind2+1:ind1])                       #ajoute une la donnee dans la liste
            ind2 = ind1
        ind1 = ind1 + 1
    liste_info.append(ligne[ind2+1:len(ligne)-1])                       #ajoute la derniere donnee dans la liste
    
    """ Correction des espaces fantomes
    for i in range(15):
        if liste_info[i][len(liste_info[i])-1] == ' ':
            liste_info[i] = liste_info[i][:len(liste_info[i])-1]
        if liste_info[i][0] == ' ':
            liste_info[i] = liste_info[i][1:]
     """   
    
    """algo pour recuperer un numero de telephone, verifie si case != de vide et priorise les mobiles"""
    choix_tel = 0
    if liste_info[24] != '':
        choix_tel = 24
        #print("24")
    if liste_info[22] != '':
        choix_tel = 22
        #print("22")
    if liste_info[23] != '':
        choix_tel = 23
        #print("23")
    if liste_info[21] != '':
        choix_tel = 21
        #print("21")
        
    if choix_tel != 0 :                                                 #enrrgistre un numero dans la liste
        liste_info[21] = liste_info[choix_tel]
    del liste_info[24]                                                  #supprime les autres cases
    del liste_info[23]                                                  #supprime les autres cases
    del liste_info[22]                                                  #supprime les autres cases
    
    
    if liste_info[13] == "":                                            #au cas ou le libelle est vide
        liste_info[13] = "00"
    
    """gestion des tailles car l'export creer plusieurs cases"""
    while liste_info[24] != "ZZ":                                       #boucle jusqu'a la case ZZ
        if liste_info[24] != "":                                        #valide si la case n'est pas vide
            liste_info[23] = liste_info[24]
        del liste_info[24]                                              #supprime la derniere case traite
    del liste_info[24]                                                  #supprime le marqueur ZZ
    
    if liste_info[23] != "":                                            #supprime les doubles ecriture de taille dans la case
        for ta in range(len(liste_info[23])):
            if liste_info[23][ta] == ",":
                liste_info[23] = liste_info[23][:ta]
                break
    else :                                                              #si pas de taille : ecrit TU
        liste_info[23] = "TU"
    #print("\n 2",liste_info, sep='')
    return liste_info                                                   #retourne une liste

"""++++++++++fonction pour valider la forme du .xml avec celle demandee par proshop++++++++++"""
def validate_xml(ficxml):
    flag = False
    theDtd = path +"Py\\ProshopVente.dtd"                               #le fichier sur lequel verifier
    #parser = etree.XMLParser(dtd_validation=True)
    with open(theDtd) as opendtd :
        dtd = etree.DTD(opendtd)                                        #lit le .dtd
        tree = etree.parse(ficxml)                                      #lit notre .xml pour avoir un arbre
    
        valid = dtd.validate(tree)                                      #verifie la validite de notre arbre
        if (valid):
            print("XML is valid!")                                      #si il est valide, rentre ici
            flag = True
    
        else:                                                           #sion rentre ici, print les erreurs, et les ecrit dans trace
            print("\n\nXML isn't valid")
            print(dtd.error_log.filter_from_errors())
            trace.write("\nXML isn't valid"+dtd.error_log.filter_from_errors())
            flag = False
    opendtd.close()
    return flag

"""++++++++++fonction pour creer l'arbre des commandes en .xml"""
def creatree_order():
    maj_forme_commande()                                                #appelle la fonction pour mettre en ordre le .csv
    with open(path +"Py\\Commande_en_traitement.csv",'r',encoding='UTF-8') as fic:  #ouvre le fichier .csv
    #fic = open(path +"Py\\Commande_en_traitement.csv",'r',encoding='UTF-8')
        fic.readline()                                                  #passe la premiere ligne
        flagfin = False
        #dateheure = str(datetime.datetime.now())                        #recupere l'heure actuel grace a une bibliotheque
        date_proshop = dateheure[:10]+'T'+dateheure[11:19]              #mise en forme date pour proshop
        date_traiter = dateheure[:10]                                   #mise en forme date pour commandes
        
        liste_infom1 = ['']                                             #creer une liste -1
        liste_info = ['']                                               #creer une liste 0
        liste_info2 = lire_csv(fic)                                     #creer une liste 2 qui prend la valeur d'une ligne du fichier
        
        last_ord = int(order_limit()[0])                                #lit la valeur de la derniere commande traitee
        while int(liste_info2[0][3:]) <= last_ord or liste_info2[31].find("Bon cadeau Noho") != -1:     #boucle tant qu'il s'agit de vieilles commandes ou payees avec bon
            liste_info = liste_info2                                    #liste 0 prend la valeur de la liste 1
            liste_info2 = lire_csv(fic)                                 #liste 1 prend la valeur de la ligne suivante
            if len(liste_info2) == 0:                                   #si la derniere ligne est atteinte, il n'y a pas de commande a traiter
                print("No order to import")
                trace.write("\nPas de commande à importer")
                return None, liste_info[0][3:]                          #si pas de commande stop la fonction ici
            
        #print(liste_info2)
        #date_traiter = liste_info2[7][:10]
        """debut de la creation de l'arbre"""
        proshop = etree.Element("proshop")                              #premiere racine
        proshop.set("datesysteme", date_proshop)                        #date et heure de traitement
        
        while flagfin == False :                                        #boucle jusqu'a indication
            liste_infom1 = liste_info
            liste_info = liste_info2                                    #modification des listes -1, 0 et 1
            liste_info2 = lire_csv(fic)
            #print(liste_info)
            #print(liste_info2)
            
            if (liste_info[31].find("Bon cadeau Noho") != -1            #verifie si bon cadeau en moyen de reglement, si il trouve "Bon cadeau Noho" il renvoie son emplacement (0,1,...) sinon il revoie -1
                    or liste_info[31].find("BCAM") != -1                #verifie si bon cadeau magasin transformé en moyen de reglement, si il trouve "BCAM" il renvoie son emplacement (0,1,...) sinon il revoie -1
                    or liste_info[31].find("euros") != -1) :            #verifie si bon cadeau en moyen de reglement, si il trouve "euros" il renvoie son emplacement (0,1,...) sinon il revoie -1
                #print(liste_info)
                if len(liste_info2) == 0:                               #verifie si la ligne actuel est la derniere du fichier
                    liste_info2.append(0)
                    flagfin = True
            else:
                if liste_info[7][:10] == date_traiter and 'ventes' in locals() :   #verifie si le sous element vente existe deja et si la date traitee est celle de la commande
                    pass
                #print(date_traiter)
                else :                                                      #sinon change la date ou creer le sous element
                    date_traiter = liste_info[7][:10]
                    ventes = etree.SubElement(proshop,"ventes")
                    ventes.set("date",date_traiter)                         #date de creation de la facture de la commande
                    ventes.set("magasin","008")                             #magasin toujours a 008 car ventes web
                    #print(date_traiter)
                
                if liste_info[0] != liste_infom1[0]:                        #si la ligne ne correspond pas a la meme commande que la ligne precedente
                    ticket = etree.SubElement(ventes,"ticket")              #un ticket correspond a une commande
                    ticket.set("numero",liste_info[0][3:])                  #numero de la facture sans le #FA
                    ticket.set("heure",liste_info[7][11:])                  #heure de creation de la facture de la commande
                    
                    last_order_process = int(liste_info[0][3:])             #enregistre le numero de la derniere commande traitee
                
                    client = etree.SubElement(ticket,"client")              #donnee du client
                    code = etree.SubElement(client,"code")
                    code.text = liste_info[2]
                    nom = etree.SubElement(client,"nom")
                    nom.text = liste_info[10]
                    prenom = etree.SubElement(client,"prenom")
                    prenom.text = liste_info[9]
                    adresse1 = etree.SubElement(client,"adresse1")
                    adresse1.text = liste_info[17]
                    if liste_info[18] != '' :                               #si l'adresse2 est vide, pas de sous element cree
                        adresse2 = etree.SubElement(client,"adresse2")
                        adresse2.text = liste_info[18]
                    codepostal = etree.SubElement(client,"codepostal")
                    codepostal.text = liste_info[19]
                    ville = etree.SubElement(client,"ville")
                    ville.text = liste_info[20]
                    if liste_info[21] != '':                                #si le numero de telephone est vide, pas de sous element cree
                        telephone = etree.SubElement(client,"telephone")
                        telephone.text = liste_info[21]
                    email = etree.SubElement(client,"email")
                    email.text = liste_info[11]
                        
                        
                    produits = etree.SubElement(ticket,"produits")          #creation du sous elemnt produits qui prendra les articles
                    if int(liste_info[12]) >= 50321432 and int(liste_info[12]) <= 50321441:  #verifie s'il s'agit d'un bon cadeau
                        BAW(produits,liste_info)                            #si bon cadeau revoie vers la fonction BAW
                        
                    else :                                                  #sinon creer un article normal
                        article = etree.SubElement(produits,"article")  
                        article.set("libelle",str(liste_info[13]))
                        type1 = etree.SubElement(article,"type")            #type pour choisir entre vente, retour, prestation...
                        type1.text = "V"
                        
                        gencod = etree.SubElement(article,"gencod")         #gencod complet necessaire
                        if liste_info[22] != '':                            #si gencod complet il l'utilise(13)
                            gencod.text = liste_info[22]
                        else:                                               #sinon bricolage sans taille et clef(10)
                            gencod.text = "900" + liste_info[12]
                        
                        taille = etree.SubElement(article,"taille")
                        taille.text = liste_info[23]
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[16]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[14]
                    
                elif liste_infom1[0] == liste_info[0]:                      #si la ligne correspond a la meme commande que la ligne precedente
                    if int(liste_info[12]) >= 50321432 and int(liste_info[12]) <= 50321441:     #verifie s'il s'agit d'un bon cadeau
                        BAW(produits,liste_info)                            #si bon cadeau revoie vers la fonction BAW
                        
                    else :                                                  #sinon creer un article normal
                        article = etree.SubElement(produits,"article")
                        article.set("libelle",str(liste_info[13]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "V"                                    #type pour choisir entre vente, retour, prestation...
                            
                        gencod = etree.SubElement(article,"gencod")         #gencod complet necessaire
                        if liste_info[22] != '':                            #si gencod complet il l'utilise(13)
                            gencod.text = liste_info[22]
                        else:                                               #sinon bricolage sans taille et clef(10)
                            gencod.text = "900" + liste_info[12]
                         
                        taille = etree.SubElement(article,"taille")
                        taille.text = liste_info[23]
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[16]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[14]
                
                if len(liste_info2) == 0:                                   #verifie si la ligne actuel est la derniere du fichier
                    liste_info2.append(0)
                    flagfin = True
                    #print(liste_info2)
                    
                if liste_info[0] != liste_info2[0]:                         #si la ligne ne correspond pas a la meme commande que la ligne suivante
                    """Ajout des frais de livraison si necessaire"""
                    #if liste_info[6] != '0.000000':                        #si le string est different de 0.000000 il ajoute la prestation transport
                    #print("Livraison +",liste_info[30],"+",liste_info[30][0:4],"+",sep="")
                    if liste_info[30] != "" and liste_info[30][0:4] != "NOHO":#ajout de la livraison meme si nul pour les relais pickup
                        article = etree.SubElement(produits,"article")
                        article.set("libelle","Transport")
                        type1 = etree.SubElement(article,"type")
                        type1.text = "R"                                    #type pour choisir entre vente(V), retour(I), prestation(R)...
                        gencod = etree.SubElement(article,"gencod")
                        gencod.text = "TTRA"                                #TTRA car premier caractere retire par Proshop
                        taille = etree.SubElement(article,"taille")
                        if liste_info[30] == "Livraison en relais Pickup":  #separe la livraison en relais qui est devenue gratuite
                            prht = etree.SubElement(article,"prht")
                            prht.text = '4.950000'
                            pvttc = etree.SubElement(article,"pvttc")
                            pvttc.text = liste_info[6]
                            if (4.9500 - float(liste_info[6])) != 0:                #n'ajoute rien si le même prix
                                remise = etree.SubElement(article,"remise")
                                remise.text = str(4.9500 - float(liste_info[6]))
                        else:
                            pvttc = etree.SubElement(article,"pvttc")
                            pvttc.text = liste_info[6]
                        #Fin_Livraison
                            
                    reglements = etree.SubElement(ticket,"reglements")      #sous element de la commande, le reglement
                    mode = etree.SubElement(reglements,"mode")
                    code = etree.SubElement(mode,"code")                    #algo pour definir le mode de paiement
                    code_v = ''
                    #print("+",liste_info[4],"+", sep="")
                    if liste_info[4] == 'PayPal':
                        code_v = 'PAY'
                    elif liste_info[4] == 'Paiement par carte bancaire' or liste_info[4] == 'Credit Card' or liste_info[4] == 'Systempay':
                        code_v = 'CB'
                    elif liste_info[4] == 'Alma - Paiement en 2 fois' or liste_info[4] == 'Alma - Paiement en 3 fois' or liste_info[4] == 'Alma - Paiement en 4 fois':
                        code_v = 'ALM'
                    elif liste_info[4] == 'Apple Pay':
                        code_v = 'APP'
                    elif liste_info[4] == 'Google Pay':
                        code_v = 'GOO'
                    elif liste_info[4] == 'Paiement avec Choozeo sans frais' :
                        code_v = 'CHO'
                    else:
                        code_v = 'ESP'                                      #si aucun des cas ci-dessus, met 'ESP'
                    #print(code_v)
                    code.text = code_v
                    montant = etree.SubElement(mode,"montant")
                    montant.text = liste_info[5]
    
    fic.close()
    return proshop, last_order_process                                  #retourne la racine initiale et la derniere commande traiter

"""++++++++++fonction pour creer l'arbre des retours en .xml (peut être complementaire ou pas des commandes)++++++++++"""
def creatree_return(proshop):
    maj_forme_retour()                                                  #appelle la fonction pour mettre en ordre le .csv
    with open(path +"Py\\Commande_en_traitement.csv",'r',encoding='UTF-8') as fic_retour:   #ouvre le fichier .csv après sa mise en forme
        fic_retour.readline()                                           #lecture de la premiere ligne
        flag_retour = True
        
        date_traiter = ""                                               
        #dateheure = str(datetime.datetime.now())                        #recupere l'heure actuel grace a une bibliotheque
        date_proshop = dateheure[:10]+'T'+dateheure[11:19]              #mise en forme date pour proshop
        
        limites = order_limit()[1]                                      #variable pour le dernier retour traite
        liste_retour = ['']
        liste_retour2 = lire_csv(fic_retour)
        #print("1",liste_retour2[30])
        last_return = liste_retour2[25]                                 #variable pour le dernier retour du .csv
        if int(liste_retour2[25]) <= limites :                          #si pas de retour a traiter       
            flag_retour = False
            print("No return to import")
            trace.write("\nPas de retour à importer")
            return proshop, last_return
        elif int(liste_retour2[25]) > limites and proshop == None:      #s'il y a des retours a traiter et pas de commande(donc aucune racine definie)
            proshop = etree.Element("proshop")
            proshop.set("datesysteme", date_proshop)
        
        
        while flag_retour == True:                                      #boucle jusqu'a indication
            liste_retourm1 = liste_retour
            liste_retour = liste_retour2                                #modification des listes -1, 0 et 1
            liste_retour2 = lire_csv(fic_retour)
            #print(liste_retour)
            if int(liste_retour[25]) <= limites:                        #verifie si le retour est a traiter
                flag_retour = False
                break
            else:
                
                if liste_retour[13][1].isdigit() == True:               #retire les cartes cadeaux
                    pass
                else:
                    if liste_retour[27][:10] == date_traiter:           #verifie si la date du retour est celle de la vente
                        pass
                    else :
                        date_traiter = liste_retour[27][:10]
                        ventes = etree.SubElement(proshop,"ventes")
                        ventes.set("date",date_traiter)
                        ventes.set("magasin","008")
                        #print(date_traiter)
                    
                    if liste_retour[0] != liste_retourm1[0]:            #si la ligne ne correspond pas a la meme commande que la ligne precedente
                        ticket = etree.SubElement(ventes,"ticket")
                        ticket.set("numero",liste_retour[25])           #numero de facture de retour
                        ticket.set("heure",liste_retour[27][11:])       #heure de creation de la facture du retour
                        
                        client = etree.SubElement(ticket,"client")      #donnee du client
                        code = etree.SubElement(client,"code")
                        code.text = liste_retour[2]
                        nom = etree.SubElement(client,"nom")
                        nom.text = liste_retour[10]
                        prenom = etree.SubElement(client,"prenom")
                        prenom.text = liste_retour[9]
                        adresse1 = etree.SubElement(client,"adresse1")
                        adresse1.text = liste_retour[17]
                        if liste_retour[18] != '' :                     #si l'adresse2 est vide, pas de sous element cree
                            adresse2 = etree.SubElement(client,"adresse2")
                            adresse2.text = liste_retour[18]
                        codepostal = etree.SubElement(client,"codepostal")
                        codepostal.text = liste_retour[19]
                        ville = etree.SubElement(client,"ville")
                        ville.text = liste_retour[20]
                        if liste_retour[21] != '':                      #si ple telephone est vide, pas de sous element cree
                            telephone = etree.SubElement(client,"telephone")
                            telephone.text = liste_retour[21]
                        email = etree.SubElement(client,"email")
                        email.text = liste_retour[11]
                        produits = etree.SubElement(ticket,"produits")
                        
                        if liste_retour[28] !='0.000000':               #verifie si l'article de la commande est en retour
                            article = etree.SubElement(produits,"article")
                            article.set("libelle",str(liste_retour[13]))
                            type1 = etree.SubElement(article,"type")
                            type1.text = "I"                            #type pour choisir entre vente(V), retour(I), prestation(R)...
                            gencod = etree.SubElement(article,"gencod") #gencod complet necessaire
                            if liste_retour[22] != '':                  #si gencod complet il l'utilise(13)
                                gencod.text = liste_retour[22]
                            else:                                       #sinon bricolage sans taille et clef(10)
                                gencod.text = "900" + liste_retour[12]
                                
                            taille = etree.SubElement(article,"taille")
                            taille.text = liste_retour[23]
                            pvttc= etree.SubElement(article,"pvttc")
                            pvttc.text = "-"+liste_retour[28]           #(-)toujours necessaire pour les retours
                            quantite= etree.SubElement(article,"quantite")
                            quantite.text = liste_retour[26]
                        
                    elif liste_retourm1[0] == liste_retour[0] and liste_retour[28] !='0.000000' :  #si la ligne correspond a la meme commande que la ligne precedente et l'article est a retourner
                        #print("**",liste_retour)
                        article = etree.SubElement(produits,"article")
                        article.set("libelle",str(liste_retour[13]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "I"                                #type pour choisir entre vente(V), retour(I), prestation(R)...
                            
                        gencod = etree.SubElement(article,"gencod")     #gencod complet necessaire
                        if liste_retour[22] != '':                      #si gencod complet il l'utilise(13)
                            gencod.text = liste_retour[22]
                        else:                                           #sinon bricolage sans taille et clef(10)
                            gencod.text = "900" + liste_retour[12]
                         
                        taille = etree.SubElement(article,"taille")
                        taille.text = liste_retour[23]
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = "-"+liste_retour[28]               #(-)toujours necessaire pour les retours
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_retour[26]
                    
                    if liste_retour[0] != liste_retour2[0]:             #si la ligne ne correspond pas a la meme commande que la ligne suivante
                        """Ajout des frais de livraison si necessaire"""
                        if liste_retour[6] != '0.000000':               #si le string est different de 0.000000 il ajoute la prestation transport
                            article = etree.SubElement(produits,"article")
                            article.set("libelle","Transport")
                            type1 = etree.SubElement(article,"type")
                            type1.text = "R"                            #type pour choisir entre vente(V), retour(I), prestation(R)...
                            gencod = etree.SubElement(article,"gencod")
                            gencod.text = "TTRA"                        #TTRA car premier caractere retire par Proshop
                            taille = etree.SubElement(article,"taille")
                            pvttc= etree.SubElement(article,"pvttc")
                            pvttc.text = "-"+liste_retour[6]            #(-)necessaire car la prestation est remboursee
                            #Fin_Livraison
                                
                        reglements = etree.SubElement(ticket,"reglements")  #sous element de la commande, le reglement
                        mode = etree.SubElement(reglements,"mode")
                        code = etree.SubElement(mode,"code")            #algo pour definirle mode de paiement
                        code_v = ''
                        if liste_retour[4] == 'PayPal':
                            code_v = 'PAY'
                        elif liste_retour[4] == 'Paiement par carte bancaire' or liste_retour[4] == 'Credit Card' or liste_retour[4] == 'Systempay':
                            code_v = 'CB'
                        elif liste_retour[4] == 'Alma - Paiement en 2 fois' or liste_retour[4] == 'Alma - Paiement en 3 fois' or liste_retour[4] == 'Alma - Paiement en 4 fois':
                            code_v = 'ALM'
                        elif liste_retour[4] == 'Apple Pay':
                            code_v = 'APP'
                        elif liste_retour[4] == 'Google Pay':
                            code_v = 'GOO'
                        elif liste_retour[4] == 'Paiement avec Choozeo sans frais' :
                            code_v = 'CHO'
                        else:
                            code_v = 'ESP'                                      #si aucun des cas ci-dessus, met 'ESP'
                        code.text = code_v
                        montant = etree.SubElement(mode,"montant")
                        #montantret = -int(liste_retour[29].replace(".","."))
                        montant.text = str(-float(liste_retour[29])-float(liste_retour[6]))     #calcul du total en negatif car pas exportable par prestshop
  
    #print(liste_retour, limites)
    fic_retour.close()
    return proshop, last_return                                         #retourne l'arbre et le dernier retour traite pour reecriture

"""++++++++++fonction pour ecrire l'arbre complet dans un fichier, et le transferer au ftp++++++++++"""
def crea_xml(proshop):
    tree = etree.ElementTree(proshop)                                   #creer un arbre xml a partir de la racine proshop avec ses sous elements
    varxmltest = path +"Py\\Test.xml"                                   #chemin d'acces au fichier test pour l'arbre
    tree.write(varxmltest, xml_declaration=True, encoding='ISO-8859-1') #ecrit son arbre dans le fichier
    if validate_xml(varxmltest) == True:                                #valide l'arbre avec le dtd de proshop, si vrai continue
        date_export = dateheure[0:4] + dateheure[5:7] + dateheure[8:10] + dateheure[11:13] + dateheure[14:16] + dateheure[17:19]    #format de la date pour le nom du fichier
        varxml = path+"CommandesClientNoho." + date_export + ".xml"     #enregistrement temporaire
        with open (varxml, 'x', encoding='ISO-8859-1') as xml_doc:      #pour ecrire dans l'enregistrement temporaire
            tree.write(varxml, xml_declaration=True, encoding='ISO-8859-1')
        xml_doc.close()
        
        fic_name = "CommandesClientNoho." + date_export + ".xml"        #nom pour le fichier du ftp
        with open(path + fic_name , 'rb') as fic_ftp_xml:               #creer le document a importer pour le ftp
            ftp.storbinary('STOR ' + "/Import/"+str(fic_name), fic_ftp_xml)
        fic_ftp_xml.close()                                             #after chapitres 5 jennifer
        
        output_path = os.path.join(path+"ArchiveExport.zip")            #chemin d'acces pour archive en zip
        with zipfile.ZipFile(output_path, 'a', zipfile.ZIP_DEFLATED) as myzip:  #enregistrement dans un zip
            myzip.write(varxml, os.path.basename(varxml))
        os.remove(varxml)                                               #suppression du fichier temporaine maintenant dans les archives

    return None                                                         #ne retourne rien

"""++++++++++zip les dossiers trace quand trop volumineux++++++++++"""
def zip_trace():
    
    path_T1 = path + "Py\\Trace1.txt"                                   #creer une variable pour le chemin d'accès de Trace1
    path_T2 = path + "Py\\Trace2.txt"                                   #creer une variable pour le chemin d'accès de Trace2
    
    file_size_T1 = os.path.getsize(path_T1)                             #verifie la taille, attention au path
    file_size_T2 = os.path.getsize(path_T2)                             #verifie la taille, attention au path
    
    if file_size_T1 > 300000 or file_size_T2 > 300000:
        date_export_trace = dateheure[0:4]+dateheure[5:7]+dateheure[8:10]+"_"+dateheure[11:13]+dateheure[14:16]+dateheure[17:19]    #format de la date pour le nom du fichier
        name_T1 = "Trace1_"+date_export_trace+".txt"                    #creer une variable pour le nom du fichier archive
        name_T2 = "Trace2_"+date_export_trace+".txt"                    #creer une variable pour le nom du fichier archive
        output_path = os.path.join(path+"Py\\ArchiveTrace.zip")         #chemin d'acces pour archive en zip
        
        with zipfile.ZipFile(output_path, 'a', zipfile.ZIP_DEFLATED) as myzip:      #enregistrement dans un zip
            myzip.write(path_T1, os.path.basename(name_T1))
            myzip.write(path_T2, os.path.basename(name_T2))
        
        with open(path+"Py\\Trace1.txt", "w") as trace1:                #suppression des donnees dans le fichier non-zipper
            trace1.write("Début du fichier (vérifier ArchiveTrace pour données antérieurs)")
        trace1.close()
        with open(path+"Py\\Trace2.txt", "w") as trace2:                #suppression des donnees dans le fichier non-zipper
            trace2.write("Début du fichier (vérifier ArchiveTrace pour données antérieurs)")
        trace2.close()

    return None

"""++++++++++global pour gestion des erreurs et du code entier++++++++++"""
with open(path+"Py\\Trace1.txt", "a") as trace:                         #ouvre le document trace qui permet un suivi des executions
    trace.write("\n\n***Envoi du "+str(datetime.datetime.now()))        #ecrit la date et l'heure d'execution dans le trace
    try:                                                                #execute sauf exeption pas de fichier
        with open(path+"Py\\Lecture_ftp.csv"): pass
    except IOError:
        print("no file")
        trace.write("\nPas de fichier csv disponible pour l'export")
        sys.exit()
    
    try:                                                                #execute sauf exeption
        proshop1, last_order_process1 = creatree_order()                #execute le programme pour chercher de nouvelles commandes
        proshop2, last_return_process1 = creatree_return(proshop1)      #execute le programme pour chercher de nouveaux retours (avec la racine en parametre)
        if proshop2 != None:                                            #s'il y a une commande ou un retour a retourner
            crea_xml(proshop2)                                          #fonction pour creer l'arbre complet et les fichiers necessaire
            rewrite_LO(last_order_process1, last_return_process1)       #fonction pour reecrire les nouvelles variables
    
        ftp.quit()                                                      #ferme la liaison au ftp
        trace.write("\nEnvoi terminé")                                  #balise la fin du processus dans le fichier trace
        zip_trace()                                                     #fonction pour zipper les fichers trace
        
    except Exception as e:                                              #exeption si erreur
        ftp.quit()                                                      #ferme la liaison au ftp
        print('Error occurred : ' + str(e))
        trace.write('\nError occurred : ' + str(e))                     #reporte la ou les erreurs dans le fichier trace

#input()                                                                #pour test en exe