# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:49:17 2022

@author: Vincent
"""
import datetime
from lxml import etree

def save_order(action, numero):
    
    
    
    return None    

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
    #print(ligne)
    #print(ligne[len(ligne)-2])
    while ligne[len(ligne)-2].isdigit()==False :
        #print(ligne[len(ligne)-2])
        ligne = ligne + fic.readline()
        
    #print("\n\n",ligne)
    liste_info = []
    ind1=0
    ind2=-1
    while len(liste_info) < 28 :
        if ligne[ind1] == '|':
            liste_info.append(ligne[ind2+1:ind1])
            ind2=ind1
        ind1 = ind1 + 1
    liste_info.append(ligne[ind2+1:len(ligne)-1])
    
    #if liste_info[17][len(liste_info[17])-1] == ' ':
        #liste_info[17] = liste_info[17][:len(liste_info[17])-1]
    #if liste_info[17][0] == ' ':
        #liste_info[17] = liste_info[17][1:]
    #print("+",liste_info[21],"+", liste_info[22],"+",liste_info[23],"+",liste_info[24])
    

    choix_tel = 0
    if liste_info[24] != '':
        choix_tel = 24
        print("24")
    if liste_info[22] != '':
        choix_tel = 22
        print("22")
    if liste_info[23] != '':
        choix_tel = 23
        print("23")
    if liste_info[21] != '':
        choix_tel = 21
        print("21")
        
    if choix_tel != 0 :
        liste_info[21] = liste_info[choix_tel]
    del liste_info[24]
    del liste_info[23]
    del liste_info[22]
    
    
    print("\n",liste_info, sep='')
    return liste_info

def validate_xml(ficxml):
    flag = False
    theDtd = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Vincent\\FichiersExemples\\ProshopVente.dtd"
    #parser = etree.XMLParser(dtd_validation=True)
    dtd = etree.DTD(open(theDtd))
    tree = etree.parse(ficxml)

    valid = dtd.validate(tree)
    if (valid):
        print("XML was valid!")
        flag = True

    else:
        print("\n\nXML was not valid:")
        print(dtd.error_log.filter_from_errors())
        flag = False

    return flag


def creaxml():
    fic = open("C:\\Users\\Vincent\\Desktop\\Entreprise\\Requête csv\\exported_orders8.csv",'r',encoding='UTF-8')
    fic.readline()
    
    dateheure = str(datetime.datetime.now())
    date_proshop = dateheure[:10]+'T'+dateheure[11:19]
    date_traiter = dateheure[:10]
    
    liste_infom1 = ['']
    liste_info = ['']
    liste_info2 = lire_csv(fic)
    
    last_order_process = liste_info2[1][3:]
    if int(last_order_process) <= order_limit():
        print("No order to import")
        return None
    else:
        proshop = etree.Element("proshop")
        proshop.set("datesysteme", date_proshop)
        
        if liste_info2[7][:10] == date_traiter :
            ventes = etree.SubElement(proshop,"ventes")
            ventes.set("magasin","008")
            ventes.set("date",date_traiter)
            print(date_traiter)
        else :
            date_traiter = liste_info2[7][:10]
            ventes = etree.SubElement(proshop,"ventes")
            ventes.set("magasin","008")
            ventes.set("date",date_traiter)
            print(date_traiter)
        
        while int(liste_info2[1][3:]) > order_limit() :

            if liste_info2[7][:10] == date_traiter :
                pass
                #print(date_traiter)
            else :
                date_traiter = liste_info2[7][:10]
                ventes = etree.SubElement(proshop,"ventes")
                ventes.set("magasin","008")
                ventes.set("date",date_traiter)
                #print(date_traiter)
            liste_infom1 = liste_info
            liste_info = liste_info2
            liste_info2 = lire_csv(fic)
            #print(liste_info)
            #print(liste_info2)
            if liste_info[3] == '2' or liste_info[3] == '3' or liste_info[3] == '4' or  liste_info[3] =='5':
                if liste_info[13][1].isdigit() == True:
                    pass
                else:
                    if liste_info[0] != liste_infom1[0]:
                        ticket = etree.SubElement(ventes,"ticket")
                        ticket.set("heure",liste_info[7][11:])
                        ticket.set("numero",liste_info[0])
                
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
                        if liste_info[24] != '':
                            taille.text = liste_info[24]
                        else :
                            taille.text = "TU"
        
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[16]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[14]
                    
                    elif liste_infom1[0] == liste_info[0]:
                        article = etree.SubElement(produits,"article")
                        #article.set("collection","A RECUPERER")        #pas complet
                        article.set("libelle",str(liste_info[13]))
                        type1 = etree.SubElement(article,"type")
                        type1.text = "V"
                        
                        gencod = etree.SubElement(article,"gencod")
                        if liste_info[22] != '':
                            gencod.text = liste_info[22]
                            #gencod_v = "900" + liste_info[12]
                        else:
                            gencod.text = "900" + liste_info[12] #gencod_v                          #pas complet
                        
                        taille = etree.SubElement(article,"taille")
                        if liste_info[24] != '':
                            taille.text = liste_info[24]
                        else :
                            taille.text = "TU"
                            
                            
                        pvttc= etree.SubElement(article,"pvttc")
                        pvttc.text = liste_info[16]
                        quantite= etree.SubElement(article,"quantite")
                        quantite.text = liste_info[14]
                        
                    if liste_info[0] != liste_info2[0]:
                        if liste_info[6] != '0.000000':                 #Debut_Livraison
                            article = etree.SubElement(produits,"article")
                            article.set("libelle","Transport")
                            type1 = etree.SubElement(article,"type")
                            type1.text = "R"                            #A verifier V
                            gencod = etree.SubElement(article,"gencod")
                            gencod.text = "TRA"
                            taille = etree.SubElement(article,"taille")
                            taille.text = ""
                            pvttc= etree.SubElement(article,"pvttc")
                            pvttc.text = liste_info[6]                  #Fin_Livraison
                            
                        reglements = etree.SubElement(ticket,"reglements")
                        mode = etree.SubElement(reglements,"mode")
                        code = etree.SubElement(mode,"code")
                        code_v = ''
                        if liste_info[4] == 'PayPal':
                            code_v = 'PAY'
                        elif liste_info[4] == 'Paiement par carte bancaire':
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
        
            else:
                #notprocess = open("",'r',encoding='UTF-8')
                #notprocess.close()
                pass
            
        
        tree = etree.ElementTree(proshop)
        varxmltest = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Test.xml"
        xml_doc = open(varxmltest, 'w', encoding='ISO-8859-1')
        xml_doc.close()
        tree.write(varxmltest, xml_declaration=True, encoding='ISO-8859-1')
        #validate_xml(varxml)
        #rewrite_LO(last_order_process)
        if validate_xml(varxmltest) == True:
            tree = etree.ElementTree(proshop)
            #date_export = date_proshop[0:13] + "-" + date_proshop[14:16] + "-" + date_proshop[17:19]
            date_export = date_proshop[0:4] + date_proshop[5:7] + date_proshop[8:10] + date_proshop[11:13] + date_proshop[14:16] + date_proshop[17:19]
            varxml = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Export\\CommandesClientNoho." + date_export + ".xml"
            xml_doc = open(varxml, 'x', encoding='ISO-8859-1')
            xml_doc.close()
            tree.write(varxml, xml_declaration=True, encoding='ISO-8859-1')
            #rewrite_LO(last_order_process)
    
    return None


creaxml()
