#!/usr/bin/python

# standard
import numpy as np
import pandas as pd
from pandas import Series
import random
import itertools

# Interface
import json
import mysql.connector
import string
import sys
import os

from generateDomain import generate
from domainUtil import vig_param_gen
from domainUtil import vig_gen_income
from domainUtil import vig_gen_health
from domainUtil import vig_gen_soc
from domainUtil import vig_text_string
from domainUtil import vig_domain_order
from domainUtil import vig_concatenate

def main():
	
    #Randomly select level 1-4 to generate domain for Vignettes 1 and 2
    
    levelArr = np.array([1,2,3,4])
    randLevels = np.random.choice(levelArr, 2, replace = False)
    
    vig1Level = randLevels[0].item()
    vig2Level = randLevels[1].item()
    

    # Generate domain for Vignettes 1-5
    df_domain_1 = generate(vig1Level)
    df_domain_2 = generate(vig2Level)
    df_domain_3 = generate(0)
    df_domain_4 = generate(0)
    df_domain_5 = generate(0)
    #userID = 0 #debug purpose

    #Vignettes 3-5 inherit the value of 1 domain from each previous vignettes

    swap_list = np.random.choice(11,9, replace= False)

    # Vignette 3 inherit one domain each from Vignette 1 and 2
    df_domain_3.ix[swap_list[0]] = df_domain_1.ix[swap_list[0]]
    df_domain_3.ix[swap_list[1]] = df_domain_2.ix[swap_list[1]]


    # Vignette 4 inherit one domain each from Vignette 1, 2, and 3
    df_domain_4.ix[swap_list[2]] = df_domain_1.ix[swap_list[2]]
    df_domain_4.ix[swap_list[3]] = df_domain_2.ix[swap_list[3]]
    df_domain_4.ix[swap_list[4]] = df_domain_3.ix[swap_list[4]]


    # Vignette 5 inherit one domain each from Vignette 1, 2, 3, and 4
    df_domain_5.ix[swap_list[5]] = df_domain_1.ix[swap_list[5]]
    df_domain_5.ix[swap_list[6]] = df_domain_2.ix[swap_list[6]]
    df_domain_5.ix[swap_list[7]] = df_domain_3.ix[swap_list[7]]
    df_domain_5.ix[swap_list[8]] = df_domain_4.ix[swap_list[8]]


    maleNameSel = np.random.choice(12, 5, replace = False)
    femaleNameSel = np.random.choice(12, 5, replace = False)
     

    # Vignette Parameters 1-5
    param_1 = vig_param_gen(df_domain_1, vig1Level, maleNameSel[0], femaleNameSel[0])
    param_2 = vig_param_gen(df_domain_2, vig2Level, maleNameSel[1], femaleNameSel[1])
    param_3 = vig_param_gen(df_domain_3, 0, maleNameSel[2], femaleNameSel[2])
    param_4 = vig_param_gen(df_domain_4, 0, maleNameSel[3], femaleNameSel[3])
    param_5 = vig_param_gen(df_domain_5, 0, maleNameSel[4], femaleNameSel[4])


    # Vignette Text 1-5
      
    income_ser1 = vig_gen_income(param_1)
    health_ser1 =vig_gen_health(param_1)
    soc_ser1 = vig_gen_soc(param_1)

    income_ser2 = vig_gen_income(param_2)
    health_ser2 =vig_gen_health(param_2)
    soc_ser2 = vig_gen_soc(param_2)


    income_ser3 = vig_gen_income(param_3)
    health_ser3 =vig_gen_health(param_3)
    soc_ser3 = vig_gen_soc(param_3)


    income_ser4 = vig_gen_income(param_4)
    health_ser4 =vig_gen_health(param_4)
    soc_ser4 = vig_gen_soc(param_4)

    income_ser5 = vig_gen_income(param_5)
    health_ser5 =vig_gen_health(param_5)
    soc_ser5 = vig_gen_soc(param_5)

    # Format Vignette Text for Vignettes 1-5 
    
    vig1_text_labour = vig_text_string(income_ser1, 'labour')
    vig1_text_health = vig_text_string(health_ser1, 'health')
    vig1_text_soc = vig_text_string(soc_ser1, 'social')
    
    vig2_text_labour = vig_text_string(income_ser2, 'labour')
    vig2_text_health = vig_text_string(health_ser2, 'health')
    vig2_text_soc = vig_text_string(soc_ser2, 'social')
    
    vig3_text_labour = vig_text_string(income_ser3, 'labour')
    vig3_text_health = vig_text_string(health_ser3, 'health')
    vig3_text_soc = vig_text_string(soc_ser3, 'social')
    
    vig4_text_labour = vig_text_string(income_ser4, 'labour')
    vig4_text_health = vig_text_string(health_ser4, 'health')
    vig4_text_soc = vig_text_string(soc_ser4, 'social')
    
    vig5_text_labour = vig_text_string(income_ser5, 'labour')
    vig5_text_health = vig_text_string(health_ser5, 'health')
    vig5_text_soc = vig_text_string(soc_ser5, 'social')
    
    
    #Get the "within group" order of apperance for each domain in the 
    #domain groups: Labour, Health and Social
    
    vig1LabourNameOrder, vig1LabourIDOrder = vig_domain_order(income_ser1, 'labour')
    vig1HealthNameOrder, vig1HealthIDOrder = vig_domain_order(health_ser1, 'health')
    vig1SocialNameOrder, vig1SocialIDOrder = vig_domain_order(soc_ser1, 'social')
    
    vig2LabourNameOrder, vig2LabourIDOrder = vig_domain_order(income_ser2, 'labour')
    vig2HealthNameOrder, vig2HealthIDOrder = vig_domain_order(health_ser2, 'health')
    vig2SocialNameOrder, vig2SocialIDOrder = vig_domain_order(soc_ser2, 'social')
    
    vig3LabourNameOrder, vig3LabourIDOrder = vig_domain_order(income_ser3, 'labour')
    vig3HealthNameOrder, vig3HealthIDOrder = vig_domain_order(health_ser3, 'health')
    vig3SocialNameOrder, vig3SocialIDOrder = vig_domain_order(soc_ser3, 'social')
    
    vig4LabourNameOrder, vig4LabourIDOrder = vig_domain_order(income_ser4, 'labour')
    vig4HealthNameOrder, vig4HealthIDOrder = vig_domain_order(health_ser4, 'health')
    vig4SocialNameOrder, vig4SocialIDOrder = vig_domain_order(soc_ser4, 'social')
    
    vig5LabourNameOrder, vig5LabourIDOrder = vig_domain_order(income_ser5, 'labour')
    vig5HealthNameOrder, vig5HealthIDOrder = vig_domain_order(health_ser5, 'health')
    vig5SocialNameOrder, vig5SocialIDOrder = vig_domain_order(soc_ser5, 'social')
    
   
    
    
    
    #Generate the permutation array for the between category order of the vig text
    permArray = list(itertools.permutations([1, 2, 3]))
	
	#Select a permutation (1 out of 6)
    perm1Sel = permArray[random.randint(0,5)]
    perm2Sel = permArray[random.randint(0,5)]
    perm3Sel = permArray[random.randint(0,5)]
    perm4Sel = permArray[random.randint(0,5)]
    perm5Sel = permArray[random.randint(0,5)]
	
    vig1_text = vig_concatenate(param_1['name'], vig1_text_labour, vig1_text_health, vig1_text_soc, perm1Sel)
    vig2_text = vig_concatenate(param_2['name'], vig2_text_labour, vig2_text_health, vig2_text_soc, perm2Sel)
    vig3_text = vig_concatenate(param_3['name'], vig3_text_labour, vig3_text_health, vig3_text_soc, perm3Sel)
    vig4_text = vig_concatenate(param_4['name'], vig4_text_labour, vig4_text_health, vig4_text_soc, perm4Sel)
    vig5_text = vig_concatenate(param_5['name'], vig5_text_labour, vig5_text_health, vig5_text_soc, perm5Sel)
    
    
    # Get name and gender of the hypothetical person in the vignettes to send to SQL
    Name1 = param_1['name']
    Name2 = param_2['name']
    Name3 = param_3['name']
    Name4 = param_4['name']
    Name5 = param_5['name']
    
    Gender1 = param_1['gender']
    Gender2 = param_2['gender']
    Gender3 = param_3['gender']
    Gender4 = param_4['gender']
    Gender5 = param_5['gender']
    
    #Get live with partner/live alone bool
    liveWithPartner1 = param_1['liveWithPartnerBool']
    liveWithPartner2 = param_2['liveWithPartnerBool']
    liveWithPartner3 = param_3['liveWithPartnerBool']
    liveWithPartner4 = param_4['liveWithPartnerBool']
    liveWithPartner5 = param_5['liveWithPartnerBool']
    
    #Get Reported Trust bool
    reportedTrust1 = param_1['reportedTrust']
    reportedTrust2 = param_2['reportedTrust']
    reportedTrust3 = param_3['reportedTrust']
    reportedTrust4 = param_4['reportedTrust']
    reportedTrust5 = param_5['reportedTrust']
    		
		
    # Send data to SQL
    queryVig = "UPDATE USA_vignettes_2017 SET vig1Level = %s, Vignette1Text = %s, Vignette1TextLabour = %s, Vignette1TextHealth = %s, Vignette1TextSoc = %s, Name1 = %s, Gender1 = %s, HouseHold_Income_Val_1 = %s, HouseHold_Income_Percentile_1= %s, HouseHold_Income_DataSource_1= %s, Unemployment_Rate_1 = %s, Unemployment_Rate_DataSource_1 = %s, Hours_Worked_Val_1 = %s, Hours_Worked_Percentile_1 = %s, Hours_Worked_DataSource_1 = %s, BMI_Val_1 = %s, BMI_Percentile_1 = %s, BMI_Cat_1 = %s, BMI_DataSource_1 = %s, Pain_Val_1 = %s, Pain_Percentile_1 = %s, Pain_Cat_1 = %s, Pain_DataSource_1 = %s, Phys_Val_1 = %s, Phys_Percentile_1 = %s, Phys_Cat_1 = %s, Phys_DataSource_1 = %s, NumFrds_Val_1 = %s, NumFrds_Percentile_1 = %s, NumFrds_DataSource_1 = %s, FreqFrds_Percentile_1 = %s, FreqFrds_Cat_1 = %s, FreqFrds_DataSource_1 = %s, Partner_Val_1 = %s, Partner_DataSource_1 = %s, NumOrg_Val_1 = %s, NumOrg_Percentile_1 = %s, NumOrg_DataSource_1 = %s, Trust_Val_1 = %s, Trust_DataSource_1 = %s, vig2Level = %s, Vignette2Text = %s, Vignette2TextLabour = %s, Vignette2TextHealth = %s, Vignette2TextSoc = %s, Name2 = %s, Gender2 = %s, HouseHold_Income_Val_2 = %s, HouseHold_Income_Percentile_2= %s, HouseHold_Income_DataSource_2= %s, Unemployment_Rate_2 = %s, Unemployment_Rate_DataSource_2 = %s, Hours_Worked_Val_2 = %s, Hours_Worked_Percentile_2 = %s, Hours_Worked_DataSource_2 = %s, BMI_Val_2 = %s, BMI_Percentile_2 = %s, BMI_Cat_2 = %s, BMI_DataSource_2 = %s, Pain_Val_2 = %s, Pain_Percentile_2 = %s, Pain_Cat_2 = %s, Pain_DataSource_2 = %s, Phys_Val_2 = %s, Phys_Percentile_2 = %s, Phys_Cat_2 = %s, Phys_DataSource_2 = %s, NumFrds_Val_2 = %s, NumFrds_Percentile_2 = %s, NumFrds_DataSource_2 = %s, FreqFrds_Percentile_2 = %s, FreqFrds_Cat_2 = %s, FreqFrds_DataSource_2 = %s, Partner_Val_2 = %s, Partner_DataSource_2 = %s, NumOrg_Val_2 = %s, NumOrg_Percentile_2 = %s, NumOrg_DataSource_2 = %s, Trust_Val_2 = %s, Trust_DataSource_2 = %s, Vignette3Text = %s, Vignette3TextLabour = %s, Vignette3TextHealth = %s, Vignette3TextSoc = %s, Name3 = %s, Gender3 = %s, HouseHold_Income_Val_3 = %s, HouseHold_Income_Percentile_3= %s, HouseHold_Income_DataSource_3= %s, Unemployment_Rate_3 = %s, Unemployment_Rate_DataSource_3 = %s, Hours_Worked_Val_3 = %s, Hours_Worked_Percentile_3 = %s, Hours_Worked_DataSource_3 = %s, BMI_Val_3 = %s, BMI_Percentile_3 = %s, BMI_Cat_3 = %s, BMI_DataSource_3 = %s, Pain_Val_3 = %s, Pain_Percentile_3 = %s, Pain_Cat_3 = %s, Pain_DataSource_3 = %s, Phys_Val_3 = %s, Phys_Percentile_3 = %s, Phys_Cat_3 = %s, Phys_DataSource_3 = %s, NumFrds_Val_3 = %s, NumFrds_Percentile_3 = %s, NumFrds_DataSource_3 = %s, FreqFrds_Percentile_3 = %s, FreqFrds_Cat_3 = %s, FreqFrds_DataSource_3 = %s, Partner_Val_3 = %s, Partner_DataSource_3 = %s, NumOrg_Val_3 = %s, NumOrg_Percentile_3 = %s, NumOrg_DataSource_3 = %s, Trust_Val_3 = %s, Trust_DataSource_3 = %s, Vignette4Text = %s, Vignette4TextLabour = %s, Vignette4TextHealth = %s, Vignette4TextSoc = %s, Name4 = %s, Gender4 = %s, HouseHold_Income_Val_4 = %s, HouseHold_Income_Percentile_4= %s, HouseHold_Income_DataSource_4= %s, Unemployment_Rate_4 = %s, Unemployment_Rate_DataSource_4 = %s, Hours_Worked_Val_4 = %s, Hours_Worked_Percentile_4 = %s, Hours_Worked_DataSource_4 = %s, BMI_Val_4 = %s, BMI_Percentile_4 = %s, BMI_Cat_4 = %s, BMI_DataSource_4 = %s, Pain_Val_4 = %s, Pain_Percentile_4 = %s, Pain_Cat_4 = %s, Pain_DataSource_4 = %s, Phys_Val_4 = %s, Phys_Percentile_4 = %s, Phys_Cat_4 = %s, Phys_DataSource_4 = %s, NumFrds_Val_4 = %s, NumFrds_Percentile_4 = %s, NumFrds_DataSource_4 = %s, FreqFrds_Percentile_4 = %s, FreqFrds_Cat_4 = %s, FreqFrds_DataSource_4 = %s, Partner_Val_4 = %s, Partner_DataSource_4 = %s, NumOrg_Val_4 = %s, NumOrg_Percentile_4 = %s, NumOrg_DataSource_4 = %s, Trust_Val_4 = %s, Trust_DataSource_4 = %s, Vignette5Text = %s, Vignette5TextLabour = %s, Vignette5TextHealth = %s, Vignette5TextSoc = %s, Name5 = %s, Gender5 = %s, HouseHold_Income_Val_5 = %s, HouseHold_Income_Percentile_5= %s, HouseHold_Income_DataSource_5= %s, Unemployment_Rate_5 = %s, Unemployment_Rate_DataSource_5 = %s, Hours_Worked_Val_5 = %s, Hours_Worked_Percentile_5 = %s, Hours_Worked_DataSource_5 = %s, BMI_Val_5 = %s, BMI_Percentile_5 = %s, BMI_Cat_5 = %s, BMI_DataSource_5 = %s, Pain_Val_5 = %s, Pain_Percentile_5 = %s, Pain_Cat_5 = %s, Pain_DataSource_5 = %s, Phys_Val_5 = %s, Phys_Percentile_5 = %s, Phys_Cat_5 = %s, Phys_DataSource_5 = %s, NumFrds_Val_5 = %s, NumFrds_Percentile_5 = %s, NumFrds_DataSource_5 = %s, FreqFrds_Percentile_5 = %s, FreqFrds_Cat_5 = %s, FreqFrds_DataSource_5 = %s, Partner_Val_5 = %s, Partner_DataSource_5 = %s, NumOrg_Val_5 = %s, NumOrg_Percentile_5 = %s, NumOrg_DataSource_5 = %s, Trust_Val_5 = %s, Trust_DataSource_5 = %s, Partner_Bool_1 = %s, Partner_Bool_2 = %s, Partner_Bool_3 = %s, Partner_Bool_4 = %s, Partner_Bool_5 = %s, Trust_Bool_1 = %s, Trust_Bool_2 = %s, Trust_Bool_3 = %s, Trust_Bool_4 = %s, Trust_Bool_5 = %s WHERE ID = " + str(userID);
    
    dataVig = (vig1Level, vig1_text, vig1_text_labour, vig1_text_health, vig1_text_soc, Name1, Gender1, df_domain_1['Value'].ix[0].item(), df_domain_1['Percentile'].ix[0].item(), df_domain_1['Data Source'].ix[0], df_domain_1['Value'].ix[1].item(), df_domain_1['Data Source'].ix[1], df_domain_1['Value'].ix[2].item(), df_domain_1['Percentile'].ix[2].item(), df_domain_1['Data Source'].ix[2], df_domain_1['Value'].ix[3].item(), df_domain_1['Percentile'].ix[3].item(), df_domain_1['Category'].ix[3], df_domain_1['Data Source'].ix[3], df_domain_1['Value'].ix[4].item(), df_domain_1['Percentile'].ix[4].item(), df_domain_1['Category'].ix[4], df_domain_1['Data Source'].ix[4], df_domain_1['Value'].ix[5].item(), df_domain_1['Percentile'].ix[5].item(), df_domain_1['Category'].ix[5], df_domain_1['Data Source'].ix[5], df_domain_1['Value'].ix[6].item(), df_domain_1['Percentile'].ix[6].item(), df_domain_1['Data Source'].ix[6], df_domain_1['Percentile'].ix[7].item(), df_domain_1['Category'].ix[7], df_domain_1['Data Source'].ix[7], df_domain_1['Value'].ix[8].item(), df_domain_1['Data Source'].ix[8], df_domain_1['Value'].ix[9].item(), df_domain_1['Percentile'].ix[9].item(), df_domain_1['Data Source'].ix[9], df_domain_1['Value'].ix[10].item(), df_domain_1['Data Source'].ix[10], vig2Level, vig2_text, vig2_text_labour, vig2_text_health, vig2_text_soc, Name2, Gender2, df_domain_2['Value'].ix[0].item(), df_domain_2['Percentile'].ix[0].item(), df_domain_2['Data Source'].ix[0], df_domain_2['Value'].ix[1].item(), df_domain_2['Data Source'].ix[1], df_domain_2['Value'].ix[2].item(), df_domain_2['Percentile'].ix[2].item(), df_domain_2['Data Source'].ix[2], df_domain_2['Value'].ix[3].item(), df_domain_2['Percentile'].ix[3].item(), df_domain_2['Category'].ix[3], df_domain_2['Data Source'].ix[3], df_domain_2['Value'].ix[4].item(), df_domain_2['Percentile'].ix[4].item(), df_domain_2['Category'].ix[4], df_domain_2['Data Source'].ix[4], df_domain_2['Value'].ix[5].item(), df_domain_2['Percentile'].ix[5].item(), df_domain_2['Category'].ix[5], df_domain_2['Data Source'].ix[5], df_domain_2['Value'].ix[6].item(), df_domain_2['Percentile'].ix[6].item(), df_domain_2['Data Source'].ix[6], df_domain_2['Percentile'].ix[7].item(), df_domain_2['Category'].ix[7], df_domain_2['Data Source'].ix[7], df_domain_2['Value'].ix[8].item(), df_domain_2['Data Source'].ix[8], df_domain_2['Value'].ix[9].item(), df_domain_2['Percentile'].ix[9].item(), df_domain_2['Data Source'].ix[9], df_domain_2['Value'].ix[10].item(), df_domain_2['Data Source'].ix[10], vig3_text, vig3_text_labour, vig3_text_health, vig3_text_soc, Name3, Gender3, df_domain_3['Value'].ix[0].item(), df_domain_3['Percentile'].ix[0].item(), df_domain_3['Data Source'].ix[0], df_domain_3['Value'].ix[1].item(), df_domain_3['Data Source'].ix[1], df_domain_3['Value'].ix[2].item(), df_domain_3['Percentile'].ix[2].item(), df_domain_3['Data Source'].ix[2], df_domain_3['Value'].ix[3].item(), df_domain_3['Percentile'].ix[3].item(), df_domain_3['Category'].ix[3], df_domain_3['Data Source'].ix[3], df_domain_3['Value'].ix[4].item(), df_domain_3['Percentile'].ix[4].item(), df_domain_3['Category'].ix[4], df_domain_3['Data Source'].ix[4], df_domain_3['Value'].ix[5].item(), df_domain_3['Percentile'].ix[5].item(), df_domain_3['Category'].ix[5], df_domain_3['Data Source'].ix[5], df_domain_3['Value'].ix[6].item(), df_domain_3['Percentile'].ix[6].item(), df_domain_3['Data Source'].ix[6], df_domain_3['Percentile'].ix[7].item(), df_domain_3['Category'].ix[7], df_domain_3['Data Source'].ix[7], df_domain_3['Value'].ix[8].item(), df_domain_3['Data Source'].ix[8], df_domain_3['Value'].ix[9].item(), df_domain_3['Percentile'].ix[9].item(), df_domain_3['Data Source'].ix[9], df_domain_3['Value'].ix[10].item(), df_domain_3['Data Source'].ix[10], vig4_text, vig4_text_labour, vig4_text_health, vig4_text_soc, Name4, Gender4, df_domain_4['Value'].ix[0].item(), df_domain_4['Percentile'].ix[0].item(), df_domain_4['Data Source'].ix[0], df_domain_4['Value'].ix[1].item(), df_domain_4['Data Source'].ix[1], df_domain_4['Value'].ix[2].item(), df_domain_4['Percentile'].ix[2].item(), df_domain_4['Data Source'].ix[2], df_domain_4['Value'].ix[3].item(), df_domain_4['Percentile'].ix[3].item(), df_domain_4['Category'].ix[3], df_domain_4['Data Source'].ix[3], df_domain_4['Value'].ix[4].item(), df_domain_4['Percentile'].ix[4].item(), df_domain_4['Category'].ix[4], df_domain_4['Data Source'].ix[4], df_domain_4['Value'].ix[5].item(), df_domain_4['Percentile'].ix[5].item(), df_domain_4['Category'].ix[5], df_domain_4['Data Source'].ix[5], df_domain_4['Value'].ix[6].item(), df_domain_4['Percentile'].ix[6].item(), df_domain_4['Data Source'].ix[6], df_domain_4['Percentile'].ix[7].item(), df_domain_4['Category'].ix[7], df_domain_4['Data Source'].ix[7], df_domain_4['Value'].ix[8].item(), df_domain_4['Data Source'].ix[8], df_domain_4['Value'].ix[9].item(), df_domain_4['Percentile'].ix[9].item(), df_domain_4['Data Source'].ix[9], df_domain_4['Value'].ix[10].item(), df_domain_4['Data Source'].ix[10], vig5_text, vig5_text_labour, vig5_text_health, vig5_text_soc, Name5, Gender5, df_domain_5['Value'].ix[0].item(), df_domain_5['Percentile'].ix[0].item(), df_domain_5['Data Source'].ix[0], df_domain_5['Value'].ix[1].item(), df_domain_5['Data Source'].ix[1], df_domain_5['Value'].ix[2].item(), df_domain_5['Percentile'].ix[2].item(), df_domain_5['Data Source'].ix[2], df_domain_5['Value'].ix[3].item(), df_domain_5['Percentile'].ix[3].item(), df_domain_5['Category'].ix[3], df_domain_5['Data Source'].ix[3], df_domain_5['Value'].ix[4].item(), df_domain_5['Percentile'].ix[4].item(), df_domain_5['Category'].ix[4], df_domain_5['Data Source'].ix[4], df_domain_5['Value'].ix[5].item(), df_domain_5['Percentile'].ix[5].item(), df_domain_5['Category'].ix[5], df_domain_5['Data Source'].ix[5], df_domain_5['Value'].ix[6].item(), df_domain_5['Percentile'].ix[6].item(), df_domain_5['Data Source'].ix[6], df_domain_5['Percentile'].ix[7].item(), df_domain_5['Category'].ix[7], df_domain_5['Data Source'].ix[7], df_domain_5['Value'].ix[8].item(), df_domain_5['Data Source'].ix[8], df_domain_5['Value'].ix[9].item(), df_domain_5['Percentile'].ix[9].item(), df_domain_5['Data Source'].ix[9], df_domain_5['Value'].ix[10].item(), df_domain_5['Data Source'].ix[10], liveWithPartner1, liveWithPartner2, liveWithPartner3, liveWithPartner4, liveWithPartner5, reportedTrust1, reportedTrust2, reportedTrust3, reportedTrust4, reportedTrust5)
    
    
    
    queryVigOrder = "UPDATE USA_vignettes_order_2017 SET vig1LabourName1 = %s, vig1LabourID1 = %s, vig1LabourName2 = %s, vig1LabourID2 = %s, vig1HealthName1 = %s, vig1HealthID1 = %s, vig1HealthName2 = %s, vig1HealthID2 = %s, vig1HealthName3 = %s, vig1HealthID3 = %s, vig1SocialName1 = %s, vig1SocialID1 = %s, vig1SocialName2 = %s, vig1SocialID2 = %s, vig1SocialName3 = %s, vig1SocialID3 = %s, vig1SocialName4 = %s, vig1SocialID4 = %s, vig1SocialName5 = %s, vig1SocialID5 = %s, vig2LabourName1 = %s, vig2LabourID1 = %s, vig2LabourName2 = %s, vig2LabourID2 = %s, vig2HealthName1 = %s, vig2HealthID1 = %s, vig2HealthName2 = %s, vig2HealthID2 = %s, vig2HealthName3 = %s, vig2HealthID3 = %s, vig2SocialName1 = %s, vig2SocialID1 = %s, vig2SocialName2 = %s, vig2SocialID2 = %s, vig2SocialName3 = %s, vig2SocialID3 = %s, vig2SocialName4 = %s, vig2SocialID4 = %s, vig2SocialName5 = %s, vig2SocialID5 = %s, vig3LabourName1 = %s, vig3LabourID1 = %s, vig3LabourName2 = %s, vig3LabourID2 = %s, vig3HealthName1 = %s, vig3HealthID1 = %s, vig3HealthName2 = %s, vig3HealthID2 = %s, vig3HealthName3 = %s, vig3HealthID3 = %s, vig3SocialName1 = %s, vig3SocialID1 = %s, vig3SocialName2 = %s, vig3SocialID2 = %s, vig3SocialName3 = %s, vig3SocialID3 = %s, vig3SocialName4 = %s, vig3SocialID4 = %s, vig3SocialName5 = %s, vig3SocialID5 = %s, vig4LabourName1 = %s, vig4LabourID1 = %s, vig4LabourName2 = %s, vig4LabourID2 = %s, vig4HealthName1 = %s, vig4HealthID1 = %s, vig4HealthName2 = %s, vig4HealthID2 = %s, vig4HealthName3 = %s, vig4HealthID3 = %s, vig4SocialName1 = %s, vig4SocialID1 = %s, vig4SocialName2 = %s, vig4SocialID2 = %s, vig4SocialName3 = %s, vig4SocialID3 = %s, vig4SocialName4 = %s, vig4SocialID4 = %s, vig4SocialName5 = %s, vig4SocialID5 = %s, vig5LabourName1 = %s, vig5LabourID1 = %s, vig5LabourName2 = %s, vig5LabourID2 = %s, vig5HealthName1 = %s, vig5HealthID1 = %s, vig5HealthName2 = %s, vig5HealthID2 = %s, vig5HealthName3 = %s, vig5HealthID3 = %s, vig5SocialName1 = %s, vig5SocialID1 = %s, vig5SocialName2 = %s, vig5SocialID2 = %s, vig5SocialName3 = %s, vig5SocialID3 = %s, vig5SocialName4 = %s, vig5SocialID4 = %s, vig5SocialName5 = %s, vig5SocialID5 = %s, vig1CatOrder1 = %s, vig1CatOrder2 = %s, vig1CatOrder3 = %s, vig2CatOrder1 = %s, vig2CatOrder2 = %s, vig2CatOrder3 = %s, vig3CatOrder1 = %s, vig3CatOrder2 = %s, vig3CatOrder3 = %s, vig4CatOrder1 = %s, vig4CatOrder2 = %s, vig4CatOrder3 = %s, vig5CatOrder1 = %s, vig5CatOrder2 = %s, vig5CatOrder3 = %s WHERE ID = " + str(userID);
    
    dataVigOrder = (vig1LabourNameOrder[0], vig1LabourIDOrder[0], vig1LabourNameOrder[1], vig1LabourIDOrder[1], vig1HealthNameOrder[0], vig1HealthIDOrder[0], vig1HealthNameOrder[1], vig1HealthIDOrder[1], vig1HealthNameOrder[2], vig1HealthIDOrder[2], vig1SocialNameOrder[0], vig1SocialIDOrder[0], vig1SocialNameOrder[1], vig1SocialIDOrder[1], vig1SocialNameOrder[2], vig1SocialIDOrder[2], vig1SocialNameOrder[3], vig1SocialIDOrder[3], vig1SocialNameOrder[4], vig1SocialIDOrder[4], vig2LabourNameOrder[0], vig2LabourIDOrder[0], vig2LabourNameOrder[1], vig2LabourIDOrder[1], vig2HealthNameOrder[0], vig2HealthIDOrder[0], vig2HealthNameOrder[1], vig2HealthIDOrder[1], vig2HealthNameOrder[2], vig2HealthIDOrder[2], vig2SocialNameOrder[0], vig2SocialIDOrder[0], vig2SocialNameOrder[1], vig2SocialIDOrder[1], vig2SocialNameOrder[2], vig2SocialIDOrder[2], vig2SocialNameOrder[3], vig2SocialIDOrder[3], vig2SocialNameOrder[4], vig2SocialIDOrder[4], vig3LabourNameOrder[0], vig3LabourIDOrder[0], vig3LabourNameOrder[1], vig3LabourIDOrder[1], vig3HealthNameOrder[0], vig3HealthIDOrder[0], vig3HealthNameOrder[1], vig3HealthIDOrder[1], vig3HealthNameOrder[2], vig3HealthIDOrder[2], vig3SocialNameOrder[0], vig3SocialIDOrder[0], vig3SocialNameOrder[1], vig3SocialIDOrder[1], vig3SocialNameOrder[2], vig3SocialIDOrder[2], vig3SocialNameOrder[3], vig3SocialIDOrder[3], vig3SocialNameOrder[4], vig3SocialIDOrder[4], vig4LabourNameOrder[0], vig4LabourIDOrder[0], vig4LabourNameOrder[1], vig4LabourIDOrder[1], vig4HealthNameOrder[0], vig4HealthIDOrder[0], vig4HealthNameOrder[1], vig4HealthIDOrder[1], vig4HealthNameOrder[2], vig4HealthIDOrder[2], vig4SocialNameOrder[0], vig4SocialIDOrder[0], vig4SocialNameOrder[1], vig4SocialIDOrder[1], vig4SocialNameOrder[2], vig4SocialIDOrder[2], vig4SocialNameOrder[3], vig4SocialIDOrder[3], vig4SocialNameOrder[4], vig4SocialIDOrder[4], vig5LabourNameOrder[0], vig5LabourIDOrder[0], vig5LabourNameOrder[1], vig5LabourIDOrder[1], vig5HealthNameOrder[0], vig5HealthIDOrder[0], vig5HealthNameOrder[1], vig5HealthIDOrder[1], vig5HealthNameOrder[2], vig5HealthIDOrder[2], vig5SocialNameOrder[0], vig5SocialIDOrder[0], vig5SocialNameOrder[1], vig5SocialIDOrder[1], vig5SocialNameOrder[2], vig5SocialIDOrder[2], vig5SocialNameOrder[3], vig5SocialIDOrder[3], vig5SocialNameOrder[4], vig5SocialIDOrder[4],perm1Sel[0], perm1Sel[1], perm1Sel[2], perm2Sel[0], perm2Sel[1], perm2Sel[2], perm3Sel[0], perm3Sel[1], perm3Sel[2], perm4Sel[0], perm4Sel[1], perm4Sel[2], perm5Sel[0], perm5Sel[1], perm5Sel[2])
   
 
   
  
    cur.execute(queryVig, dataVig)
    cur.execute(queryVigOrder, dataVigOrder)
    
    dbConnect.commit()
    cur.close()
    dbConnect.close()

   
if __name__ == '__main__':
	dbConnect = mysql.connector.connect(user="henryfung", password="mtuarsftqq", database="vignettes_live")
	cur = dbConnect.cursor()
	userID = sys.argv[1]
	main()

  


