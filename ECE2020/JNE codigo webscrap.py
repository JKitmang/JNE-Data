#!/usr/bin/env python
# coding: utf-8

# In[122]:


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

#b = webdriver.Chrome(executable_path = 'D:/Programas/Python packages/chromedriver_win32/chromedriver.exe' )
b = webdriver.Firefox(executable_path = 'C:/Users/ACER/Documents/Python Scripts/geckodriver.exe')

#set path file
path = "D:/Google Drive/ECE2020/"
os.chdir(path)

#create output file
f = open("cv_candidatos.txt",'w', encoding='utf-8')
#towrite = "CÓDIGO" + "\t" + "CARGO" + "\t" + "DNI" + "\t" + "NOMBRES" + "\t" + "FEC_NAC"  + "\t" + "GENERO" + "\t" + "DESIGNADO"  + "\t" + "NATIVO" + "\t" + "ESTADO" + "\n"
#f.write(towrite)
f.close()
 
#abrir lista de codigos
df = open('lista_candidatos_v2.txt', encoding='utf-8')
linesdf = df.readlines()
resultdf = []
for x in linesdf:
    #print(x)
    resultdf.append(x.split('\t')[3])
df.close()
#print(resultdf)

#C: URLs dwn
f = open("cv_fecha.txt", 'r',encoding="UTF-8")
info = f.readlines()
url_dwn = []
for x in info:
    url_dwn.append(x.split('\t')[0])
f.close()

#C: DNI que no funcionan
f = open("dni_no_se_puede.txt", 'r',encoding="UTF-8")
info2 = f.readlines()
dni_no = []
for x in info2:
    dni_no.append(x.split('\t')[0])
f.close()

print("Done: ",len(url_dwn))
#print(resultdf)
print("Total: ",len(resultdf))
      
resultdf = set(resultdf).difference(url_dwn)
resultdf = set(resultdf).difference("NOMBRES")
resultdf = set(resultdf).difference(dni_no)

resultdf=set(resultdf)
print("Missing: ",len(resultdf))

url = "https://plataformaelectoral.jne.gob.pe/OrganizacionesPoliticas/BuscarCandidato"
b.get(url)

#Busqueda avanzada por DNI
buscar = '/html/body/main/div/div[1]/div[2]/div[2]/div/button'
input = '//*[@id="iddni"]'
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
     
    time.sleep(2)
    try:
        b.find_element_by_xpath(buscar).click()
    except:
        time.sleep(2)
        b.find_element_by_xpath(buscar).click()
    try:    
        estado = b.find_element_by_xpath('/html/body/main/div/div[1]/div[4]/article/div/div/div/div[2]/p[5]').text
    except:
        estado = ""
        
    window_before = b.window_handles[0]
    #b.switch_to.window(window_before)

    #open cv data
    time.sleep(2)

    try:
        b.find_element_by_xpath('/html/body/main/div/div[1]/div[4]/article/div/div/div/div[2]/div[2]/button[2]').click()
        window_after = b.window_handles[1]

        #switch to new window
        b.switch_to.window(window_after)
        time.sleep(2)

        #Save data
        #-----------------------------------------------------------------
        # datos_basicos
        #-----------------------------------------------------------------

        nac_fecha = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[2]/div[2]/div[6]/label[2]').text
        nac_pais = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[3]/div[1]/label[2]').text
        nac_dpto = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[3]/div[2]/label[2]').text
        nac_provincia = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[3]/div[3]/label[2]').text
        nac_distrito = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[3]/div[4]/label[2]').text
        dom_pais = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[4]/div[1]/label[2]').text
        dom_dpto = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[4]/div[2]/label[2]').text
        dom_provincia = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[4]/div[3]/label[2]').text
        direccion = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[2]/div[5]/div[1]/label[2]').text

        #Export data
        f = open("cv_data_basica.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [nac_fecha, nac_pais, nac_dpto, nac_provincia, nac_distrito, dom_pais,dom_dpto,dom_provincia,direccion]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()



        #-----------------------------------------------------------------
        # experiencia laboral
        #-----------------------------------------------------------------


        cent = []
        ocup = []
        ruce = []
        dire = []
        aini = []
        afin = []
        pais = []
        dpto = []
        prov = []
        dist = []

        cc_el = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article')) + 1
        #print(cc_el)
        for i in range(1,cc_el):
            cent.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[1]/div[1]/label[2]'.format(i)).text)
            ocup.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[2]/div[1]/label[2]'.format(i)).text)
            ruce.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[2]/div[2]/label[2]'.format(i)).text)
            dire.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[3]/div[1]/label[2]'.format(i)).text)
            aini.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[3]/div[2]/label[2]'.format(i)).text)
            afin.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[3]/div[3]/label[2]'.format(i)).text)
            pais.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[4]/div[1]/label[2]'.format(i)).text)
            dpto.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[4]/div[2]/label[2]'.format(i)).text)
            prov.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[4]/div[3]/label[2]'.format(i)).text)
            dist.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[3]/section/article[{0}]/div[4]/div[4]/label[2]'.format(i)).text)

        #Export data
        matrix = numpy.array([cent,ocup,ruce,dire,aini,afin,pais,dpto,prov,dist])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_experiencia_laboral.txt",'a', encoding='utf-8')    
        towrite = num_dni

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()



        #-----------------------------------------------------------------
        #education
        #-----------------------------------------------------------------


        #Educacion basica
        edu_prim = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[3]/div[1]/label[2]').text
        edu_prim_concl = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[3]/div[2]/label[2]').text
        edu_secu = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[4]/div[1]/label[2]').text
        edu_secu_concl = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[4]/div[2]/label[2]').text

        #Educacion tecnica
        edu_tec_etec = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[6]/div/label[2]').text
        etec_centro = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[7]/div[1]/label[2]').text
        etec_carrera = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[7]/div[2]/label[2]').text
        etec_conclu = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[7]/div[3]/label[2]').text
        edu_nouniv_nu = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[8]/div/label[2]').text
        nu_centro = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[9]/div[1]/label[2]').text
        nu_carrera = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[9]/div[2]/label[2]').text
        nu_conclu = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[9]/div[3]/label[2]').text


        #educación de post grado
        edu_post = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[12]/div[1]/label[2]').text
        post_centro = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[13]/div[1]/label[2]').text
        post_especial = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[13]/div[2]/label[2]').text
        post_conclu = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[14]/div[1]/label[2]').text
        post_egr = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[14]/div[2]/label[2]').text
        post_maestr = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[15]/div[1]/label[2]').text
        post_doc = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[15]/div[2]/label[2]').text
        post_ano = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/div[15]/div[3]/label[2]').text

        #Export data
        f = open("cv_educacion.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [edu_prim,edu_prim_concl,edu_secu,edu_secu_concl,edu_tec_etec,etec_centro,etec_carrera,etec_conclu,edu_nouniv_nu,nu_centro,nu_carrera,nu_conclu,edu_post,post_centro,post_especial,post_conclu,post_egr,post_maestr,post_doc,post_ano]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()

        #Educacion universitaria
        univ_centro = []
        univ_concl = []
        univ_carrera = []
        univ_egres = []
        univ_bach = []
        univ_ano_bach = []
        univ_titulo = []
        univ_titulo_bach = []                                    

        cc_el = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section')) + 1

        for j in range(1,cc_el):                                      
            univ_centro.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[1]/div[1]/label[2]'.format(j)).text)
            univ_concl.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[1]/div[2]/label[2]'.format(j)).text)
            univ_carrera.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[2]/div[1]/label[2]'.format(j)).text)
            univ_egres.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[2]/div[2]/label[2]'.format(j)).text)
            univ_bach.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[3]/div[1]/label[2]'.format(j)).text)
            univ_ano_bach.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[3]/div[2]/label[2]'.format(j)).text)
            univ_titulo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[3]/div[3]/label[2]'.format(j)).text)
            univ_titulo_bach.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[4]/section[{0}]/div/div/article/div[3]/div[4]/label[2]'.format(j)).text)


        #Export data
        matrix = numpy.array([univ_centro,univ_concl,univ_carrera,univ_egres,univ_bach,univ_ano_bach,univ_titulo,univ_titulo_bach])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_educacion_univ.txt",'a', encoding='utf-8')    
        towrite = num_dni

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()


        #-----------------------------------------------------------------
        #cargo partidiario
        #-----------------------------------------------------------------

        carg_part_org_1 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[1]/div/div/div[1]/label[2]').text
        carg_part_cargo_1 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[1]/div/div/div[2]/label[2]').text
        carg_part_ini_1 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[1]/div/div/div[3]/label[2]').text
        carg_part_fin_1 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[1]/div/div/div[4]/label[2]').text

        try:
            carg_part_org_2 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[2]/div/div/div[1]/label[2]').text
            carg_part_cargo_2 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[2]/div/div/div[2]/label[2]').text
            carg_part_ini_2 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[2]/div/div/div[3]/label[2]').text
            carg_part_fin_2 	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[5]/section/article[2]/div/div/div[4]/label[2]').text
        except:
            carg_part_org_2 	= "" 
            carg_part_cargo_2 	= ""
            carg_part_ini_2 	= ""
            carg_part_fin_2 	= ""

        #Export data
        f = open("cv_cargo_partidiario.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [carg_part_org_1,carg_part_cargo_1,carg_part_ini_1,carg_part_fin_1,carg_part_org_2,carg_part_cargo_2,carg_part_ini_2,carg_part_fin_2]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()


        #-----------------------------------------------------------------
        #cargos de elección popular
        #-----------------------------------------------------------------

        #-----------------------------------------------------------------
        #Renuncias
        #-----------------------------------------------------------------
        renun_1_part	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[6]/article[1]/div/div[1]/label[2]').text
        renun_1_year	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[6]/article[1]/div/div[2]/label[2]').text
        try:
            renun_2_part	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[6]/article[2]/div/div[1]/label[2]').text
            renun_2_year	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[6]/article[2]/div/div[2]/label[2]').text
        except: 
            renun_2_part = ""
            renun_2_year = ""

        #Export data
        f = open("cv_renuncias.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [renun_1_part,renun_1_year,renun_2_part,renun_2_year]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
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

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
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

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
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
        ingr_total	= b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[1]/form/div[3]/div/label[2]').text

        #Export data
        f = open("cv_ingresos.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [ingr_remu_bru_pub,ingr_remu_bru_priv,ingr_remu_bru_tot,ingr_rent_bru_pub,ingr_rent_bru_priv,ingr_rent_bru_tot,ingr_otro_bru_pub,ingr_otro_bru_priv,ingr_otro_bru_tot,ingr_total]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()

        #-----------------------------------------------------------------
        #Bienes inmuebles
        #-----------------------------------------------------------------

        bien_tipo = []
        bien_pais = []
        bien_dpto = []
        bien_prov = []
        bien_dist = []
        bien_direcc = []
        bien_sunarp = []
        bien_part = []
        bien_ficha = []
        bien_auto = []

        cc_imm = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr')) + 1
        for l in range(1,cc_imm):                                                                    
            bien_tipo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[2]/label'.format(l)).text)
            bien_pais.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[3]/label'.format(l)).text)
            bien_dpto.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[4]/label'.format(l)).text)
            bien_prov.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[5]/label'.format(l)).text)
            bien_dist.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[6]/label'.format(l)).text)
            bien_direcc.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[7]/label'.format(l)).text)
            bien_sunarp.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[8]/label'.format(l)).text)
            bien_part.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[9]/label'.format(l)).text)
            bien_ficha.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[10]/label'.format(l)).text)
            bien_auto.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[2]/div[2]/table/tbody/tr[{0}]/td[11]/label'.format(l)).text)


        #Export data
        matrix = numpy.array([bien_tipo,bien_pais,bien_dpto,bien_prov,bien_dist,bien_direcc,bien_sunarp,bien_part,bien_ficha,bien_auto])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_bienes_inmuebles.txt",'a', encoding='utf-8')    
        towrite = num_dni

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()



        #-----------------------------------------------------------------
        #Bienes muebles
        #-----------------------------------------------------------------


        mueb_total = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[2]/div/label[2]').text

        mueb_vehi_tipo = []
        mueb_vehi_marca = []
        mueb_vehi_modelo = []
        mueb_vehi_year = []
        mueb_vehi_placa = []
        mueb_vehi_carac = []
        mueb_vehi_valor = []

        cc_mueb = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr')) + 1
        for m in range(1,cc_mueb):                                                                                                   
            mueb_vehi_tipo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[2]/label'.format(m)).text)
            mueb_vehi_marca.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[3]/label'.format(m)).text)
            mueb_vehi_modelo.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[4]/label'.format(m)).text)
            mueb_vehi_year.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[5]/label'.format(m)).text)
            mueb_vehi_placa.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[6]/label'.format(m)).text)
            mueb_vehi_carac.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[7]/label'.format(m)).text)
            mueb_vehi_valor.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr[{0}]/td[8]/label'.format(m)).text)

        #Export data
        matrix = numpy.array([mueb_vehi_tipo,mueb_vehi_marca,mueb_vehi_modelo,mueb_vehi_year,mueb_vehi_placa,mueb_vehi_carac,mueb_vehi_valor])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_bienes_muebles.txt",'a', encoding='utf-8')    
        towrite = num_dni + "\t" + str(mueb_total) 

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()


        #                                                                           
        otro_name = []
        otro_descr = []
        otro_carac = []
        otro_valor = []

        ccc_mueb = len(b.find_elements_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[3]/table/tbody/tr')) + 1
        for n in range(1,ccc_mueb):     
            try:
                otro_name.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[4]/table/tbody/tr[{0}]/td[2]/label'.format(n)).text)
            except: 
                otro_name.append("") 
            try:
                otro_descr.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[4]/table/tbody/tr[{0}]/td[3]/label'.format(n)).text)
            except:
                otro_descr.append("")

            try:
                otro_carac.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[4]/table/tbody/tr[{0}]/td[4]/label'.format(n)).text)
            except:
                otro_carac.append("")

            try:
                otro_valor.append(b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[9]/section/article[3]/div[4]/table/tbody/tr[{0}]/td[5]/label'.format(n)).text)
            except:
                otro_valor.append("")


        #Export data
        matrix = numpy.array([otro_name,otro_descr,otro_carac,otro_valor])
        ancho = len(matrix)
        largo = len(matrix[0])
        #print(ancho,largo)

        f = open("cv_bienes_muebles_otros.txt",'a', encoding='utf-8')    
        towrite = num_dni

        for i in range(0,largo):
         #   print(i)
            for j in range(0,ancho):
                towrite = towrite + "\t" + str(matrix[j][i]) 
            towrite = towrite + "\n"
            f.write(towrite)

        f.close()

        #Fecha de llenado                                      
        fech_llenado = b.find_element_by_xpath('/html/body/main/section/article/section/div/div/table/tbody/tr/td/section[11]/div/div/label[2]').text
        #Export data
        f = open("cv_fecha.txt",'a', encoding='utf-8')    
        towrite = num_dni
        varlist = [fech_llenado]
        cc = len(varlist)
        for j in range(0,cc):
            towrite = towrite + "\t" + str(varlist[j]) 
        towrite = towrite + "\n"
        f.write(towrite)
        f.close()

        print(num_dni,": Done")
        b.close()
        b.switch_to.window(window_before)
    
    except:
        print(num_dni,": No found")
        
        #export dni que no se puede descargar
        f = open("dni_no_se_puede.txt",'a', encoding='utf-8')    
        towrite = num_dni + "\t" + estado  + "\n"
        f.write(towrite)
        f.close()
        
        try: 
            window_after = b.window_handles[1]
            #switch to new window
            b.close()
            b.switch_to.window(window_before)
        except:
            print(num_dni,"Something happen")
        

