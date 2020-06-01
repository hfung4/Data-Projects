<?php


//prompts 
$comp = $Comprehension_Text_Displayed;



/*For question 1, randomly select between a "health related question",
or a "social life" related question.
*/

$HealthOrSoc = rand(0,1);  //0 is health, 1 is social

if($HealthOrSoc == 0)
{
	$compQuestion1Prompt = $comp["health"];
}
else
{
	$compQuestion1Prompt = $comp["social"];
}


//run python code to generate Q1
$cmdQ1 = "python compTest/compTest_Question1.py $HealthOrSoc";

//get output from python
$compTestSelection_Q1 = shell_exec($cmdQ1);

//decode from json to associative array
$compQ1Decoded = json_decode($compTestSelection_Q1,true);

$Q1_ArrayKeys = array_keys($compQ1Decoded);
$Q1_ArrayVals = array_values($compQ1Decoded); 



//run python code to generate Q2
$cmdQ2 = "python compTest/compTest_Question2.py";

//get output from python
$compTestSelection_Q2 = shell_exec($cmdQ2);

//decode from json to associative array
$compQ2Decoded = json_decode($compTestSelection_Q2,true);

$compQ2Decoded_shuffled = shuffle_assoc($compQ2Decoded);


$Q2_ArrayKeys = array_keys($compQ2Decoded_shuffled);
$Q2_ArrayVals = array_values($compQ2Decoded_shuffled); 



//Update the "viewed" flag to check if the user has already accessed the comp test page
$compTestArray['visitedComp'] = 1;

//Update whether social or health question is randomly selected for comp test Q1

if($HealthOrSoc == 1)  //Social Question selected for Q1
{
	$compTestArray['SocialTestSelected'] = 1;
}


//update mysql row
sqlRowUpdate('USA_responses_2017', $compTestArray, $_POST['ID']);



?>





<body id="body_CompTest" >

<img id="top" src="images/top.png" alt="">



<div style ="position:absolute; top:20; right:20px;" 
<div class="c100 p88">
	<span>88%</span>
	<div class="slice">
		<div class="bar"></div>
		<div class="fill"></div>
	</div>
<p style="font-size:15%; color:#428bca; position: relative; top: 105px; "> Your progress </p>
</div>

</div>




<div id="form_container">

<h1><a>The Vignette Comprehension Test</a></h1>

<form class="form_temp"  action="surveyIUEHQ34VX.php" method="POST">
	
<!-- Hidden inputs": variables that I want to send from page 6 to the subsequent page -->	
<input type="hidden" name="page" value="8">
<input type="hidden" name="lang" value="<?php echo $_POST['lang']; ?>">
<input type="hidden" name="randurl" value="<?php echo $_POST['randurl']; ?>" >
<input type="hidden" name="ID" value="<?php echo $_POST['ID']; ?>" >
<input type="hidden" name="compTest_startTime" value="<?php echo $compTest_startTime; ?>" >
	


<div class="form_description">


<h2><strong>The Vignette Comprehension Test</strong></h2>

<br>
<br>
<p><?php echo $comp["note"]; ?></p>


<p style ="color:#29a3a3;"><?php echo $comp["note2"]; ?></p>

<p style = "color: red"> Warning: Please do not push the refresh or back button on your browser; otherwise all your responses will be lost and you would not be paid.</p>


<br><br>
		
</div>						
<ul >


<label class="description" for="element_1"><?php echo $compQuestion1Prompt; ?></label>	
	
<li id="li_1" >

<span>
<input type="hidden" name="<?php echo $Q1_ArrayKeys[0]; ?>" value="0" />
<input id="element_1_1" name="<?php echo $Q1_ArrayKeys[0]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_1_1"><?php echo $Q1_ArrayVals[0]; ?></label>

<input type="hidden" name="<?php echo $Q1_ArrayKeys[1]; ?>" value="0" />
<input id="element_1_2" name="<?php echo $Q1_ArrayKeys[1]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_1_2"><?php echo $Q1_ArrayVals[1]; ?></label>

<input type="hidden" name="<?php echo $Q1_ArrayKeys[2]; ?>" value="0" />
<input id="element_1_3" name="<?php echo $Q1_ArrayKeys[2]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_1_3"><?php echo $Q1_ArrayVals[2]; ?></label>

<input type="hidden" name="<?php echo $Q1_ArrayKeys[3]; ?>" value="0" />
<input id="element_1_4" name="<?php echo $Q1_ArrayKeys[3]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_1_4"><?php echo $Q1_ArrayVals[3]; ?></label>

<input type="hidden" name="<?php echo $Q1_ArrayKeys[4]; ?>" value="0" />
<input id="element_1_5" name="<?php echo $Q1_ArrayKeys[4]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_1_5"><?php echo $Q1_ArrayVals[4]; ?></label>
</span>

 
</li>		


<br><br>

<label class="description" for="element_2"><?php echo $comp["attrQuestion"]; ?>
</label>

<li id="li_2" >

<span>

<input type="hidden" name="<?php echo $Q2_ArrayKeys[0]; ?>" value="0" />
<input id="element_2_1" name="<?php echo $Q2_ArrayKeys[0]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_1"><?php echo $Q2_ArrayVals[0]; ?></label>

<input type="hidden" name="<?php echo $Q2_ArrayKeys[1]; ?>" value="0" />
<input id="element_2_2" name="<?php echo $Q2_ArrayKeys[1]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_2"><?php echo $Q2_ArrayVals[1]; ?></label>

<input type="hidden" name="<?php echo $Q2_ArrayKeys[2]; ?>" value="0" />
<input id="element_2_3" name="<?php echo $Q2_ArrayKeys[2]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_3"><?php echo $Q2_ArrayVals[2]; ?></label>

<input type="hidden" name="<?php echo $Q2_ArrayKeys[3]; ?>" value="0" />
<input id="element_2_4" name="<?php echo $Q2_ArrayKeys[3]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_4"><?php echo $Q2_ArrayVals[3]; ?></label>

<input type="hidden" name="<?php echo $Q2_ArrayKeys[4]; ?>" value="0" />
<input id="element_2_5" name="<?php echo $Q2_ArrayKeys[4]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_5"><?php echo $Q2_ArrayVals[4]; ?></label>


<input type="hidden" name="<?php echo $Q2_ArrayKeys[5]; ?>" value="0" />
<input id="element_2_6" name="<?php echo $Q2_ArrayKeys[5]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_6"><?php echo $Q2_ArrayVals[5]; ?></label>


<input type="hidden" name="<?php echo $Q2_ArrayKeys[6]; ?>" value="0" />
<input id="element_2_7" name="<?php echo $Q2_ArrayKeys[6]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_7"><?php echo $Q2_ArrayVals[6]; ?></label>


<input type="hidden" name="<?php echo $Q2_ArrayKeys[7]; ?>" value="0" />
<input id="element_2_8" name="<?php echo $Q2_ArrayKeys[7]; ?>" class="element checkbox" type="checkbox" value="1" >
<label class="choice" for="element_2_8"><?php echo $Q2_ArrayVals[7]; ?></label>

</span>

</li>


<center>
<li class="buttons">
<center><input type='submit' name='CompTestSubmit' id= 'CompSubmit' value='Submit'>
</li>
</center>



</ul>
		
</form>	
		
</div>
	
	
<img id="bottom" src="images/bottom.png" alt="">


</body>


</html>


