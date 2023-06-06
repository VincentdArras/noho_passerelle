# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:49:17 2022

@author: Vincent d'Arras'
"""
import datetime
from lxml import etree
import pandas

def maj_forme_retour():
    data = pandas.read_csv("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",sep ='|', dtype="string")
    data = data.sort_values(by=['Credit Slip Number'], ascending=False)
    #print(data)
    data.to_csv("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')

    return None

def maj_forme_commande():
    fic = open("C:\Users\Vincent\Desktop\Entreprise\Requête csv\exported_orders14.csv",'r',encoding='UTF-8')
    fic2 = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",'w',encoding= 'UTF-8')

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
        #print("\n +",ligne)

     
    fic.close()
    fic2.close()
    
    data = pandas.read_csv("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",sep ='|', dtype="string")
    data = data.sort_values(by=['Numéro de facture'], ascending=True)
    #print(data)
    data.to_csv("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv", index=False, encoding='UTF-8', sep ='|')
    return None

def order_limit():
    #last_order = 0
    fic = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\last_order.txt", 'r')
    last_order = int(fic.readline())
    last_return = int(fic.readline())
    #print(last_order,type(last_order))
    
    fic.close()
    return last_order,last_return

def rewrite_LO(last_o, last_r):
    fic = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\last_order.txt", 'w')
    fic.write(str(last_o)+"\n")
    fic.write(str(last_r))
    fic.close()
    print("Done Rewriting!")
    return None

def lire_csv(fic):
    liste_info = []
    ind1 = 0
    ind2 = -1
    ligne = fic.readline()
    if len(ligne) == 0:
        return liste_info
     
    #print("\n\n",ligne)
    ind1=0
    ind2=-1
    while len(liste_info) < 34 :
        if ligne[ind1] == '|':
            liste_info.append(ligne[ind2+1:ind1])
            ind2=ind1
        ind1 = ind1 + 1
    liste_info.append(ligne[ind2+1:len(ligne)-1])
    
    """ Correction des espaces fantomes
    for i in range(15):
        if liste_info[i][len(liste_info[i])-1] == ' ':
            liste_info[i] = liste_info[i][:len(liste_info[i])-1]
        if liste_info[i][0] == ' ':
            liste_info[i] = liste_info[i][1:]
     """   
    

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
        
    if choix_tel != 0 :
        liste_info[21] = liste_info[choix_tel]
    del liste_info[24]
    del liste_info[23]
    del liste_info[22]
    
    if liste_info[13] == "":
        liste_info[13] = "00"

    #print("\n",liste_info, sep='')
    return liste_info

def validate_xml(ficxml):
    flag = False
    theDtd = "C:\Users\Vincent\Desktop\Entreprise\Passerllepy\ProshopVente.dtd"
    #parser = etree.XMLParser(dtd_validation=True)
    opendtd = open(theDtd)
    dtd = etree.DTD(opendtd)
    tree = etree.parse(ficxml)

    valid = dtd.validate(tree)
    if (valid):
        print("XML is valid!")
        flag = True

    else:
        print("\n\nXML isn't valid:")
        print(dtd.error_log.filter_from_errors())
        flag = False
    opendtd.close()
    return flag


def creatree_order():
    maj_forme_commande()
    fic = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",'r',encoding='UTF-8')
    fic.readline()
    flagfin = False
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    date_traiter = dateheure[:10]
    
    liste_infom1 = ['']
    liste_info = ['']
    liste_info2 = lire_csv(fic)
    
    
    while int(liste_info2[0][3:]) <= int(order_limit()[0]):
        liste_info = liste_info2
        liste_info2 = lire_csv(fic)
        #print(liste_info2)
        if len(liste_info2) == 0:
            print("No order to import")
            return None, liste_info[0][3:]
          
   
    #print(liste_info2)
    #date_traiter = liste_info2[7][:10]
    proshop = etree.Element("proshop")
    proshop.set("datesysteme", date_proshop)
    
    while flagfin == False :
        liste_infom1 = liste_info
        liste_info = liste_info2
        liste_info2 = lire_csv(fic)
        #print(liste_info)
        #print(liste_info2)
        #if liste_info[3] == '2' or liste_info[3] == '3' or liste_info[3] == '4' or  liste_info[3] =='5' or liste_info[3] =='5':

        if liste_info[13][1].isdigit() == True:             #Retire les cartes cadeaux
            pass
        else:
            if liste_info[7][:10] == date_traiter and 'ventes' in locals() :
                pass
            #print(date_traiter)
            else :
                date_traiter = liste_info[7][:10]
                ventes = etree.SubElement(proshop,"ventes")
                ventes.set("magasin","008")
                ventes.set("date",date_traiter)
                #print(date_traiter)
            
            if liste_info[0] != liste_infom1[0]:                    #111111111111111111111111111111111111
                ticket = etree.SubElement(ventes,"ticket")
                ticket.set("heure",liste_info[7][11:])
                ticket.set("numero",liste_info[0][3:])      #numéro de facture, a changer
                
                last_order_process = int(liste_info[0][3:])
            
                client = etree.SubElement(ticket,"client")
                code = etree.SubElement(client,"code")
                code.text = liste_info[2]
                nom = etree.SubElement(client,"nom")
                nom.text = liste_info[10]
                prenom = etree.SubElement(client,"prenom")
                prenom.text = liste_info[9]
                adresse1 = etree.SubElement(client,"adresse1")
                adresse1.text = liste_info[17]
                    
                if liste_info[18] != '' :
                    adresse2 = etree.SubElement(client,"adresse2")
                    adresse2.text = liste_info[18]
                codepostal = etree.SubElement(client,"codepostal")
                codepostal.text = liste_info[19]
                ville = etree.SubElement(client,"ville")
                ville.text = liste_info[20]
                if liste_info[21] != '':    
                    telephone = etree.SubElement(client,"telephone")
                    telephone.text = liste_info[21]
                email = etree.SubElement(client,"email")
                email.text = liste_info[11]
                    
                    
                produits = etree.SubElement(ticket,"produits")
                article = etree.SubElement(produits,"article")
                article.set("libelle",str(liste_info[13]))
                type1 = etree.SubElement(article,"type")
                type1.text = "V"
                gencod = etree.SubElement(article,"gencod")
                if liste_info[22] != '':
                    gencod.text = liste_info[22]
                else:
                    gencod.text = "900" + liste_info[12]
                    
                taille = etree.SubElement(article,"taille")
                size =""
                for t in range(23,26):
                    if liste_info[t] != '':
                        size = liste_info[t]
                if len(size) != 0:
                    for ta in range(len(size)):
                        if size[ta] == ",":
                            size = size[:ta]
                            break
                    taille.text = size
                else :
                    taille.text = "TU"
    
                pvttc= etree.SubElement(article,"pvttc")
                pvttc.text = liste_info[16]
                quantite= etree.SubElement(article,"quantite")
                quantite.text = liste_info[14]
                
            elif liste_infom1[0] == liste_info[0]:                          #222222222222222222222222222222222
                article = etree.SubElement(produits,"article")
                #article.set("collection","A RECUPERER")        #pas complet
                article.set("libelle",str(liste_info[13]))
                type1 = etree.SubElement(article,"type")
                type1.text = "V"
                    
                gencod = etree.SubElement(article,"gencod")
                if liste_info[22] != '':
                    gencod.text = liste_info[22]
                else:
                    gencod.text = "900" + liste_info[12]                        #pas complet
                 
                    
                taille = etree.SubElement(article,"taille")
                size =""
                for t in range(23,26):
                    if liste_info[t] != '':
                        size = liste_info[t]
                if len(size) != 0:
                    for ta in range(len(size)):
                        if size[ta] == ",":
                            size = size[:ta]
                            break
                    taille.text = size
                else :
                    taille.text = "TU"
                        
                        
                pvttc= etree.SubElement(article,"pvttc")
                pvttc.text = liste_info[16]
                quantite= etree.SubElement(article,"quantite")
                quantite.text = liste_info[14]
            
            if len(liste_info2) == 0:
                liste_info2.append(0)
                #print(liste_info2)
                flagfin = True
            if liste_info[0] != liste_info2[0]:                         #33333333333333333333333333333333
                if liste_info[6] != '0.000000':                 #Debut_Livraison
                    article = etree.SubElement(produits,"article")
                    article.set("libelle","Transport")
                    type1 = etree.SubElement(article,"type")
                    type1.text = "R"                            #A verifier V
                    gencod = etree.SubElement(article,"gencod")
                    gencod.text = "TRA"
                    
                    taille = etree.SubElement(article,"taille")
                    taille.text = "TU"
                       
                    pvttc= etree.SubElement(article,"pvttc")
                    pvttc.text = liste_info[6]                  #Fin_Livraison
                        
                reglements = etree.SubElement(ticket,"reglements")
                mode = etree.SubElement(reglements,"mode")
                code = etree.SubElement(mode,"code")
                code_v = ''
                if liste_info[4] == 'PayPal':
                    code_v = 'PAY'
                elif liste_info[4] == 'Paiement par carte bancaire' or 'Credit Card':
                    code_v = 'CB'
                elif liste_info[4] == 'Apple Pay':
                    code_v = 'APP'
                elif liste_info[4] == 'Google Pay':
                    code_v = 'GOO'
                elif liste_info[4] == 'Paiement avec Choozeo sans frais' :
                    code_v = 'CHO'
                else:
                    code_v = 'ESP'
                code.text = code_v
                montant = etree.SubElement(mode,"montant")
                montant.text = liste_info[5]
    
        
           
    fic.close()
    return proshop, last_order_process

def creatree_return(proshop):
    maj_forme_retour()
    fic_retour = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",'r',encoding='UTF-8')
    fic_retour.readline()
    flag_retour = True
    
    date_traiter = ""
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    
    limites = order_limit()[1]
    liste_retour = ['']
    liste_retour2 = lire_csv(fic_retour)
    liste_retour2[31] = liste_retour2[31][:len(liste_retour2[31])-1]
    last_return = liste_retour2[28]
    
    if int(liste_retour2[28]) <= limites and proshop == None:
        flag_retour = False
        print("No return to import")
        return proshop, last_return
    elif int(liste_retour2[28]) <= limites and proshop != None:
        flag_retour = False
        print("No return to import")
        return proshop, last_return
    elif int(liste_retour2[28]) > limites and proshop == None:
        proshop = etree.Element("proshop")
        proshop.set("datesysteme", date_proshop)
    
    
    while flag_retour == True:
        liste_retourm1 = liste_retour
        liste_retour = liste_retour2
        liste_retour2 = lire_csv(fic_retour)
        liste_retour2[31] = liste_retour2[31][:len(liste_retour2[31])-1]
        #print(liste_retour)
        if int(liste_retour[28]) <= limites:
            flag_retour = False
            break
        else:
            
            if liste_retour[13][1].isdigit() == True:             #Retire les cartes cadeaux
                pass
            else:
                if liste_retour[7][:10] == date_traiter:
                    pass
                else :
                    date_traiter = liste_retour[7][:10]
                    ventes = etree.SubElement(proshop,"ventes")
                    ventes.set("magasin","008")
                    ventes.set("date",date_traiter)
                    #print(date_traiter)
                
                if liste_retour[0] != liste_retourm1[0]:                    #111111111111111111111111111111111111
                    ticket = etree.SubElement(ventes,"ticket")
                    ticket.set("heure",liste_retour[7][11:])
                    ticket.set("numero",liste_retour[0][3:])      #numéro de facture, a changer
                    
                    client = etree.SubElement(ticket,"client")
                    code = etree.SubElement(client,"code")
                    code.text = liste_retour[2]
                    nom = etree.SubElement(client,"nom")
                    nom.text = liste_retour[10]
                    prenom = etree.SubElement(client,"prenom")
                    prenom.text = liste_retour[9]
                    adresse1 = etree.SubElement(client,"adresse1")
                    adresse1.text = liste_retour[17]
                        
                    if liste_retour[18] != '' :
                        adresse2 = etree.SubElement(client,"adresse2")
                        adresse2.text = liste_retour[18]
                    codepostal = etree.SubElement(client,"codepostal")
                    codepostal.text = liste_retour[19]
                    ville = etree.SubElement(client,"ville")
                    ville.text = liste_retour[20]
                    if liste_retour[21] != '':    
                        telephone = etree.SubElement(client,"telephone")
                        telephone.text = liste_retour[21]
                    email = etree.SubElement(client,"email")
                    email.text = liste_retour[11]
                    produits = etree.SubElement(ticket,"produits")
                    
                    if liste_retour[30] !='0.000000':
                        
                        article = etree.SubElement(produits,"article")
                        article.set("libelle",str(liste_retour[13]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "I"
                        gencod = etree.SubElement(article,"gencod")
                        if liste_retour[22] != '':
                            gencod.text = liste_retour[22]
                        else:
                            gencod.text = "900" + liste_retour[12]
                            
                        taille = etree.SubElement(article,"taille")
                        size =""
                        for t in range(23,26):
                            if liste_retour[t] != '':
                                size = liste_retour[t]
                        if len(size) != 0:
                            for ta in range(len(size)):
                                if size[ta] == ",":
                                    size = size[:ta]
                                    break
                            taille.text = size
                        else :
                            taille.text = "TU"
    
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_retour[30]                             #Voir pour moins
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_retour[14]
                    
                elif liste_retourm1[0] == liste_retour[0] and liste_retour[30] !='0.000000' :    #222222222222222222222222222222222
                    print("**",liste_retour)
                    article = etree.SubElement(produits,"article")
                    article.set("libelle",str(liste_retour[13]))
                    type1 = etree.SubElement(article,"type")
                    type1.text = "I"
                        
                    gencod = etree.SubElement(article,"gencod")
                    if liste_retour[22] != '':
                        gencod.text = liste_retour[22]
                    else:
                        gencod.text = "900" + liste_retour[12]                        #pas complet
                     
                        
                    taille = etree.SubElement(article,"taille")
                    size =""
                    for t in range(23,26):
                        if liste_retour[t] != '':
                            size = liste_retour[t]
                    if len(size) != 0:
                        for ta in range(len(size)):
                            if size[ta] == ",":
                                size = size[:ta]
                                break
                        taille.text = size
                    else :
                        taille.text = "TU"
                            
                            
                    pvttc= etree.SubElement(article,"pvttc")
                    pvttc.text = liste_retour[30]                             #Voir pour moins
                    quantite= etree.SubElement(article,"quantite")
                    quantite.text = liste_retour[14]
                
                if liste_retour[0] != liste_retour2[0]:                         #33333333333333333333333333333333
                    if liste_retour[6] != '0.000000':                 #Debut_Livraison
                        article = etree.SubElement(produits,"article")
                        article.set("libelle","Transport")
                        type1 = etree.SubElement(article,"type")
                        type1.text = "R"                            #A verifier V
                        gencod = etree.SubElement(article,"gencod")
                        gencod.text = "TRA"
                        
                        taille = etree.SubElement(article,"taille")
                        taille.text = "TU"
                           
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = "-"+liste_retour[6]                  #Fin_Livraison
                            
                    reglements = etree.SubElement(ticket,"reglements")
                    mode = etree.SubElement(reglements,"mode")
                    code = etree.SubElement(mode,"code")
                    code_v = ''
                    if liste_retour[4] == 'PayPal':
                        code_v = 'PAY'
                    elif liste_retour[4] == 'Paiement par carte bancaire' or 'Credit Card':
                        code_v = 'CB'
                    elif liste_retour[4] == 'Apple Pay':
                        code_v = 'APP'
                    elif liste_retour[4] == 'Google Pay':
                        code_v = 'GOO'
                    elif liste_retour[4] == 'Paiement avec Choozeo sans frais' :
                        code_v = 'CHO'
                    else:
                        code_v = 'ESP'
                    code.text = code_v
                    montant = etree.SubElement(mode,"montant")
                    montant.text = "-"+liste_retour[31]
        """
        Adapter l'import de vente pour lire les retours
        Attention au total, au shipping, au reduction, au produit multiple ...
        """
        
    #print(liste_retour, limites)
    fic_retour.close()
    
    
    return proshop, last_return

def crea_xml(proshop, rw_order, rw_return):
    
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    tree = etree.ElementTree(proshop)
    varxmltest = "C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Test.xml"
    xml_doc = open(varxmltest, 'w', encoding='ISO-8859-1')
    tree.write(varxmltest, xml_declaration=True, encoding='ISO-8859-1')
    xml_doc.close()
    #validate_xml(varxml)
    if validate_xml(varxmltest) == True:
        #tree = etree.ElementTree(proshop)
        #date_export = date_proshop[0:13] + "-" + date_proshop[14:16] + "-" + date_proshop[17:19]
        date_export = date_proshop[0:4] + date_proshop[5:7] + date_proshop[8:10] + date_proshop[11:13] + date_proshop[14:16] + date_proshop[17:19]
        varxml = "C:\Users\Vincent\Desktop\Entreprise\Export\CommandesClientNoho." + date_export + ".xml"     #placement a definir
        xml_doc = open(varxml, 'x', encoding='ISO-8859-1')
        tree.write(varxml, xml_declaration=True, encoding='ISO-8859-1')
        xml_doc.close()
        #rewrite_LO(rw_order)
    return None

proshop1, last_order_process1 = creatree_order()
proshop2, last_return_process1 = creatree_return(proshop1)
if proshop2 != None:
    crea_xml(proshop2, last_order_process1, last_return_process1)
    rewrite_LO(last_order_process1, last_return_process1)

csv_file = open("C:\Users\Vincent\Desktop\Entreprise\Passerllepy\Commande_en_traitement.csv",'r',encoding='UTF-8')
csv_file.close()