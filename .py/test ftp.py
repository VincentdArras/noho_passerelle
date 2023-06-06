# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 09:52:26 2022

@author: Vincent
"""
input()
from ftplib import FTP
fic = open("C:\\Users\\Vincent\\Desktop\\Test_ftp\\Test2.csv", 'wb')


path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\PY\\"
path2 = "C:\\Users\\Vincent\\Desktop\\Test_ftp\\"
ftp = FTP('ftp0.aquitem.fr')
ftp.login('nohoWeb', 'nohoWeb2022!')

f_name = "Test.csv"
f = open(path2 + f_name , 'rb')
ftp.storbinary('STOR ' + f_name, f)
f.close()

ftp.retrbinary('RETR exported_orders_prestashop.csv', fic.write)

ftp.quit()
fic.close()
print("FIN")
input()