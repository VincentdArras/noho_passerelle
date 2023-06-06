# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:45:29 2022

@author: Vincent
"""

if liste_retour[13][1].isdigit() == True:             #Retire les cartes cadeaux
    pass
else:
    if liste_retour[7][:10] == date_traiter :
        pass
    #print(date_traiter)
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
        
        last_order_process = int(liste_retour[0][3:])
    
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
        article = etree.SubElement(produits,"article")
        article.set("libelle",str(liste_retour[13]))
        type1 = etree.SubElement(article,"type")
        type1.text = "V"
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
        pvttc.text = liste_retour[16]
        quantite= etree.SubElement(article,"quantite")
        quantite.text = liste_retour[14]
        
    elif liste_retourm1[0] == liste_retour[0]:                          #222222222222222222222222222222222
        article = etree.SubElement(produits,"article")
        #article.set("collection","A RECUPERER")        #pas complet
        article.set("libelle",str(liste_retour[13]))
        type1 = etree.SubElement(article,"type")
        type1.text = "V"
            
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
        pvttc.text = liste_retour[16]
        quantite= etree.SubElement(article,"quantite")
        quantite.text = liste_retour[14]
    
    if len(liste_retour2) == 0:
        liste_retour2.append(0)
        #print(liste_retour2)
        flagfin = True
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
            pvttc.text = liste_retour[6]                  #Fin_Livraison
                
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
        montant.text = liste_retour[5]