

<body id="body_demographics" >

<img id="top" src="images/top.png" alt="">



<div style ="position:absolute; top:20; right:20px;" 
<div class="c100 p100">
	<span>100%</span>
	<div class="slice">
		<div class="bar"></div>
		<div class="fill"></div>
	</div>
<p style="font-size:15%; color:#428bca; position: relative; top: 105px; "> Your progress </p>
</div>

</div>




<div id="form_container">

<h1><a>A few last questions about you</a></h1>

<form class="form_temp"  action="surveyIUEHQ34VX.php" method="POST">
	
<!-- Hidden inputs": variables that I want to send from page 8 to the subsequent page -->	
<input type="hidden" name="page" value="9">
<input type="hidden" name="lang" value="<?php echo $_POST['lang']; ?>">
<input type="hidden" name="randurl" value="<?php echo $_POST['randurl']; ?>" >
<input type="hidden" name="ID" value="<?php echo $_POST['ID']; ?>" >
<input type="hidden" name="demographics_startTime" value="<?php echo $demographics_startTime; ?>" >
	


<div class="form_description">


<h2><strong>A Few Last Questions About You</strong></h2>


<br>
<p>
<strong>Please answer carefully the following questions.</strong>
</p>					

</div>						
<ul >
	
	
<br>
<li id="li_1" >
<label class="description" for="Age1">1. What is your age? </label>
<div>
<input id="element_1" name="Age1" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 
</li>		



<li id="li_2" >
<label class="description" for="Gender">2. What is your gender </label>
<div>
<input id="element_2" name="Gender" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 
</li>

<br>

<li id="li_3" >
<label class="description" for="Education">3. What is the highest level of education you have completed? </label>
<span>
<input id="element_10_1" name="Education" class="element radio" type="radio" value="1" />
<label class="choice" for="Education">Attended high school but did not graduate</label>
<input id="element_10_2" name="Education" class="element radio" type="radio" value="2" />
<label class="choice" for="Education">High school graduate</label>
<input id="element_10_3" name="Education" class="element radio" type="radio" value="3" />
<label class="choice" for="Education">Attended college/university but did not graduate</label>
<input id="element_10_4" name="Education" class="element radio" type="radio" value="4" />
<label class="choice" for="Education">Bachelor's Degree</label>
<input id="element_10_5" name="Education" class="element radio" type="radio" value="5" />
<label class="choice" for="Education">Master's Degree</label>
<input id="element_10_6" name="Education" class="element radio" type="radio" value="6" />
<label class="choice" for="Education">Doctoral Degree</label>
<input id="element_10_7" name="Education" class="element radio" type="radio" value="7" />
<label class="choice" for="Education">Professional Degree</label>
</span> 
</li>


<br>
		
<li id="li_4" >
<label class="description" for="maranswer">4. What is your marital status? </label>
<span>
<input id="element_11_1" name="maranswer" class="element radio" type="radio" value="single" />
<label class="choice" for="maranswer">Single</label>
<input id="element_11_2" name="maranswer" class="element radio" type="radio" value="married" />
<label class="choice" for="maranswer">Married or Cohabitating</label>
<input id="element_11_3" name="maranswer" class="element radio" type="radio" value="divorced" />
<label class="choice" for="maranswer">Divorced</label>
<input id="element_11_4" name="maranswer" class="element radio" type="radio" value="widowed" />
<label class="choice" for="maranswer">Widowed</label>
</span> 
</li>		

<br>

<li id="li_5" >
<label class="description" for="employanswer">5. Are you currently employed? </label>
<span>
<input id="element_12_1" name="employanswer" class="element radio" type="radio" value="1" />
<label class="choice" for="employanswer">Yes</label>
<input id="element_12_2" name="employanswer" class="element radio" type="radio" value="2" />
<label class="choice" for="employanswer">No, and looking for a job</label>
<input id="element_12_3" name="employanswer" class="element radio" type="radio" value="3" />
<label class="choice" for="employanswer">No, and NOT looking for a job</label>
</span> 
</li>		

<br>


<li id="li_6" >
<label class="description" for="indincomeanswer">6. What is your personal annual income (before tax)? </label>
<label class="description" for="element_13"> Enter value or choose from the options: </label>
<span>
<span> </span>	
<input type="radio" id="indIncomeTextSel" name="indincomeanswer" value="-1" />

<input type="text" id="indincometextbox" value="Your Income" name ="indincomeanswertext"
    onclick="if(this.value=='Your Income'){this.value=''; this.style.color='#000'}" 
    onblur="if(this.value==''){this.value='Your Income'; this.style.color='#555'}" />


<input id="element_13_1" name="indincomeanswer" class="element radio" type="radio" value="10000" />
<label class="choice" for="indincomeanswer">Less than $10 000</label>
<input id="element_13_2" name="indincomeanswer" class="element radio" type="radio" value="20000" />
<label class="choice" for="indincomeanswer">$10 000 - $19 999</label>
<input id="element_13_3" name="indincomeanswer" class="element radio" type="radio" value="30000" />
<label class="choice" for="indincomeanswer">$20 000 - $29 999</label>
<input id="element_13_4" name="indincomeanswer" class="element radio" type="radio" value="40000" />
<label class="choice" for="indincomeanswer">$30 000 - $39 999</label>
<input id="element_13_5" name="indincomeanswer" class="element radio" type="radio" value="50000" />
<label class="choice" for="indincomeanswer">$40 000 - $49 999</label>
<input id="element_13_6" name="indincomeanswer" class="element radio" type="radio" value="60000" />
<label class="choice" for="indincomeanswer">$50 000 - $59 999</label>
<input id="element_13_7" name="indincomeanswer" class="element radio" type="radio" value="70000" />
<label class="choice" for="indincomeanswer">$60 000 - $69 999</label>
<input id="element_13_8" name="indincomeanswer" class="element radio" type="radio" value="90000" />
<label class="choice" for="indincomeanswer">$70 000 - $89 999</label>
<input id="element_13_9" name="indincomeanswer" class="element radio" type="radio" value="120000" />
<label class="choice" for="indincomeanswer">$90 000 - $119 999</label>
<input id="element_13_10" name="indincomeanswer" class="element radio" type="radio" value="150000" />
<label class="choice" for="indincomeanswer">$120 000 - $149 999</label>
<input id="element_13_11" name="indincomeanswer" class="element radio" type="radio" value="200000" />
<label class="choice" for="indincomeanswer">More than $150 000</label>
</span> 
</li>		


<br>


<li id="li_7" >
<label class="description" for="element_14">7. What is your annual household income (before tax)? </label>
<label class="description" for="element_14"> Enter value or choose from the options: </label>
<span>
<span></span>	

<input type="radio" id="overIncomeTextSel" name="householdIncomeanswer" value="0" />

<input type="text" id="overincometextbox" value="Your Income" name ="householdIncomeanswertext"
    onclick="if(this.value=='Your Income'){this.value=''; this.style.color='#000'}" 
    onblur="if(this.value==''){this.value='Your Income'; this.style.color='#555'}" />
	
	
<input id="element_14_1" name="householdIncomeanswer" class="element radio" type="radio" value="10000" />
<label class="choice" for="element_14_1">Less than $10 000</label>
<input id="element_14_2" name="householdIncomeanswer" class="element radio" type="radio" value="20000" />
<label class="choice" for="element_14_2">$10 000 - $19 999</label>
<input id="element_14_3" name="householdIncomeanswer" class="element radio" type="radio" value="30000" />
<label class="choice" for="element_14_3">$20 000 - $29 999</label>
<input id="element_14_4" name="householdIncomeanswer" class="element radio" type="radio" value="40000" />
<label class="choice" for="element_14_4">$30 000 - $39 999</label>
<input id="element_14_5" name="householdIncomeanswer" class="element radio" type="radio" value="50000" />
<label class="choice" for="element_14_5">$40 000 - $49 999</label>
<input id="element_14_6" name="householdIncomeanswer" class="element radio" type="radio" value="60000" />
<label class="choice" for="element_14_6">$50 000 - $59 999</label>
<input id="element_14_7" name="householdIncomeanswer" class="element radio" type="radio" value="70000" />
<label class="choice" for="element_14_7">$60 000 - $69 999</label>
<input id="element_14_8" name="householdIncomeanswer" class="element radio" type="radio" value="90000" />
<label class="choice" for="element_14_8">$70 000 - $89 999</label>
<input id="element_14_9" name="householdIncomeanswer" class="element radio" type="radio" value="120000" />
<label class="choice" for="element_14_9">$90 000 - $119 999</label>
<input id="element_14_10" name="householdIncomeanswer" class="element radio" type="radio" value="150000" />
<label class="choice" for="element_14_10">$120 000 - $149 999</label>
<input id="element_14_11" name="householdIncomeanswer" class="element radio" type="radio" value="200000" />
<label class="choice" for="element_14_11">More than $150 000</label>
</span> 
</li>		


<br>
		

<li id="li_8" >
<label class="description" for="element_15">8. How many people contribute to the total annual household income? </label>
<span>
<input id="element_15_1" name="contrincomeanswer" class="element radio" type="radio" value="1" />
<label class="choice" for="element_15_1">1</label>
<input id="element_15_2" name="contrincomeanswer" class="element radio" type="radio" value="2" />
<label class="choice" for="element_15_2">2</label>
<input id="element_15_3" name="contrincomeanswer" class="element radio" type="radio" value="3" />
<label class="choice" for="element_15_3">3</label>
<input id="element_15_4" name="contrincomeanswer" class="element radio" type="radio" value="4" />
<label class="choice" for="element_15_4">More than 3</label>
</span> 
</li>		

<br>

<li id="li_9" >
<label class="description" for="element_16">9. How many people are there in your household?  </label>
<span>
<input id="element_16_1" name="NumFamHousehold" class="element radio" type="radio" value="1" />
<label class="choice" for="element_16_1">1</label>
<input id="element_16_2" name="NumFamHousehold" class="element radio" type="radio" value="2" />
<label class="choice" for="element_16_2">2</label>
<input id="element_16_3" name="NumFamHousehold" class="element radio" type="radio" value="3" />
<label class="choice" for="element_16_3">3</label>
<input id="element_16_4" name="NumFamHousehold" class="element radio" type="radio" value="4" />
<label class="choice" for="element_16_4">4</label>
<input id="element_16_5" name="NumFamHousehold" class="element radio" type="radio" value="5" />
<label class="choice" for="element_16_5">5</label>
<input id="element_16_6" name="NumFamHousehold" class="element radio" type="radio" value="6" />
<label class="choice" for="element_16_6">6</label>
<input id="element_16_7" name="NumFamHousehold" class="element radio" type="radio" value="7" />
<label class="choice" for="element_16_7">7</label>
<input id="element_16_8" name="NumFamHousehold" class="element radio" type="radio" value="8" />
<label class="choice" for="element_16_8">More than 7</label>
</span> 
</li>		


<br>

<li id="li_10" >
<label class="description" for="element_17">10. What is your age (again)? </label>
<span>
<input id="element_17_1" name="ageanswer2" class="element radio" type="radio" value="1" />
<label class="choice" for="element_17_1">Younger than 20</label>
<input id="element_17_2" name="ageanswer2" class="element radio" type="radio" value="2" />
<label class="choice" for="element_17_2">20-30</label>
<input id="element_17_3" name="ageanswer2" class="element radio" type="radio" value="3" />
<label class="choice" for="element_17_3">31-40</label>
<input id="element_17_4" name="ageanswer2" class="element radio" type="radio" value="4" />
<label class="choice" for="element_17_4">41-50</label>
<input id="element_17_5" name="ageanswer2" class="element radio" type="radio" value="5" />
<label class="choice" for="element_17_5">51-60</label>
<input id="element_17_6" name="ageanswer2" class="element radio" type="radio" value="6" />
<label class="choice" for="element_17_6">61-70</label>
<input id="element_17_7" name="ageanswer2" class="element radio" type="radio" value="7" />
<label class="choice" for="element_17_7">Older than 70</label>
</span> 
</li>		

<br>
		
<li id="li_11" >
<label class="description" for="element_3">11. List up to 5 countries that you have lived in: </label>
<br>
		
<div>
<label class="description" for="Country1">Country 1 </label>
<input id="element_3" name="Country1" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 

<label class="description" for="Country2">Country 2 </label>
<div>
<input id="element_4" name="Country2" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 

<label class="description" for="Country3">Country 3 </label>
<div>
<input id="element_5" name="Country3" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 
	

<label class="description" for="Country4">Country 4 </label>
<div>
<input id="element_6" name="Country4" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 

<label class="description" for="Country5">Country 5 </label>
<div>
<input id="element_7" name="Country5" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 
</li>	

<br>
<br>
						
<li id="li_12" >		
<label class="description" for="state">12. Which state in the country that you live in? </label>
<div>
<select class="element select medium" id="element_18" name="state"> 
<option> Enter State </option>
<option> I do not live in the USA</option>
<option>Alabama</option>
<option>Alaska</option>
<option>Arizona</option>
<option>Arkansas</option>
<option>California</option>
<option>Colorado</option>
<option>Connecticut</option>
<option>Colorado</option>
<option>Delaware</option>
<option>District of Columbia</option>
<option>Florida</option>
<option>Georgia</option>
<option>Hawaii</option>
<option>Idaho</option>
<option>Illinois</option>
<option>Indiana</option>
<option>Iowa</option>
<option>Kansas</option>
<option>Kentucky</option>
<option>Louisiana</option>
<option>Maine</option>
<option>Maryland</option>
<option>Massachusetts</option>
<option>Michigan</option>
<option>Minnesota</option>
<option>Mississippi</option>
<option>Missouri</option>
<option>Montana</option>
<option>Nebraska</option>
<option>Nevada</option>
<option>New Hampshire</option>
<option>New Jersey</option>
<option>New Mexico</option>
<option>New York</option>
<option>North Carolina</option>
<option>North Dakota</option>
<option>Ohio</option>
<option>Oklahoma</option>
<option>Oregon</option>
<option>Pennsylvania</option>
<option>Rhode Island</option>
<option>South Carolina</option>
<option>South Dakota</option>
<option>Tennessee</option>
<option>Texas</option>
<option>Utah</option>
<option>Vermont</option>
<option>Virginia</option>
<option>Washington</option>
<option>West Virginia</option>
<option>Wisconsisn</option>
<option>Wyoming</option>
</select>
</div> 
</li>

<br>
<br>
				

<label class="description" for="codeAnsAge">13. Completion code: To generate your completion code, please enter your age in years.  Your code will be displayed in the next page.</label>
<div>
<input id="element_8" name="codeAnsAge" class="element text medium" type="text" maxlength="255" value=""/> 
</div> 

<br>
		
<br>
		
<label class="description" for="Comments">14. Please enter any comments that you may have about the survey. Thank you! </label>
<div>
<textarea id="element_9" name="Comments" class="element textarea medium"></textarea> 
</div> 


<center>
<li class="buttons">
<center><input type='submit' name='DemographicSubmit' id= 'DemoSubmit' value='Submit'>
</li>
</center>


</ul>
		
</form>	
		
</div>
	
	
<img id="bottom" src="images/bottom.png" alt="">





</body>


</html>
