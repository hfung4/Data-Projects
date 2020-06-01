# standard
import random
import numpy as np
import pandas as pd
from pandas import DataFrame

from domainUtil import income_df_gen
from domainUtil import distribution_gen
from domainUtil import BMI_output_gen
from domainUtil import bmi_cat_gen
from domainUtil import pain_cat_gen
from domainUtil import freq_frd_cat_gen


def generate(level):
    # HouseHold Income (income_arr)
    incomeFileName = "/home/projects/vignettes/web/webDev/domainGen/data/incomeWorkData/HouseholdIncomeData.csv"
    df_income = income_df_gen(incomeFileName, random.randint(0, 508))
    incomeSrc = df_income.index.name
    income_arr = distribution_gen(df_income, 'Probability', 250000.0, 5000.0, 'income', level) 
    income_arr[2] = 'NA'
    income_arr[3] = incomeSrc
     

    # Unemployment Rate (unemploy_arr)
    unemployFileName = "/home/projects/vignettes/web/webDev/domainGen/data/incomeWorkData/UnemploymentRateData.csv"
    df_employ = pd.read_csv(unemployFileName)
    unemploySel = random.randint(0, 504)
    unemployment_rate = round(df_employ['Unemployment rate'].ix[unemploySel] * 100, 3)
    unemployment_src = df_employ['Geography'].ix[unemploySel]
    unemploy_arr = [unemployment_rate, 0, 'NA', unemployment_src]

    # Hours Worked (hrWorked_arr)
    hrWorkedFileName = "/home/projects/vignettes/web/webDev/domainGen/data/incomeWorkData/hoursWorkedData.csv"
    hrWorkSel = ["Comm1", "Comm2", "Comm3"]
    hrWorkRandom = random.randint(0, 2)
    hrWorkedSrc = hrWorkSel[hrWorkRandom]
    df_hrWorked = pd.read_csv(hrWorkedFileName, usecols=[hrWorkedSrc]) * 0.05
    hrWorked_arr = distribution_gen(df_hrWorked, hrWorkedSrc, 65.0, 0.05, 'Hours_Worked', level)
    hrWorked_arr[2] = 'NA'
    hrWorked_arr[3] = hrWorkedSrc

    # BMI (BMI_arr)
    
    # Select BMI data from a Province 
    BMI_PDF_FileName = "/home/projects/vignettes/web/webDev/domainGen/data/healthData/BMI_skewnorm_pdf.csv"
    BMI_CDF_FileName = "/home/projects/vignettes/web/webDev/domainGen/data/healthData/BMI_skewnorm_cdf.csv"
    BMISel = ["Newfoundland", "PEI", "Nova Scotia", "New Brunswick", "Quebec", "Ontario",
           "Manitoba", "Saskatchewan", "Alberta"]
           
    BMIRandom = random.randint(0, 8)
    BMISrc = BMISel[BMIRandom]
    
    # The BMI data (read from csv) are normalized skew norm fit pdf and cdf data for each province 
    # (Skew norm fit was perform on the actual BMI data offline, and the results are stored in the csv)
    df_BMI_pdf = pd.read_csv(BMI_PDF_FileName, usecols=[BMISrc])
    df_BMI_cdf = pd.read_csv(BMI_CDF_FileName, usecols=[BMISrc])
      
    # Select BMI based on the distribution and level
    BMIGen = BMI_output_gen(df_BMI_pdf, BMISrc, level)
    	
	# Generate cdf of the skew norm distribution based on the parameters
    BMISkewNormCdf = np.array(df_BMI_cdf[BMISrc].values)

    # Get position of the selected BMI in the array
    temp = int((BMIGen - 16.0)/0.5)

	# Get the percentile from the CDF
    BMI_percentile = round(BMISkewNormCdf[temp] * 100, 2)
	
	# Get the BMI category
    BMICat = bmi_cat_gen(BMIGen)

	# Put everything in the BMI array
    BMI_arr = [BMIGen, BMI_percentile, BMICat, BMISrc]


    # Pain or Discomfort

    # Use hypothetical community data
    # Comm1: Most people have no pain
    # Comm2: Most people have no pain or severe pain
    # Comm3: Most people have mild or moderate pain
    # Comm4: Most people have no pain or mild pain
    # Comm5: Most people have moderate or severe pain

    PainFileName = "/home/projects/vignettes/web/webDev/domainGen/data/healthData/PADDataCdnProv.csv"
    PainSel = ["Comm 1", "Comm 2", "Comm 3", "Comm 4", "Comm 5"]
    painRandom = random.randint(0, 4)
    painSrc = PainSel[painRandom]
    df_pain = pd.read_csv(PainFileName, usecols=[painSrc])
    pain_arr = distribution_gen(df_pain, painSrc, 4.0, 1.0, 'pain', level)
    pain_level = int(pain_arr[0])
    painCat = pain_cat_gen(pain_level)
    pain_arr[2] = painCat
    pain_arr[3] = painSrc

    # Frequency of Exercise

    # Use hypothetical community data
    # Comm1: Most people are inactive
    # Comm2: Most people are moderately active or active
    # Comm3: Most people are moderately active

    PhysFileName = "/home/projects/vignettes/web/webDev/domainGen/data/healthData/PhysHypData.csv"
    PhysSel = ["PEI", "New Brunswick", "Ontario", "BC", "Comm1", "Comm2", "Comm3"]

    # Select from data for Canadian Province/Hypothetical Data
    # (to introduce more variance between communities)
    physRandom = random.randint(0, 6)
    physSrc = PhysSel[physRandom]
    df_phys = pd.read_csv(PhysFileName, usecols=[physSrc])
    phys_arr = distribution_gen(df_phys, physSrc, 120.0, 30.0, 'phys', level)
    phys_arr[3] = physSrc

    # Number of close friends
    NumFrdFileName = "/home/projects/vignettes/web/webDev/domainGen/data/socialData/FrdNumData.csv"
    NumFrdSel = ["Comm1", "Comm2", "Comm3"]
    numFrdRandom = random.randint(0, 2)
    numFrdSrc = NumFrdSel[numFrdRandom]
    df_num_frd = pd.read_csv(NumFrdFileName, usecols=[numFrdSrc])
    num_frd_arr = distribution_gen(df_num_frd, numFrdSrc, 14.0, 1.0, 'numFrd', level)
    num_frd_arr[2] = 'NA'
    num_frd_arr[3] = numFrdSrc

    # Frequency of contacting friends
    FreqFrdFileName = "/home/projects/vignettes/web/webDev/domainGen/data/socialData/FrdFreqData.csv"
    FreqFrdSel = ["Comm1", "Comm2", "Comm3"]
    freqFrdRandom = random.randint(0, 2)
    freqFrdSrc = FreqFrdSel[freqFrdRandom]
    df_freq_frd = pd.read_csv(FreqFrdFileName, usecols=[freqFrdSrc])
    freq_frd_arr = distribution_gen(df_freq_frd, freqFrdSrc, 4.0, 1.0, 'freqFrd', level)
    freq_frd_level = int(freq_frd_arr[0])
    freq_frd_arr[2] = freq_frd_cat_gen(freq_frd_level)
    freq_frd_arr[3] = freqFrdSrc

    # Number of community organizations involved in the past 12 months
    OrgNumFileName = "/home/projects/vignettes/web/webDev/domainGen/data/socialData/OrgNumData.csv"
    OrgNumSel = ["Comm1", "Comm2", "Comm3", "Comm4", "Comm5"]
    orgNumRandom = random.randint(0, 4)
    orgNumSrc = OrgNumSel[orgNumRandom]
    df_org_num = pd.read_csv(OrgNumFileName, usecols=[orgNumSrc])
    org_num_arr = distribution_gen(df_org_num, orgNumSrc, 5.0, 1.0, 'orgNum', level)
    org_num_arr[2] = 'NA'
    org_num_arr[3] = orgNumSrc


    # Living Alone/Living with a partner
    partnerFileName = "/home/projects/vignettes/web/webDev/domainGen/data/socialData/livingPartnerHypData.csv"
    df_partner = pd.read_csv(partnerFileName)
    #partnerSel = random.randint(0, 187)  (Use real data)
    partnerSel = random.randint(0, 9)  
    
    livingPartnerRate = round(df_partner['Live with a partner'].ix[partnerSel] * 100, 3)
    partner_src = df_partner['Geography'].ix[partnerSel]
    partner_arr = [livingPartnerRate, 0, 'NA', partner_src]

    # General Trust
    trustFileName = "/home/projects/vignettes/web/webDev/domainGen/data/socialData/GenTrustHypData.csv"
    df_trust = pd.read_csv(trustFileName)
    trustSel = random.randint(0, 9)  #Introduce new hyp data
    trustRate = round(df_trust['Probability'].ix[trustSel] * 100, 3)
    trust_arr = [trustRate, 0, 'NA', trustSel]


    # Construct DataFrame containing domain absolute and relative data
    domain_df = DataFrame(np.zeros(44).reshape(11, 4),
                          index=['Household Income', 'Unemployment Rate', 'Weekly Hours Worked',
                                 'BMI', 'Pain', 'Frequency of Exercise',
                                 'Number of Friends', 'Frequency of Friends', 'Living with Partner',
                                 'Number of Org', 'General Trust'],
                          columns=['Value', 'Percentile', 'Category', 'Data Source'])

    domain_df.ix['Household Income'] = income_arr
    domain_df.ix['Unemployment Rate'] = unemploy_arr
    domain_df.ix['Weekly Hours Worked'] = hrWorked_arr

    domain_df.ix['BMI'] = BMI_arr
    domain_df.ix['Pain'] = pain_arr
    domain_df.ix['Frequency of Exercise'] = phys_arr

    domain_df.ix['Number of Friends'] = num_frd_arr
    domain_df.ix['Frequency of Friends'] = freq_frd_arr
    domain_df.ix['Living with Partner'] = partner_arr

    domain_df.ix['Number of Org'] = org_num_arr
    domain_df.ix['General Trust'] = trust_arr

    return domain_df



