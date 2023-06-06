# -*- coding: ISO-8859-1 -*-
import xml.etree.ElementTree as ET
import datetime
from lxml import etree
"""
Created on Thu Dec  1 11:23:24 2022

@author: Vincent
"""
def order_limit():
    last_order = 0
    fic = open("last_order.txt", 'r+')
    last_order = int(fic.readline())
    #print(last_order,type(last_order))
    
    fic.close()
    return last_order

def lire_csv(fic):
    #liste_info = []
    #liste_info = ligne.split(';')
    liste_info = []
    ind1 = 0
    ind2 = -1
    ligne = fic.readline()
    #print(ligne)
    #print(ligne[len(ligne)-3])
    while ligne[len(ligne)-3].isdigit()==False :
        ligne= ligne + fic.readline()
    #print("\n\n",ligne)
    liste_info = []
    ind1=0
    ind2=-1
    while len(liste_info) < 26 :
        if ligne[ind1] == ',':
            liste_info.append(ligne[ind2+1:ind1])
            ind2=ind1
        ind1 = ind1 + 1
    del liste_info[10]
    for i in range(len(liste_info)):
        liste_info[i] = liste_info[i][1:len(liste_info[i])-1]
    print(liste_info)
    return liste_info


def creaxml(fic):
    fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Vincent\\noho_orders.csv",'r',encoding='UTF-8')
    fic.readline()
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    
    liste_infom1 = ['']
    liste_info = ['']
    liste_info2 = lire_csv(fic)
    
    proshop = ET.Element("proshop")
    proshop.set("datesystem", date_proshop)
    
    
    ventes = ET.SubElement(proshop,"ventes")
    ventes.set("magasin","008")
    ventes.set("date",dateheure[:10])
    #flag = True
    
    while int(liste_info2[0]) > order_limit() :
    #while flag == True:
        liste_infom1 = liste_info
        liste_info = liste_info2
        liste_info2 = lire_csv(fic)
        #print(liste_info)
        #print(liste_info2)
        #heure = liste_info[7][12:]
        #date_v = liste_info[8][6:10]+"-"+liste_info[8][3:5]+"-"+liste_info[8][0:2]
        if liste_info[16][1].isdigit() == True:
            pass
        else:
            if liste_info[0] != liste_infom1[0]:
                ticket = ET.SubElement(ventes,"ticket")
                ticket.set("heure",liste_info[8][11:])
                ticket.set("numero",liste_info[0])
        
                client = ET.SubElement(ticket,"client")
                code = ET.SubElement(client,"code")
                code.text = liste_info[2]
                nom = ET.SubElement(client,"nom")
                nom.text = liste_info[13]
                prenom = ET.SubElement(client,"prenom")
                prenom.text = liste_info[12]
                adresse1 = ET.SubElement(client,"adresse1")
                adresse1.text = liste_info[20]
                
                if liste_info[21] != '' :
                    adresse2 = ET.SubElement(client,"adresse2")
                    adresse2.text = liste_info[21]
                codepostal = ET.SubElement(client,"codepostal")
                codepostal.text = liste_info[22]
                ville = ET.SubElement(client,"ville")
                ville.text = liste_info[23]
                email = ET.SubElement(client,"email")
                email.text = liste_info[14]
                if liste_info[24] != '':    
                    telephone = ET.SubElement(client,"telephone")
                    telephone.text = liste_info[24]
                
                produits = ET.SubElement(ticket,"produit")
                article = ET.SubElement(produits,"article")
                #article.set("collection","A RECUPERER")     #pas complet
                article.set("libelle",str(liste_info[16]))
                type1 = ET.SubElement(article,"type")
                type1.text = "V"
                gencode = ET.SubElement(article,"gencode")
                gencode_v = "900" + liste_info[15]
                gencode.text = gencode_v                    #pas complet
                taille = ET.SubElement(article,"taille")
                indt = 0
                print(liste_info[16],type(liste_info[16]))
                #print(liste_info[16][1].isdigit())
                if liste_info[16][1].isdigit() == True:     #Plus utile mais sécurité
                    pass                                    #Plus utile mais sécurité
                else:
                    while liste_info[16][indt] != ":":
                        indt = indt + 1
                    taille_v = liste_info[16][indt+2:len(liste_info[16])-1]
                    taille.text = taille_v
                pvttc= ET.SubElement(article,"pvttc")
                pvttc.text = liste_info[19]
                quantite= ET.SubElement(article,"quantite")
                quantite.text = liste_info[17]
            
            elif liste_infom1[0] == liste_info[0]:
                article = ET.SubElement(produits,"article")
                #article.set("collection","A RECUPERER")     #pas complet
                article.set("libelle",str(liste_info[16]))
                type1 = ET.SubElement(article,"type")
                type1.text = "V"
                gencode = ET.SubElement(article,"gencode")
                gencode_v = "900" + liste_info[15]
                gencode.text = gencode_v                    #pas complet
                taille = ET.SubElement(article,"taille")
                indt = 0
                while liste_info[16][indt] != ":":
                    indt = indt + 1
                taille_v = liste_info[16][indt+2:len(liste_info[16])-1]
                taille.text = taille_v
                pvttc= ET.SubElement(article,"pvttc")
                pvttc.text = liste_info[19]
                quantite= ET.SubElement(article,"quantite")
                quantite.text = liste_info[17]
                
            if liste_info[0] != liste_info2[0]:
                if liste_info[7] != '0.000000':     #Livraison
                    article = ET.SubElement(produits,"article")
                    article.set("libelle","Transport")
                    type1 = ET.SubElement(article,"type")
                    type1.text = "R"                #A verifier
                    gencode = ET.SubElement(article,"gencode")
                    gencode_v = "TRA"
                    pvttc= ET.SubElement(article,"pvttc")
                    pvttc.text = liste_info[7]
                reglements = ET.SubElement(ticket,"reglements")
                mode = ET.SubElement(reglements,"mode")
                code = ET.SubElement(mode,"code")
                code_v = ''
                if liste_info[5] == 'PayPal':
                    code_v = 'PAY'
                elif liste_info[5] == 'Paiement par carte bancaire':
                    code_v = 'CB'
                elif liste_info[5] == 'Apple Pay':
                    code_v = 'APP'
                elif liste_info[5] == 'Google Pay':
                    code_v = 'GOO'
                else:
                    code_v = 'ESP'
                code.text = code_v
                montant = ET.SubElement(mode,"montant")
                montant.text = liste_info[6]
    
            #flag = False
            print("FIN")
    tree = ET.ElementTree(proshop)
    tree.write("ecriture.xml", xml_declaration=True, encoding='ISO-8859-1')

    theDtd = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Vincent\\FichiersExemples\\ProshopVente.dtd"
    parser = etree.XMLParser(dtd_validation=True)
    dtd = etree.DTD(open(theDtd))
    tree2 = etree.parse("C:\\Users\\Vincent\\Desktop\\Entreprise\\ecriture.xml")

    valid = dtd.validate(tree2)
    if (valid):
        print("XML was valid!")

    else:
        print("XML was not valid:")
        print(dtd.error_log.filter_from_errors())
    
    return

fichier = 'request_sql_5.csv'
creaxml(fichier)
