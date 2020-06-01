<?php

/**
* INPUTS:
* Welcome page for the Life Conditions Survey
* This page is a form the following input arguments:
* 
* en: A radio input for English language for the survey.
* fr: A radio input for French language for the survey.
* submit: state of submit button for the form.
*
* The following inputs are "hidden".  They can be accessed through subsequent pages via _POST super global
* randurl: A hidden random value (between 1000, 10000) that is generated at the stary of the survey. 
* random:  A hidden random value (between 1 and 1000000) that is generated at the start of the survey.
* ipaddress1:  A hidden ip addresss recorded at the start of the survey.
* timewelcome: A hidden time and date value recorded at the start of the survey.
* page:  Page number of the survey
* 
* OUTPUTS:
* The user input is stored in a super global assoicated array $_POST.
* $_POST is then processed in "surveyIUEHQ34VX.php"
*/

//ip address and time that is recorded at the start of the survey
$ipaddress1 = $_SERVER['REMOTE_ADDR'];
$timewelcome = date('m/d/Y h:i:s a', time());

//generate random variables
$randurl=rand(1000,100000); // used for URL
$random=rand(1,1000000); //used for user ID




/* NOTE:  Always use this snippet if I want to use php variables in html 
 * 
 * <?php echo $myVar; ?>
 */

?>



<html>
<body id="main_body">


<div id="form_container" style="width:800px; position:relative;">
	
<div style ="position:absolute; top:70px; right:18px;"> 
<img src="images/mcgilllogo.png" alt="McGill University"width="145" height="45"/>
</div>

<div style ="position:absolute; top:55px; left:20px;">
<img src="images/ihsplogo.jpg" alt="IHSP"width="120" height="70"/>
</div>

    
<h1><a>Life Conditions Survey</a></h1>
                
<form class="form_temp"   action="surveyIUEHQ34VX.php" method="POST">
        
        <div class="form_description">
        
        <center><h2 style ="font-size: 200%; font-weight: bold;">The Life Conditions Survey</h2></center>
        
        
          <div style="padding-bottom: 100px;"></div> 
        
        <p style = "text-align:center; font-size: 120%">Welcome! Thank you for participating in the Life Conditions Survey.  This survey is best carried out on a desktop or a laptop computer.  We hope this will be a fun experience for you. Enjoy!
        
        <br><br>
        
        <p style="text-align:center; color : teal; font-size: 120%;">At the end of the survey, you will be given a completion code to enter in MTurk to receive the payment.</p>
	
		
		</div>
		
          <div style="padding-bottom: 50px;"></div> 			
				
		<!-- Get outputs from form to subsequent pages -->		
		<input type="hidden" name="page" value="1">
		<input type="hidden" name="lang" value="en">
		<input type="hidden" name="randurl" value="<?php echo $randurl; ?>" >
		<input type="hidden" name="ID" value="<?php echo $random; ?>" >
		<input type="hidden" name="ipaddress1" value="<?php echo $ipaddress1; ?>" >
		<input type="hidden" name="timewelcome" value="<?php echo $timewelcome; ?>" >
		
			
													
         <center>
         <input type="submit" name="newWelcomeSubmit" value="Click Here to Start >>" class="w3-button w3-green" style ="width:250px;">
        </center>						
		
		
		
		
		
		</form>	
		
		
	</div>

	</body>

</html>
