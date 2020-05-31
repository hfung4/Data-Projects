# standard
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import random
from sklearn.utils import shuffle
# Stats
from scipy import stats
from scipy.interpolate import interp1d

def distribution_gen(df_p, col_name, size, inc, dom_type, level):
    
    xk = np.arange(0.0, size, inc)
    pk = df_p[col_name].values
    
    domain_rv = stats.rv_discrete(values=(xk, pk))

    # Interpolation data for cdf
    y_cdf = domain_rv.cdf(xk)
    cdf_interpolate = interp1d(xk, y_cdf, kind='linear')

    category = ""
    dataSrc = ""
    
   
    # Special processing for phys
    if dom_type == 'phys':
		
		if level == 0:
			output = np.random.choice(xk, 1, p=pk)[0]
			#output = domain_rv.rvs()
		else:
			output = level_output_gen(xk, pk, dom_type, level)
		
		
		max_rand = 0
		min_rand = 0

		if output == 0:  # Inactive (0 min)
			max_rand = 0
			min_rand = 0
			category = "inactive"
		elif output == 30:  # Inactive (0-29 min)
			max_rand = 30
			min_rand = 1
			category = "inactive"
		elif output == 60:  # Moderately Active (30-59 min)
			max_rand = 30
			min_rand = 1
			category = "moderately active"
		elif output == 90:  # Active (60-90 min)
			max_rand = 30
			min_rand = 0
			category = "active"

		output = output - random.randint(min_rand, max_rand)  # Randomly select a time from each bin
		percentile = cdf_interpolate(output)
		percentile = round((percentile * 100), 2)
		output_arr = np.array([output, percentile, category, dataSrc], dtype='O')
		return output_arr

    else:
		
		if level == 0:
			output = np.random.choice(xk, 1, p=pk)[0]
		else:
			output = level_output_gen(xk, pk, dom_type, level)
        
    percentile = domain_rv.cdf(output)
    percentile = round((percentile * 100), 2)
    output_arr = np.array([output, percentile, category, dataSrc], dtype='O')

    return output_arr


# Helper function to generate income dataframe
def income_df_gen(filename, rand_select):
    df_raw = pd.read_csv(filename)
    df_sel = df_raw.ix[rand_select]
    data_src_name = df_sel.ix[0]

    # init df_processed with 51 rows
    index = range(0, 50)
    df_p = DataFrame(np.zeros([50, 1]), index=index, columns=['Probability'])

    # populate df_processed with probabilities from the df_raw

    # 0-10000 (2 categories)
    for i in range(0, 2):
        df_p.ix[i] = df_sel.ix[1] / 2

    # 10000-14999
    df_p.ix[2] = df_sel.ix[2]

    # 15000-24999 (2 categories)
    for i in range(3, 5):
        df_p.ix[i] = df_sel.ix[3] / 2

    # 25000-34999 (2 categories)
    for i in range(5, 7):
        df_p.ix[i] = df_sel.ix[4] / 2

    # 35000-49999 (3 categories)
    for i in range(7, 10):
        df_p.ix[i] = df_sel.ix[5] / 3

    # 50000-74999 (5 categories)
    for i in range(10, 15):
        df_p.ix[i] = df_sel.ix[6] / 5

    # 75000-99999 (5 categories)
    for i in range(15, 20):
        df_p.ix[i] = df_sel.ix[7] / 5

    # 100000-149999 (10 categories)
    for i in range(20, 30):
        df_p.ix[i] = df_sel.ix[8] / 10

    # 150000-200000 (10 categories)
    for i in range(30, 40):
        df_p.ix[i] = df_sel.ix[9] / 10

    # 200000-250000 (10 categories)
    for i in range(40, 50):
        df_p.ix[i] = df_sel.ix[10] / 10

    # Ensure sum of probability is 1 (correct small rounding error)
    diff = 1.0 - df_p.sum()
    for i in range(0, 50):
        df_p.ix[i] = df_p.ix[i] + diff / 50

    df_p[data_src_name] = np.arange(0, 250000, 5000)
    df_p = df_p.set_index(data_src_name)

    return df_p


# Helper function to randomly select
# from distribution based on level for 
# income, hours worked, pain, phys, numfrd, freqfrd, and orgnum
def level_output_gen(xk, pk, dom_type, level):
	
	output = 0
	
	# level 3 mode 0   (3_0):  high income, high working hours
	# level 3 mode 1   (3_1):  very high income, very high working hours
	
	# level 4:  very high income, high working hours
	incomeWorkMode = random.randint(0,1)
	
	
	# level 1 mode 0:  severe pain

	# level 1 mode 1:  moderate pain
	# level 2 mode 0:  moderate pain
	
	# level 2 mode 1:  mild pain 
	# level 3 mode 0:  mild pain
	
	# level 4: no pain
	# level 3 mode 1:  no pain	
	painMode = random.randint(0,1)
	

	if (dom_type == 'income'):
		
		if level == 1: # 0 to 25000
			xk_p = np.array(xk[0:6])  
			pk_p = np.array(pk[0:6]) 
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif level == 2: # 30000 to 55000
			xk_p = np.array(xk[6:12])  
			pk_p = np.array(pk[6:12]) 
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif (level == 3 and incomeWorkMode == 0): # 60000 to 95000
			xk_p = np.array(xk[12:20])  
			pk_p = np.array(pk[12:20]) 
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif ((level ==4) or (level == 3 and incomeWorkMode == 1)): # 100000 to 245000
			xk_p = np.array(xk[20:50])  
			pk_p = np.array(pk[20:50]) 
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
	
	if (dom_type == 'Hours_Worked'):
		
		if level == 1:  # [0 h ,15 h]   (0 to 300)
			xk_p = np.array(xk[0:300])  
			pk_p = np.array(pk[0:300])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif level == 2:  # (15h,32h]  (301 to 640)
			xk_p = np.array(xk[301:640])  
			pk_p = np.array(pk[301:640])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif ((level == 4) or (level == 3 and incomeWorkMode == 0)):  # (32h,45h]  (641 to 900) 
			xk_p = np.array(xk[641:900])  
			pk_p = np.array(pk[641:900])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif (level == 3 and incomeWorkMode == 1):  #(45h, 65h]   (901 to 1300)
			xk_p = np.array(xk[901:1300])  
			pk_p = np.array(pk[901:1300])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
	
	if(dom_type == 'pain'):
		
		if (level == 1 and painMode == 0):
			output = 0
		elif (level == 2 and painMode == 0) or (level == 1 and painMode == 1):
			output = 1
		elif (level == 2 and painMode == 1) or (level == 3 and painMode == 0) :
			output = 2
		elif (level == 4) or (level == 3 and painMode == 1):
			output = 3
	
	if(dom_type == 'phys'):
		if (level == 1) or (level == 2):
			output = 30
		elif (level == 3):
			output = 60
		elif (level == 4):
			output = 90
			
	if(dom_type == 'numFrd'):
		if level == 1:
			xk_p = np.array(xk[0:2])  
			pk_p = np.array(pk[0:2])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif level == 2:
			xk_p = np.array(xk[2:4])  
			pk_p = np.array(pk[2:4])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]			
		elif level == 3:
			xk_p = np.array(xk[4:7])  
			pk_p = np.array(pk[4:7])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		elif level == 4:
			xk_p = np.array(xk[7:13])  
			pk_p = np.array(pk[7:13])
			pk_p = pk_p/sum(pk_p)
			output = np.random.choice(xk_p, 1, p=pk_p)[0]
		
	if(dom_type == 'freqFrd'):
		output = level - 1
		return output
		
	if(dom_type == 'orgNum'):
		if level == 1:
			output = 0
		elif level == 2:
			output = 1
		elif level == 3:
			output = random.randint(2,3)
		elif level == 4:
			output = 4
			
		
	return output


# Helper function to randomly select
# from distribution based on level for BMI 
def BMI_output_gen(df_pdf, BMISrc, level):
	
	# Support of the distribution
    BMI_x = np.arange(16, 44, 0.5)

	# Put pdf in a numpy array
    BMI_y = np.array(df_pdf[BMISrc].values)

    BMIGen = 0

    if level == 0:
		BMIGen = np.random.choice(BMI_x, 1, p=BMI_y)[0]

    elif level == 1:

        # Level 1:  BMI 16 to 18,  40 to 44
        BMI_x_level_1 = BMI_x[((BMI_x >= 16) & (BMI_x <= 18)) | ((BMI_x >= 40) & (BMI_x <= 44))]
        BMI_level1_indices =  np.where(((BMI_x >= 16) & (BMI_x <= 18)) | ((BMI_x >= 40) & (BMI_x <= 44)))
        BMI_y_level_1 = BMI_y[BMI_level1_indices]
        BMI_y_level_1_norm =  BMI_y_level_1/sum(BMI_y_level_1)
        BMIGen = np.random.choice(BMI_x_level_1, 1, p= BMI_y_level_1_norm)[0]
        
    elif level == 2:

        # Level 2: BMI is between 25 to 40
        BMI_x_level_2 = BMI_x[(BMI_x >= 25) & (BMI_x <= 40)]
        BMI_level2_indices = np.where((BMI_x >= 25) & (BMI_x <= 40))
        BMI_y_level_2 = BMI_y[BMI_level2_indices]
        BMI_y_level_2_norm = BMI_y_level_2 / sum(BMI_y_level_2)

        BMIGen = np.random.choice(BMI_x_level_2, 1, p=BMI_y_level_2_norm)[0]

    elif level == 3:

        # Level 3: BMI is between 18 to 30
        BMI_x_level_3 = BMI_x[(BMI_x >= 18) & (BMI_x <= 30)]
        BMI_level3_indices = np.where((BMI_x >= 18) & (BMI_x <= 30))
        BMI_y_level_3 = BMI_y[BMI_level3_indices]
        BMI_y_level_3_norm = BMI_y_level_3 / sum(BMI_y_level_3)

        BMIGen = np.random.choice(BMI_x_level_3, 1, p=BMI_y_level_3_norm)[0]

    elif level == 4:

        # Level 4: BMI is between 18 to 25
        BMI_x_level_4 = BMI_x[(BMI_x >= 18) & (BMI_x <= 25)]
        BMI_level4_indices = np.where((BMI_x >= 18) & (BMI_x <= 25))
        BMI_y_level_4 = BMI_y[BMI_level4_indices]
        BMI_y_level_4_norm = BMI_y_level_4/ sum(BMI_y_level_4)

        BMIGen = np.random.choice(BMI_x_level_4, 1, p=BMI_y_level_4_norm)[0]
    
    return BMIGen





# Helper function to generate BMI Categories
def bmi_cat_gen(x):
    if x < 18.5:
        cat = "underweight"
    elif x >= 18.5 and x < 25:
        cat = "normal weight"
    elif x >= 25 and x < 30:
        cat = "overweight"
    elif x >= 30 and x < 35:
        cat = "low risk obesity"
    elif x >= 35 and x < 40:
        cat = "moderate risk obesity"
    elif x >= 40:
        cat = "high risk obesity"

    return cat


# Helper function to generate Pain Categories
def pain_cat_gen(x):
    if x == 0:
        pain = 'a severe level of pain or discomfort'
    elif x == 1:
        pain = 'a moderate level of pain or discomfort'
    elif x == 2:
        pain = 'a mild level of pain or discomfort'
    elif x == 3:
        pain = 'no pain or discomfort'
    return pain


# Helper function to generate Frequency of contacting friends Categories
def freq_frd_cat_gen(x):
    if x == 0:
        frd_freq = 'rarely and did not make any contact in the past month'
    elif x == 1:
        frd_freq = 'one to three times per month'
    elif x == 2:
        frd_freq = 'once a week or more'
    elif x == 3:
        frd_freq = 'every day'
    return frd_freq


# Helper function to generate Vignette string format parameters
def vig_param_gen(df_domain, level, maleNameSel, femaleNameSel):

    #init the param output Series

    param = Series(np.zeros(18), index={'income', 'hours_worked','phys', 'phys_cat', 'pain', 'BMI',
                                        'BMI_cat', 'freq_frd', 'num_frd', 'num_org',
                                        'partner', 'trust', 'pronoun', 'pronoun_possessive', 'name', 'gender', 'liveWithPartnerBool', 'reportedTrust'})

    USMaleNames = ["James", "John", "Robert", "Michael", "William", "David",
                   "Richard", "Ethan", "Joseph", "Daniel", "Christopher", "Henry"]

    USFemaleNames = ["Karen", "Judy", "Linda", "Emma", "Elizabeth", "Jennifer",
                     "Christine", "Susan", "Isabella", "Dorothy", "Lisa", "Sophia"]


    # Map from df_domain to domain variables
    param["income"] = df_domain['Value'].ix['Household Income']
    
    if param["income"]<10000:
		param["income"] = "less than $10,000"
		
    
    param["hours_worked"] = df_domain['Value'].ix['Weekly Hours Worked']

    param["phys"] = df_domain['Value'].ix['Frequency of Exercise']
    param["phys_cat"] = df_domain['Category'].ix['Frequency of Exercise']
    
    param["pain"] = df_domain['Category'].ix['Pain']
    param["BMI"] = df_domain['Value'].ix['BMI']
    param["BMI_cat"] = df_domain['Category'].ix['BMI']

    param["freq_frd"] = df_domain['Category'].ix['Frequency of Friends']
    param["num_frd"] = df_domain['Value'].ix['Number of Friends']
    param["num_org"] = df_domain['Value'].ix['Number of Org']

    
    if(level == 0):
		partner_rand = random.randint(0, 1)
		trust_rand = random.randint(0, 1)
    else:
		if level == 1:
			partner_rand = 0
			trust_rand = 0
		elif level == 2:
			partner_rand = 0
			trust_rand = 0
		elif level == 3:
			partner_rand = 1
			trust_rand = 1
		elif level == 4:
			partner_rand = 1
			trust_rand = 1
		  
    param["liveWithPartnerBool"] = partner_rand
    param["reportedTrust"] = trust_rand
    
    
    gender_rand = random.randint(0, 1)
    
    if gender_rand == 1:
		param["gender"] = "Male"
    else:
		param["gender"] = "Female"
		
        
    param["partner"] = "lives alone"

    if trust_rand == 1:
        param["trust"] = "can be trusted"
    else:
        param["trust"] = "cannot be trusted"

    if gender_rand == 1:
        param["pronoun"] = "He"
        param["pronoun_smallcap"] = "he"
        param["pronoun_possessive"] = "his"
        param["pronoun_poss_cap"] = "His"
        param["name"] = USMaleNames[maleNameSel]
        if partner_rand == 1:
			param['partner'] = "lives with his partner"
			
		    
    else:
        param["pronoun"] = "She"
        param["pronoun_smallcap"] = "she"
        param["pronoun_possessive"] = "her"
        param["pronoun_poss_cap"] = "Her"
        param["name"] = USFemaleNames[femaleNameSel]
        if partner_rand == 1:
			param['partner'] = "lives with her partner"
   
    return param


# Helper function to input (format )parameters to Vignette text
def vig_gen_income(param):
	
	IncomeWork_Ser = Series(["The annual income of {pronoun_possessive} household is {income}.",
                         "{pronoun} is employed and works {hours_worked} {hours} per week."],
                        index=["income", "hours_worked"])
    
	income = param['income']
	income_str = "$"
	
	if type(income) is float:
		income = int(income)
		income = format(income, ',d')
		income_str += str(income)
	else:
		income_str = income
		
	
	hours_worked = int(round(param['hours_worked']))
	
	if(hours_worked == 1):
		hours = "hour"
	else:
		hours = "hours"
 
	IncomeWork_Ser['income'] = IncomeWork_Ser['income'].format(pronoun_possessive = param['pronoun_possessive'], income = income_str)
	IncomeWork_Ser['hours_worked'] = IncomeWork_Ser['hours_worked'].format(pronoun = param['pronoun'], hours_worked = hours_worked, hours = hours)
	
	#Within group shuffle
	IncomeWork_Ser = shuffle(IncomeWork_Ser)
	
	return IncomeWork_Ser


def vig_gen_health(param):
		                         
	Health_Ser = Series(["{pronoun} is {phys_cat} and walks {phys} {minutes} per day, which is {phys_recommand} the recommended level of exercise.",
                     "{pronoun} usually experiences {pain}.",
                     "{pronoun_poss_cap} body mass index (BMI) is {BMI}, which is categorized as "
                     "{BMI_cat}."],
                    index=["phys", "pain", "BMI"])
                    
	phys = int(param['phys'])

	if(phys == 1):
		minutes = "minute"
	else:
		minutes = "minutes"
		
	if(phys <30):
		phys_recommand = "below"
	else:
		phys_recommand = "above"
		
         
	Health_Ser['phys'] = Health_Ser['phys'].format(pronoun = param['pronoun'], pronoun_possessive = param['pronoun_possessive'], phys = phys, phys_cat = param['phys_cat'], minutes = minutes, phys_recommand = phys_recommand)
	Health_Ser['pain'] = Health_Ser['pain'].format(pronoun = param['pronoun'], pain = param['pain'])
	Health_Ser['BMI']  = Health_Ser['BMI'].format(pronoun_poss_cap = param['pronoun_poss_cap'], BMI = int(round(param['BMI'])), BMI_cat = param['BMI_cat'])
	
	#Within group shuffle
	Health_Ser = shuffle(Health_Ser)
	
	return Health_Ser
                   	                
 
def vig_gen_soc(param):                   
	
	Social_Ser = Series(["{pronoun} contacts {pronoun_possessive} friends {freq_frd}.",
                     "{pronoun} has {num_frd} {friends} that {pronoun_smallcap} considers to be close.",
                     "{pronoun} {partner}.",
                     "{pronoun} was involved in {num_org} community {org} in the past year.",
                     "{pronoun} believes that in general, most people in {pronoun_possessive} community {trust}."],
                    index=["freq_frd", "num_frd", "partner", "num_org", "trust"])
    
    
	num_frd = int(param['num_frd'])
    
	if(num_frd == 1):
		friends = "friend"
	else:
		friends = "friends"
    
	num_org = int(param['num_org'])
    
	if(num_org == 1):
		org = "organization/club"
	else:
		org = "organizations/clubs"
                    
	Social_Ser['freq_frd'] = Social_Ser['freq_frd'].format(pronoun = param['pronoun'], pronoun_possessive = param['pronoun_possessive'], freq_frd = param['freq_frd'])
	Social_Ser['num_frd'] = Social_Ser['num_frd'].format(pronoun = param['pronoun'], pronoun_smallcap = param['pronoun_smallcap'], num_frd = num_frd, friends = friends)
	Social_Ser['partner'] = Social_Ser['partner'].format(pronoun = param['pronoun'], partner = param['partner'])
	Social_Ser['num_org'] = Social_Ser['num_org'].format(pronoun = param['pronoun'], num_org = num_org, org = org)  
	Social_Ser['trust'] = Social_Ser['trust'].format(pronoun = param['pronoun'], pronoun_possessive = param['pronoun_possessive'], trust = param['trust']) 
	
	#Within group shuffle
	Social_Ser = shuffle(Social_Ser) 
	                	                
	return Social_Ser
	

# Helper function to format ser to string for vig text

def vig_text_string(domain_ser, domain_type):
	
	
	str_list = []
	
	if domain_type == "labour":
		for i in range (2):
			str_list.append(domain_ser[i])
				
	elif domain_type == "health":
		for i in range (3):
			str_list.append(domain_ser[i])
		
	elif domain_type == "social":
		for i in range (5):
			str_list.append(domain_ser[i])
		
	return ' '.join(str_list)
	
	
	
def vig_domain_order(domain_ser, domain_type):
	
	val_order = []
	id_order = []

	
	
	if domain_type == "labour":
		for i in range (2):
			if(domain_ser.index[i] == "income"):
				val_order.append("Income")
				id_order.append("IncomeBt")
			elif(domain_ser.index[i] == "hours_worked"):
				val_order.append("Weekly Hours Worked")
				id_order.append("WorkBt")		
			
				
	if domain_type == "health":
		for i in range (3):
			if(domain_ser.index[i] == "phys"):
				val_order.append("Frequency of Exercise")
				id_order.append("ExerciseBt")
			elif(domain_ser.index[i] == "pain"):
				val_order.append("Pain and Discomfort")
				id_order.append("PainBt")
			elif(domain_ser.index[i] == "BMI"):
				val_order.append("Body Mass Index (BMI)")
				id_order.append("BMIBt")
						
			
	if domain_type == "social":
		for i in range (5):
			if(domain_ser.index[i] == "freq_frd"):
				val_order.append("Frequency of Seeing Friends")
				id_order.append("FreqFrdBt")
			elif(domain_ser.index[i] == "num_frd"):
				val_order.append("Number of Close Friends")
				id_order.append("NumFrdBt")
			elif(domain_ser.index[i] == "partner"):
				val_order.append("Live alone/with a partner")
				id_order.append("PartnerBt")
			elif(domain_ser.index[i] == "num_org"):
				val_order.append("Community Involvement")
				id_order.append("CommunityBt")
			elif(domain_ser.index[i] == "trust"):
				val_order.append("Trust")
				id_order.append("TrustBt")
						
		

	return val_order, id_order
	
	
	
	
# Helper function to concatenate the complete Vignette Text

def vig_concatenate(name, vigTextLabour, vigTextHealth, vigTextSoc, permSel):
	
	
	
	str_list = []
	
	name_str = "{} is 30 years old.".format(name)
	str_list.append(name_str)
	
	
	for j in range (3):
		
		if permSel[j] == 1:
			str_list.append(vigTextLabour)
				
		elif permSel[j] == 2:
			str_list.append(vigTextHealth)
		
		elif permSel[j] == 3:
			str_list.append(vigTextSoc)
		
	return ' '.join(str_list)
		


		


	 
	
	
	



