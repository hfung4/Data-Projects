
<body id="main_body_V5" >

<img id="top" src="images/top.png" alt="">

 
 
 
<div style ="position:absolute; top:20; right:20px;" 
<div class="c100 p75">
	<span>75%</span>
	<div class="slice">
		<div class="bar"></div>
		<div class="fill"></div>
	</div>
<p style="font-size:15%; color:#428bca; position: relative; top: 105px; "> Your progress </p>
</div>

</div>




<div id="form_container">

<h1><a>Vignette 5</a></h1>

<form class="form_temp"  action="surveyIUEHQ34VX.php" method="POST">


<div class="form_description">


<h2><strong>Vignette 5</strong></h2>



<br>
<p>
<strong><?php echo $vig_prompts["note5"]; ?></strong>
</p>

<br>


</div>


<ul >


<br>


<div class="vig_description">
<label class="description" for="vigDesc" style ="color:black;">Please evaluate the Life Satisfaction of this person  </label>
<br>
<p>

<b><?php echo $Name5; ?></b> is 30 years old.

<?php
foreach($vig5Order as $k)
{
	if($k == 1) { ?>
		<span style = "color: brown;"> <?php echo $Vignette5TextLabour; ?></span>
	
	<?php } else if($k == 2) { ?>
		<span style = "color: #006400;"> <?php echo $Vignette5TextHealth; ?> </span>
	
	<?php }else if($k == 3) { ?>
		<span style = "color: #00008B;"><?php echo $Vignette5TextSoc; ?> </span>
	<?php }
}
?>



</p>
</div>		

<br>
<br>

<label class="description" for="RelSel" style ="color:black;">If you like, you can click on the buttons to learn more about <?php echo $Name5; ?>'s community </label>
<br>
 
 
 
 
<?php
foreach($vig5Order as $k)
{
	if($k == 1) { ?>
		
		<div class="w3-bar">
        		
		<input type="button"  name="rel<?php echo $vig5LabourID1; ?>5" value="<?php echo $vig5LabourName1; ?>" class = "w3-bar-item w3-button w3-brown" style="width:33.3%" id = "<?php echo $vig5LabourID1; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		
		<input type="button"  name="rel<?php echo $vig5LabourID2; ?>5" value="<?php echo $vig5LabourName2; ?>" class = "w3-bar-item w3-button w3-brown" style="width:33.3%" id = "<?php echo $vig5LabourID2; ?>"
        onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
        
       	<input type="button"  name="relUnemployBt5" value="Unemployment Rate" class = "w3-bar-item w3-button w3-brown" style="width:33.3%" id = "UnemployBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartUnemploy(<?php echo $unemploy_Val5; ?>, '<?php echo $Name5; ?>');">     
        
        </div>
        <br>
        
        
    <?php } else if($k == 2) { ?>
		
		<div class="w3-bar">
		<input type="button"  name="rel<?php echo $vig5HealthID1; ?>5" value="<?php echo $vig5HealthName1; ?>" class = "w3-bar-item w3-button w3-teal" style="width:33.3%" id = "<?php echo $vig5HealthID1; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		
		<input type="button"  name="rel<?php echo $vig5HealthID2; ?>5" value="<?php echo $vig5HealthName2; ?>" class = "w3-bar-item w3-button w3-teal" style="width:33.3%" id = "<?php echo $vig5HealthID2; ?>"
        onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
        
        <input type="button"  name="rel<?php echo $vig5HealthID3; ?>5" value="<?php echo $vig5HealthName3; ?>" class = "w3-bar-item w3-button w3-teal" style="width:33.3%" id = "<?php echo $vig5HealthID3; ?>"
        onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
        
        </div>
        <br>
        
    <?php }else if($k == 3) { ?>
		
		<div class="w3-bar">
		
		<?php if(strcmp($vig5SocialName1, "Live alone/with a partner")==0) { ?>
		<input type="button"  name="relPartnerBt5" value="Live alone/with a partner" class = "w3-bar-item w3-button w3-indigo"  style="width:33.3%" id="PartnerBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartPartner(<?php echo $partner_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5PartnerBool; ?> );">   
		
		<?php }else if(strcmp($vig5SocialName1,"Trust")==0) { ?>
		<input type="button"  name="relTrustBt5" value="Trust" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id = "TrustBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartTrust(<?php echo $trust_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5TrustBool; ?> );">
		
		<?php }else { ?>	
		<input type="button"  name="rel<?php echo $vig5SocialID1; ?>5" value="<?php echo $vig5SocialName1; ?>" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id = "<?php echo $vig5SocialID1; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		<?php } ?>  
		
		
		
		
		<?php if(strcmp($vig5SocialName2, "Live alone/with a partner")==0) { ?>
		<input type="button"  name="relPartnerBt5" value="Live alone/with a partner" class = "w3-bar-item w3-button w3-indigo"  style="width:33.3%" id="PartnerBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartPartner(<?php echo $partner_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5PartnerBool; ?> );">   
		
		<?php }else if(strcmp($vig5SocialName2,"Trust")==0) { ?>
		<input type="button"  name="relTrustBt5" value="Trust" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id = "TrustBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartTrust(<?php echo $trust_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5TrustBool; ?> );">
		
		<?php }else { ?>
		<input type="button"  name="rel<?php echo $vig5SocialID2; ?>5" value="<?php echo $vig5SocialName2; ?>" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id="<?php echo $vig5SocialID2; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);"> 
		<?php } ?>  
		
		
		
		
		<?php if(strcmp($vig5SocialName3, "Live alone/with a partner")==0) { ?>
		<input type="button"  name="relPartnerBt5" value="Live alone/with a partner" class = "w3-bar-item w3-button w3-indigo"  style="width:33.3%" id="PartnerBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartPartner(<?php echo $partner_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5PartnerBool; ?> );">   
		
		<?php }else if(strcmp($vig5SocialName3,"Trust")==0) { ?>
		<input type="button"  name="relTrustBt5" value="Trust" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id = "TrustBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartTrust(<?php echo $trust_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5TrustBool; ?> );">
		
		<?php }else { ?>
		<input type="button"  name="rel<?php echo $vig5SocialID3; ?>5" value="<?php echo $vig5SocialName3; ?>" class = "w3-bar-item w3-button w3-indigo" style="width:33.3%" id= "<?php echo $vig5SocialID3; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		<?php } ?>
		
		</div>
		<br>
		
		
		
		<div class="w3-bar">
		
		<?php if(strcmp($vig5SocialName4,"Live alone/with a partner")==0) { ?>
		<input type="button"  name="relPartnerBt5" value="Live alone/with a partner" class = "w3-bar-item w3-button w3-indigo"  style="width:50%" id="PartnerBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartPartner(<?php echo $partner_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5PartnerBool; ?> );">   
		
		<?php }else if(strcmp($vig5SocialName4,"Trust")==0) { ?>
		<input type="button"  name="relTrustBt5" value="Trust" class = "w3-bar-item w3-button w3-indigo" style="width:50%" id = "TrustBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartTrust(<?php echo $trust_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5TrustBool; ?> );">
		
		<?php }else { ?>
		<input type="button"  name="rel<?php echo $vig5SocialID4; ?>5" value="<?php echo $vig5SocialName4; ?>" class = "w3-bar-item w3-button w3-indigo" style="width:50%" id= "<?php echo $vig5SocialID4; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		<?php } ?>
		
		
		
		
		<?php if(strcmp($vig5SocialName5,"Live alone/with a partner")==0) { ?>
		<input type="button"  name="relPartnerBt5" value="Live alone/with a partner" class = "w3-bar-item w3-button w3-indigo"  style="width:50%" id="PartnerBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartPartner(<?php echo $partner_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5PartnerBool; ?> );">   
		
		<?php }else if(strcmp($vig5SocialName5,"Trust")==0) { ?>
		<input type="button"  name="relTrustBt5" value="Trust" class = "w3-bar-item w3-button w3-indigo" style="width:50%" id = "TrustBt" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this); getChartTrust(<?php echo $trust_Val5; ?>, '<?php echo $Name5; ?>', <?php echo $vig5TrustBool; ?> );">
		
		<?php }else { ?>
		<input type="button"  name="rel<?php echo $vig5SocialID5; ?>5" value="<?php echo $vig5SocialName5; ?>" class = "w3-bar-item w3-button w3-indigo" style="width:50%" id= "<?php echo $vig5SocialID5; ?>" onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>); btDisable(this);">
		<?php } ?>
		
		</div>
		<br>
		
		<?php }
}
?>



  
  
 
  
   <div id="DisplayRelBars"></div>
  
 <div id="IncomeBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-red">
	
	
  <div style ="margin-left: 50px"> 
	  
  <br>
     
     <p style="margin-left:0%;  font-weight:bold; color:brown; font-size:14px"><?php echo $Name5; ?>'s household income is $<?php echo $income_Val5; ?>
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $income_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?>'s </span> <span style ="font-weight:bold; font-size: 12px; color:brown;">income</span> 

<?php if($income_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than </span> <span style ="font-weight:bold; font-size: 12px; color:#CC0000;"><?php echo $income_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>
  
  
  
   <div id="WorkBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-red">
  <div style ="margin-left: 50px">
	 <br>    
     
     <p style="margin-left:0%;  font-weight:bold; color:brown; font-size:14px"><?php echo $Name5; ?> works <?php echo $hoursWorked_Val5; ?> hours per week </p>
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $hoursWorked_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?>'s </span> <span style ="font-weight:bold; font-size: 12px; color:brown;">Weekly Hours Worked</span> 

<?php if($hoursWorked_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than </span> <span style ="font-weight:bold; font-size: 12px; color:#CC0000;"><?php echo $hoursWorked_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>




  
  <div id="UnemployBar" style ="display:none;"  class="w3-panel w3-border w3-hover-border-red">
	  <div style ="margin-left: 50px"> 
	<br>      
     <p style="margin-left: 0%;font-weight:bold; color:brown; font-size:14px">The Unemployment rate in <?php echo $Name5; ?>'s community is <?php echo $unemploy_Val5; ?>% </p>
     </div>

  <div id="piechartUnemploy"></div>
 
  </div>


  
 <div id="NumFrdBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-blue">
  <div style ="margin-left: 50px">
	  <br> 
     
     <?php if($numFrds_Val5 == 0) { ?>
     <p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> has no friend that <?php echo $GenderNoun5; ?>   considers close </p>
     <?php } else if ($numFrds_Val5 == 1){ ?> 
	 <p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> has <?php echo $numFrds_Val5; ?> friend that <?php echo $GenderNoun5; ?> considers close  </p>
	 <?php } else { ?> 
	 <p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> has <?php echo $numFrds_Val5; ?> friends that <?php echo $GenderNoun5; ?> considers close  </p>
	 <?php }  ?>
     
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $numFrds_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?> <span style ="font-weight:bold; font-size: 12px; color:#00008B;">has more close friends </span> 
<?php if($numFrds_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">than </span> <span style ="font-weight:bold; font-size: 12px; color:blue;"><?php echo $numFrds_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>

 
  
  
 <div id="FreqFrdBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-blue">
  <div style ="margin-left: 50px">  
	  
    <br> 
     <?php if($freqFrds_Val5 == 0) { ?>
	 <p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> did not contact <?php echo $GenderPronoun5; ?> friends in the past month</p>
     <?php } else { ?>		 
     <p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> contacts <?php echo $GenderPronoun5; ?> friends <?php echo $freqFrds_Cat5; ?> </p>
     <?php } ?>
		 
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $freqFrds_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?></span> <span style ="font-weight:bold; font-size: 12px; color:#00008B;">contacts <?php echo $GenderPronoun5; ?> friends </span> 
<span style ="font-weight:bold; font-size: 12px">more frequently than</span> 

<?php if($freqFrds_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px"> almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px"></span> <span style ="font-weight:bold; font-size: 12px; color:blue;"><?php echo $freqFrds_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>

  
  
  
 <div id="TrustBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-blue">
  <div style ="margin-left: 50px">  
	  
 <br> 
     
     <p style="margin-left:-12%;  font-weight:bold; color:#00008B; font-size:14px" align="center" >The Reported Trust in <?php echo $Name5; ?>'s  Community is <?php echo $trust_Val5; ?>% </p>
</div>
<div id="piechartTrust"></div>
          
</div>

  

   <div id="CommunityBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-blue">
  <div style ="margin-left: 50px">  
	  
 <br> 
     
     <?php if($numOrg_Val5 == 0) { ?>
	<p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> was not involved in any community organizations</p>
	<?php } else if ($numOrg_Val5 == 1){ ?>
	<p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> was involved in <?php echo $numOrg_Val5; ?>   community organization</p>
	<?php } else { ?>
	<p style="margin-left:0%;  font-weight:bold; color:#00008B; font-size:14px"><?php echo $Name5; ?> was involved in <?php echo $numOrg_Val5; ?>   community organizations</p>
	<?php } ?>
		
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $numOrg_Per5; ?>%;" ></div> 
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?> was involved in a greater  </span> <span style ="font-weight:bold; font-size: 12px; color:#00008B;">number of community organizations in the past 12 months than</span> 
<?php if($numOrg_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px"> almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px"></span> <span style ="font-weight:bold; font-size: 12px; color:blue;"><?php echo $numOrg_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>
  

  
<div id="PartnerBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-blue">
	<div style ="margin-left: 50px">  
	  
 <br> 
     
     <?php if($vig5PartnerBool == 0) { ?>     
     <p style="margin-left: -8%;  font-weight:bold; color:#00008B; font-size:14px" align="center">The percentage of people who live alone in <?php echo $Name5; ?>'s community is <?php echo $alone5; ?>% </p>
     <?php }else{ ?>
     
     <p style="margin-left: -8%;  font-weight:bold; color:#00008B; font-size:16px;" align="center">The percentage of people who live with a partner in <?php echo $Name5; ?>'s community is <?php echo $partner_Val5; ?>% </p>
     
     <?php } ?>
     </div>

	
<div id="piechartPartner"></div>

</div>
  
  
  
  
      <div id="ExerciseBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-green">
  <div style ="margin-left: 50px">  
	  
 <br> 
     
     <p style="margin-left:0%;  font-weight:bold; color:#006400; font-size:14px"><?php echo $Name5; ?> is <?php echo $phys_Cat5; ?> and walks <?php echo $phys_Val5; ?> minutes per day  </p>
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $phys_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?> engages in more </span> <span style ="font-weight:bold; font-size: 12px; color:#006400;">physical activities per day</span> 

<?php if($phys_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">than </span> <span style ="font-weight:bold; font-size: 12px; color:#00b300;"><?php echo $phys_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>



      <div id="PainBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-green">
  <div style ="margin-left: 50px">  
	  
 <br>  
     
     <p style="margin-left:0%;  font-weight:bold; color:#006400; font-size:14px"><?php echo $Name5; ?> usually experiences <?php echo $pain_Cat5; ?> </p>
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $pain_Per5; ?>%;" ></div>
     </div>
<br>


<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?> suffers from </span> <span style ="font-weight:bold; font-size: 12px; color:#006400;">less pain and discomfort</span> 

<?php if($pain_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">than </span> <span style ="font-weight:bold; font-size: 12px; color:#00b300;"><?php echo $pain_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>






      <div id="BMIBar" style ="display:none;" class="w3-panel w3-border w3-hover-border-green">
  <div style ="margin-left: 50px">  
	  
 <br>  
     
     <p style="margin-left:0%;  font-weight:bold; color:#006400; font-size:14px"><?php echo $Name5; ?>'s BMI is <?php echo $BMI_Val5; ?>, which is categorized as <?php echo $BMI_Cat5; ?> </p>
     <div class="w3-border" style="width: 80%; height: 10px;">  
     <div id="myBar" style="height: 8px; width: <?php echo $BMI_Per5; ?>%;" ></div>
     </div>
<br>
<span style ="text-align: center; font-weight:bold; font-size: 12px" > <?php echo $Name5; ?>'s </span> <span style ="font-weight:bold; font-size: 12px; color:#006400;">Body Mass Index (BMI) </span> 

<?php if($BMI_Per5 == 100) { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than almost everyone in <?php echo $GenderPronoun5; ?> community</span>
<?php } else { ?>
	<span style ="font-weight:bold; font-size: 12px">is greater than </span> <span style ="font-weight:bold; font-size: 12px; color:#00b300;"><?php echo $BMI_Per5; ?>% </span>of the people in <?php echo $GenderPronoun5; ?> community</span>
<?php } ?>
</div> 
<br>         
</div>





<br>
<br>
<br>
<br>
<br>




<span style="font-size:150%; text-align:left; font-weight:bold; color:#29a3a3;"> This person's Life Satisfaction is: </span>

<span id="Vig5displayAmount" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:150%"></span>
<br><br>
<div id="Vig5slider"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="Vig5amount" name= "vignetteans">
<input type="hidden" id="Vig5Triggered" name= "vignettetrigger">


<br><br><br><br><br><br>
<div class="buttons" style = "float:right">
<input type='submit' name='Vignette5Submit' id= 'Vig5Submit' value='Next >>' onClick = "confirmBox('Vig5Triggered');">
</div>

<!-- Hidden inputs": variables that I want to send from page 6 to the subsequent page -->	
<input type="hidden" name="page" value="7">
<input type="hidden" name="lang" value="<?php echo $_POST['lang']; ?>">
<input type="hidden" name="randurl" value="<?php echo $_POST['randurl']; ?>" >
<input type="hidden" name="ID" value="<?php echo $_POST['ID']; ?>" >
<input type="hidden" name="vignette5_startTime" value="<?php echo $vignette5_startTime; ?>" >



</ul>


<br><br><br><br>

<input type="button"  name="PreviousVigBt5" value="Review Previous Responses" id="previousVigBt"
style = " background-color: #669999; color: white;   padding: 16px; border: none;  cursor: pointer;"
onClick ="get(this.name, <?php echo $_POST['ID']; ?>, <?php echo $_POST['page']; ?>);">


<div id="previousVigDisplay" style ="display:none; background-color: #E6E6DC;">

<?php if($vignette1Answer==-1) { ?>	
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 1: No Response Yet</h3>
<?php } else { ?>
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 1 Response: <?php echo $vignette1Answer; ?></h3>
<p style = "color: #00628B;"><?php echo $Vignette1Displayed; ?></p>
<?php } ?>


<br>

<?php if($vignette2Answer==-1) { ?>	
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 2: No Response Yet</h3>
<?php } else { ?>
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 2 Response: <?php echo $vignette2Answer; ?></h3>
<p style = "color: #00628B;"><?php echo $Vignette2Displayed; ?></p>
<?php } ?>


<br>

<?php if($vignette3Answer==-1) { ?>	
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 3: No Response Yet</h3>
<?php } else { ?>
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 3 Response: <?php echo $vignette3Answer; ?></h3>
<p style = "color: #00628B;"><?php echo $Vignette3Displayed; ?></p>
<?php } ?>

<br>

<?php if($vignette4Answer==-1) { ?>	
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 4: No Response Yet</h3>
<?php } else { ?>
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 4 Response: <?php echo $vignette4Answer; ?></h3>
<p style = "color: #00628B;"><?php echo $Vignette4Displayed; ?></p>
<?php } ?>


<br>
<?php if($vignette5Answer==-1) { ?>	
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 5: No Response Yet</h3>
<?php } else { ?>
<h4 style ="font-weight:bold; color: #81A594; font-size:14px">Vignette 5 Response: <?php echo $vignette5Answer; ?></h3>
<p style = "color: #00628B;"><?php echo $Vignette5Displayed; ?></p>
<?php } ?>



</div>




</form>		

</div>


<img id="bottom" src="images/bottom.png" alt="">


</body>


</html>






