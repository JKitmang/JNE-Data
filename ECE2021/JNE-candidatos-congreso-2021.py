#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Preamble
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import urllib
import pandas as pd
import numpy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#b = webdriver.Chrome(executable_path = 'D:/Programas/Python packages/chromedriver_win32/chromedriver.exe' )
b = webdriver.Firefox(executable_path = 'C:/Users/ACER/Documents/Python Scripts/geckodriver.exe')

#set path file
path = "D:/Dropbox/Projects/Impulso País/Elecciones 2021/data_congreso/"
os.chdir(path)

#A: create output file
df = open("dni_candidatos.txt", encoding='utf-8')
linesdf = df.readlines()
resultdf = []
for x in linesdf:
    resultdf.append(x.split('\t')[0])
df.close()


#C: URLs descargados
#f = open("cv_fecha.txt", 'r',encoding="UTF-8")
#info = f.readlines()
#url_dwn = []
#for x in info:
#    url_dwn.append(x.split('\t')[0])
#f.close()

#Tab n
print("Total: ",len(resultdf))
      
#resultdf = set(resultdf).difference(url_dwn)
resultdf=set(resultdf)
print(resultdf)
print("Missing: ",len(resultdf))


url = "https://plataformaelectoral.jne.gob.pe/OrganizacionesPoliticas/BuscarCandidato"
b.get(url)

#Busqueda avanzada por DNI
buscar = '/html/body/main/div/div[1]/div[2]/div[2]/div/button'
input = '//*[@id="iddni"]'
c = 1
for id in resultdf:
    num_dni = id
    #complete DNI
    try:
        b.find_element_by_xpath(input).clear()
        b.find_element_by_xpath(input).send_keys(num_dni)
    except:
        window_after = b.window_handles[1]
        b.close()
        window_before = b.window_handles[0]
        b.switch_to.window(window_before)
        b.find_element_by_xpath(input).clear()
        b.find_element_by_xpath(input).send_keys(num_dni)
     
    #darle buscar
    time.sleep(2)
    try:
        b.find_element_by_xpath(buscar).click()
    except:
        time.sleep(1)
        b.find_element_by_xpath(buscar).click()

    #guardar estado
    try:    
        estado = b.find_element_by_xpath('/html/body/main/div/div[1]/div[4]/article/div/div/div/div[2]/p[5]').text
    except:
        estado = ""
        
    window_before = b.window_handles[0]
    #b.switch_to.window(window_before)

    #open cv data
    time.sleep(2)

    try:
        #time.sleep(1)
        b.find_element_by_xpath('/html/body/main/div/div[1]/div[4]/article/div/div/div/div[2]/div[2]/button[2]').click()
        time.sleep(2)

        window_after = b.window_handles[1]

        #switch to new window
        b.switch_to.window(window_after)
              
        time.sleep(4)        

        #Save data
        #-----------------------------------------------------------------
        # datos_basicos
        #-----------------------------------------------------------------
        num_dni = num_dni.strip()

        
        nac_fecha  = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[2]/div[2]/div[6]/label[2]').text
        dist_electoral = b.find_element_by_xpath('//*[@id="datos_personales"]/div[8]/div/label[2]').text
        org_pol  = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[6]/div/label[2]').text
        sexo = b.find_element_by_xpath("/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[2]/div[2]/div[2]/label[2]").text
        
        #Export data
        f = open("cv_data_basica.txt",'a', encoding='utf-8')    
        towrite = num_dni
        towrite = towrite.strip()
        varlist = [nac_fecha, dist_electoral, sexo,org_pol]
        cc = len(varlist)
        for j in range(0,cc):
            var = str(varlist[j])
            var2 = var.strip()
            towrite = towrite + "\t" + str(var2) 
        
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()

        #-----------------------------------------------------------------
        #Ingresos
        #-----------------------------------------------------------------
        ingr_remu_bru_pub	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[1]/td[2]/label').text
        ingr_remu_bru_priv	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[1]/td[3]/label').text
        ingr_remu_bru_tot	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[1]/td[4]/label').text
        ingr_rent_bru_pub	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[2]/td[2]/label').text
        ingr_rent_bru_priv	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[2]/td[3]/label').text
        ingr_rent_bru_tot	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[2]/td[4]/label').text
        ingr_otro_bru_pub	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[3]/td[2]/label').text
        ingr_otro_bru_priv	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[3]/td[3]/label').text
        ingr_otro_bru_tot	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[2]/table/tbody/tr[3]/td[4]/label').text
        ingr_total	        = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[3]/div/label[2]').text

        #Export data
        f = open("cv_ingresos.txt",'a', encoding='utf-8')    
        towrite = num_dni
        towrite = towrite.strip()

        varlist = [ingr_remu_bru_pub,ingr_remu_bru_priv,ingr_remu_bru_tot,ingr_rent_bru_pub,ingr_rent_bru_priv,ingr_rent_bru_tot,ingr_otro_bru_pub,ingr_otro_bru_priv,ingr_otro_bru_tot,ingr_total]
        cc = len(varlist)
        for j in range(0,cc):
            var = str(varlist[j])
            var2 = var.strip()
            towrite = towrite + "\t" + str(var2) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()

        
        #-----------------------------------------------------------------
        #Sentencias firmes
        #-----------------------------------------------------------------

        sent_firme_exp = [] 
        sent_firme_fec = []
        sent_firme_org = []
        sent_firme_del = []
        sent_firme_fal = []
        sent_firme_mod = []
        sent_firme_cum = []

        cc_sen = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article')) + 1
        for k in range(1,cc_sen):          
            sent_firme_exp.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[1]/div[1]/label[2]'.format(k)).text)
            sent_firme_fec.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[1]/div[2]/label[2]'.format(k)).text)
            sent_firme_org.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[1]/div[3]/label[2]'.format(k)).text)
            sent_firme_del.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[2]/div[1]/label[2]'.format(k)).text)
            sent_firme_fal.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[2]/div[2]/label[2]'.format(k)).text)
            sent_firme_mod.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[3]/div[1]/label[2]'.format(k)).text)
            sent_firme_cum.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[7]/section/article[{0}]/div[3]/div[2]/label[2]'.format(k)).text)

        #Export data
        matrix = numpy.array([sent_firme_exp,sent_firme_fec,sent_firme_org,sent_firme_del,sent_firme_fal,sent_firme_mod,sent_firme_cum])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_sentencias_firmes.txt",'a', encoding='utf-8')    
        towrite = num_dni
        towrite = towrite.strip()


        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                var = str(matrix[j][i])
                var2 = var.strip()
                towrite = towrite + "\t" + str(var2)                 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()
        
        #-----------------------------------------------------------------
        #Sentencias declaradas
        #-----------------------------------------------------------------

        sent_decla_mat = []
        sent_decla_exp = []
        sent_decla_org = []
        sent_decla_fallo = []

        cc_sen = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[8]/section/article')) + 1
        for k in range(1,cc_sen):                          
            #print(k)
            sent_decla_mat.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[8]/section/article[{0}]/div[1]/div[1]/label[2]'.format(k)).text)
            sent_decla_exp.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[8]/section/article[{0}]/div[1]/div[2]/label[2]'.format(k)).text)
            sent_decla_org.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[8]/section/article[{0}]/div[1]/div[3]/label[2]'.format(k)).text)
            sent_decla_fallo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[8]/section/article[{0}]/div[2]/div[1]/label[2]'.format(k)).text)

        #Export data
        matrix = numpy.array([sent_decla_mat,sent_decla_exp,sent_decla_org,sent_decla_fallo])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_sentencias_declaradas.txt",'a', encoding='utf-8')    
        towrite = num_dni
        towrite = towrite.strip()


        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                var = str(matrix[j][i])
                var2 = var.strip()
                towrite = towrite + "\t" + str(var2)                 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()

        #-----------------------------------------------------------------
        #Bienes inmuebles
        #-----------------------------------------------------------------

        bien_tipo = []
        bien_direc = []
        bien_sunarp = []
        bien_partida = []
        bien_valor = []

        cc_imm = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr')) + 1
        for l in range(1,cc_imm):                                                                    
            bien_tipo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[2]/label'.format(l)).text)
            bien_direc.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[3]/label'.format(l)).text)
            bien_sunarp.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[4]/label'.format(l)).text)
            bien_partida.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[5]/label'.format(l)).text)
            bien_valor.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[6]/label'.format(l)).text)

        #Export data
        matrix = numpy.array([bien_tipo, bien_direc, bien_sunarp, bien_partida, bien_valor])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_bienes_inmuebles.txt",'a', encoding='utf-8')    
        towrite = num_dni
        towrite = towrite.strip()

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                var = str(matrix[j][i])
                var2 = var.strip()
                towrite = towrite + "\t" + str(var2)                 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()

        print(str(cc),num_dni,": Done")
        b.close()
        b.switch_to.window(window_before)
            
        cc =cc +1
            
    except:
        print(str(num_dni), ": No found")
        
        #export dni que no se puede descargar
        f = open("dni_no_se_puede.txt",'a', encoding='utf-8')    
        towrite = num_dni + "\t" + estado  + "\n"
        towrite = towrite.strip()

        f.write(towrite)
        f.close()
        
        try: 
            window_after = b.window_handles[1]
            #switch to new window
            b.close()
            b.switch_to.window(window_before)
        except:
            print(num_dni,": Something happen")
        
        cc = cc + 1

