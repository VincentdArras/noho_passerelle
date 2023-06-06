# -*- coding: utf-8 -*-
from lxml import etree
"""
Created on Wed Nov 30 16:01:37 2022

@author: Vincent d'Arras
"""
def lire_csv(ligne):
    liste_info = []
    liste_info = ligne.split(';')
    
    return liste_info

def creaxml(fic):
    fic = open(fichier,'r',encoding='UTF-8')
    fic.readline()
    liste_info = lire_csv(fic.readline())
    print(liste_info)
    proshop = etree.Element("proshop")
    proshop.set("datesystem", liste_info[8])
    ventes = etree.SubElement(proshop,"ventes")
    ventes.set("magasin","008")
    ventes.set("date",liste_info[8][:10])
    ticket = etree.SubElement(ventes,"ticket")
    heure = liste_info[8][11:] +":00" #Ajout des secondes pour avoir le format correct
    ticket.set("heure",heure)
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
    adresse2 = etree.SubElement(client,"adresse2")
    adresse2.text = liste_info[21]
    codepostal = etree.SubElement(client,"codepostal")
    codepostal.text = liste_info[22]
    ville = etree.SubElement(client,"ville")
    ville.text = liste_info[23]
    
    #xml_str = etree.tostring(proshop, pretty_print=True)
    xml_str = str(etree.tostring(proshop,  pretty_print=True))
    print(xml_str, type(xml_str))
    with open("ecriture.xml", "w") as f:
        f.write(xml_str)
    
    
    fic.close
    return

fichier = 'request_sql_5.csv'
creaxml(fichier)