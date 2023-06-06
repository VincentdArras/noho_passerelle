# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:49:17 2022

@author: Vincent
"""
import datetime
from lxml import etree

def order_limit():
    last_order = 0
    fic = open("last_order.txt", 'r')
    last_order = int(fic.readline())
    #print(last_order,type(last_order))
    
    fic.close()
    return last_order

def rewrite_LO(last_o):
    fic = open("last_order.txt", 'w')
    fic.write(last_o)
    fic.close()
    print("Done Rewriting!")
    return None

def lire_csv(fic):
    #liste_info = []
    #liste_info = ligne.split(';')
    liste_info = []
    ind1 = 0
    ind2 = -1
    ligne = fic.readline()
    print(ligne)
    #print(ligne[len(ligne)-2])
    while ligne[len(ligne)-2].isdigit()==False :
        #print(ligne[len(ligne)-2])
        ligne = ligne + fic.readline()
        
    #print("\n\n",ligne)
    liste_info = []
    ind1=0
    ind2=-1
    while len(liste_info) < 30 :
        if ligne[ind1] == '|':
            liste_info.append(ligne[ind2+1:ind1])
            ind2=ind1
        ind1 = ind1 + 1
    #print(liste_info[10])
    #print("1",liste_info)
    del liste_info[10]
    #print(liste_info[20],type(liste_info[20]))
    #print(liste_info[20][len(liste_info[20])-1])
    if liste_info[20][len(liste_info[20])-1] == ' ':
        liste_info[20] = liste_info[20][:len(liste_info[20])-1]
    else :
        pass
    print("\n",liste_info, sep='')
    return liste_info

def validate_xml(ficxml):
    
    theDtd = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Vincent\\FichiersExemples\\ProshopVente.dtd"
    #parser = etree.XMLParser(dtd_validation=True)
    dtd = etree.DTD(open(theDtd))
    tree = etree.parse(ficxml)

    valid = dtd.validate(tree)
    if (valid):
        print("XML was valid!")

    else:
        print("\n\nXML was not valid:")
        print(dtd.error_log.filter_from_errors())

    return None


def creaxml():
    fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders3.csv",'r',encoding='UTF-8')
    fic.readline()
    
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    date_traiter = dateheure[:10]
    
    liste_infom1 = ['']
    liste_info = ['']
    liste_info2 = lire_csv(fic)
    
    last_order_process = liste_info2[0]
    if int(last_order_process) <= order_limit():
        print("No order to import")
        return None
    else:
        proshop = etree.Element("proshop")
        proshop.set("datesysteme", date_proshop)
        
        if liste_info2[10][:10] == date_traiter :
            ventes = etree.SubElement(proshop,"ventes")
            ventes.set("magasin","008")
            ventes.set("date",date_traiter)
            print(date_traiter)
        else :
            date_traiter = liste_info2[10][:10]
            ventes = etree.SubElement(proshop,"ventes")
            ventes.set("magasin","008")
            ventes.set("date",date_traiter)
            print(date_traiter)
        
        while int(liste_info2[0]) > order_limit() :

            if liste_info2[10][:10] == date_traiter :
                pass
                #print(date_traiter)
            else :
                date_traiter = liste_info2[10][:10]
                ventes = etree.SubElement(proshop,"ventes")
                ventes.set("magasin","008")
                ventes.set("date",date_traiter)
                #print(date_traiter)
            liste_infom1 = liste_info
            liste_info = liste_info2
            liste_info2 = lire_csv(fic)
            #print(liste_info)
            #print(liste_info2)
            if liste_info[4] == '2' or liste_info[4] == '3' or liste_info[4] == '4' or  liste_info[4] =='5':
                if liste_info[16][1].isdigit() == True:
                    pass
                else:
                    if liste_info[0] != liste_infom1[0]:
                        ticket = etree.SubElement(ventes,"ticket")
                        ticket.set("heure",liste_info[8][11:])
                        ticket.set("numero",liste_info[0])
                
                        client = etree.SubElement(ticket,"client")
                        code = etree.SubElement(client,"code")
                        code.text = liste_info[2]
                        nom = etree.SubElement(client,"nom")
                        nom.text = liste_info[13]
                        prenom = etree.SubElement(client,"prenom")
                        prenom.text = liste_info[12]
                        adresse1 = etree.SubElement(client,"adresse1")
                        adresse1.text = liste_info[20]
                        
                        if liste_info[21] != '' :
                            adresse2 = etree.SubElement(client,"adresse2")
                            adresse2.text = liste_info[21]
                        codepostal = etree.SubElement(client,"codepostal")
                        codepostal.text = liste_info[22]
                        ville = etree.SubElement(client,"ville")
                        ville.text = liste_info[23]
                        if liste_info[24] != '':    
                            telephone = etree.SubElement(client,"telephone")
                            telephone.text = liste_info[24]
                        email = etree.SubElement(client,"email")
                        email.text = liste_info[14]
                        
                        
                        produits = etree.SubElement(ticket,"produits")
                        article = etree.SubElement(produits,"article")
                        article.set("libelle",str(liste_info[16]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "V"
                        gencod = etree.SubElement(article,"gencod")
                        gencod_v = "900" + liste_info[15]
                        gencod.text = gencod_v                          #pas complet
                        
                        taille = etree.SubElement(article,"taille")
                        #flag = False
                        #for indt in range(len(liste_info[16])):
                            #if liste_info[16][indt] == ":":
                                #taille_v = liste_info[16][indt+2:len(liste_info[16])-1]
                                #taille.text = taille_v
                                #flag = True
                        #if flag == False :
                            #taille.text = "TU"
                        if liste_info[26] != '':
                            taille.text = liste_info[26]
                        else :
                            taille.text = "TU"
        
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[19]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[17]
                    
                    elif liste_infom1[0] == liste_info[0]:
                        article = etree.SubElement(produits,"article")
                        #article.set("collection","A RECUPERER")        #pas complet
                        article.set("libelle",str(liste_info[16]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "V"
                        gencod = etree.SubElement(article,"gencod")
                        gencod_v = "900" + liste_info[15]
                        gencod.text = gencod_v                          #pas complet
                        
                        taille = etree.SubElement(article,"taille")
                        #flag = False
                        #for indt in range(len(liste_info[16])):
                            #if liste_info[16][indt] == ":":
                                #taille_v = liste_info[16][indt+2:len(liste_info[16])-1]
                                #taille.text = taille_v
                                #flag = True
                        #if flag == False :
                            #taille.text = "TU"
                        if liste_info[26] != '':
                            taille.text = liste_info[26]
                        else :
                            taille.text = "TU"
                            
                            
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[19]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[17]
                        
                    if liste_info[0] != liste_info2[0]:
                        if liste_info[7] != '0.000000':                 #Debut_Livraison
                            article = etree.SubElement(produits,"article")
                            article.set("libelle","Transport")
                            type1 = etree.SubElement(article,"type")
                            type1.text = "R"                            #A verifier V
                            gencod = etree.SubElement(article,"gencod")
                            gencod.text = "TRA"
                            taille = etree.SubElement(article,"taille")
                            taille.text = ""
                            pvttc= etree.SubElement(article,"pvttc")
                            pvttc.text = liste_info[7]                  #Fin_Livraison
                            
                        reglements = etree.SubElement(ticket,"reglements")
                        mode = etree.SubElement(reglements,"mode")
                        code = etree.SubElement(mode,"code")
                        code_v = ''
                        if liste_info[5] == 'PayPal':
                            code_v = 'PAY'
                        elif liste_info[5] == 'Paiement par carte bancaire':
                            code_v = 'CB'
                        elif liste_info[5] == 'Apple Pay':
                            code_v = 'APP'
                        elif liste_info[5] == 'Google Pay':
                            code_v = 'GOO'
                        elif liste_info[5] == 'Paiement avec Choozeo sans frais' :
                            code_v = 'CHO'
                        else:
                            code_v = 'ESP'
                        code.text = code_v
                        montant = etree.SubElement(mode,"montant")
                        montant.text = liste_info[6]
        
            else:
                #notprocess = open("",'r',encoding='UTF-8')
                #notprocess.close()
                pass
            
        tree = etree.ElementTree(proshop)
        #date_export = date_proshop[0:13] + "-" + date_proshop[14:16] + "-" + date_proshop[17:19]
        date_export = date_proshop[0:4] + date_proshop[5:7] + date_proshop[8:10] + date_proshop[11:13] + date_proshop[14:16] + date_proshop[17:19]
        varxml = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Export\\CommandesClientNoho." + date_export + ".xml"
        xml_doc = open(varxml, 'x', encoding='ISO-8859-1')
        xml_doc.close()
        tree.write(varxml, xml_declaration=True, encoding='ISO-8859-1')
        
        validate_xml(varxml)
        #rewrite_LO(last_order_process)
    
    return None


creaxml()
