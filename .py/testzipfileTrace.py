# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:53:19 2023

@author: Vincent
"""
import datetime
from lxml import etree                                                  #pour creer les arbres xml
import pandas                                                           #pour trier les csv
import os, sys
import zipfile
from ftplib import FTP                                                  #pour communication avec serveur ftp

dateheure = str(datetime.datetime.now())   
path = "C:\\Users\\Vincent\\Desktop\\Entreprise\\Passerellepy\\" 

with zipfile.ZipFile(path+"ArchiveExport.zip", mode="w") as archive:
    #archive.printdir()
    with archive.open("Trace.txt", mode="w") as hello:
        hello.write(b"Hello, World!")