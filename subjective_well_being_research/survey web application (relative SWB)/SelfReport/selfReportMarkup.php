<?php

/** The Self-Reports on Life Satisfication Survey (page 1) */

//Initialization
$selfReport_startTime = date('h:i:s a', time());  //Time at the start of the Self Report Survey  
$percentComplete='12.5';  // 1/8th of the entire survey is completed.
$prompts=$Survey_Prompts_Displayed; // Display prompt text (from dictionaries.php)

//Suffle the Self Report LS questions array so that the order of the questions would be randomized
$Suffled_SelfReport_Questions = shuffle_assoc($Questions_SelfReportLs_Displayed);

$keyArray=array_keys($Suffled_SelfReport_Questions);


foreach ($keyArray as $k) {
    $keySlider[] = $k."slider";
    $keyAmount[] = $k."amount";
    $keyDisp[] = $k."displayAmount";
}

foreach ($Suffled_SelfReport_Questions as $s){
	$questionText[] = $s;
}

 
 /* NOTE:  Always use this snippet if I want to use php variables in html 
 * 
 * <?php echo $myVar; ?>
 */
 
 ?>







<body id="main_body_SelfReport" >

<img id="top" src="images/top.png" alt="">

 
 
 
<div style ="position:absolute; top:20; right:20px;"> 
<div class="c100 p12">
	<span>12%</span>
	<div class="slice">
		<div class="bar"></div>
		<div class="fill"></div>
	</div>
<p style="font-size:15%; color:#428bca; position: relative; top: 105px; "> Your progress </p>
</div>

</div>






<div id="form_container">
<h1><a><?php echo $prompts["title"]; ?></a></h1>


<form class="form_temp"  method="POST" action="surveyIUEHQ34VX.php">




<div class="form_description">

<h2><strong><?php echo $prompts["title"]; ?></strong></h2>


<br>
<p>
<strong><?php echo $prompts["info"]; ?></strong>
</p>


</div>


<br><br>

<ul >
	

		



<span style="font-size:110%; text-align:left; font-weight:bold; color:#51A5BA;">  <?php echo $prompts["satisfaction"]; ?> </span>
<span id="overalldisplayAmount" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:110%"></span>

<br><br>


<div id="overallslider"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="overallamount" name= "overall">

<br><br><br><br><br>




<span style="font-size:110%; text-align:left; font-weight:bold; color:#51A5BA;">  <?php echo $questionText[0]; ?> </span>
<span id="<?php echo $keyDisp[0]; ?>" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:110%"></span>

<br><br>


<div id="<?php echo $keySlider[0]; ?>"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="<?php echo $keyAmount[0]; ?>" name= "<?php echo $keyArray[0]; ?>">

<br><br><br><br><br>




<span style="font-size:110%; text-align:left; font-weight:bold; color:#51A5BA;">  <?php echo $questionText[1]; ?> </span>
<span id="<?php echo $keyDisp[1]; ?>" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:110%"></span>

<br><br>


<div id="<?php echo $keySlider[1]; ?>"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="<?php echo $keyAmount[1]; ?>" name= "<?php echo $keyArray[1]; ?>">

<br><br><br><br><br>



<span style="font-size:110%; text-align:left; font-weight:bold; color:#51A5BA;">  <?php echo $questionText[2]; ?> </span>
<span id="<?php echo $keyDisp[2]; ?>" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:110%"></span>

<br><br>


<div id="<?php echo $keySlider[2]; ?>"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="<?php echo $keyAmount[2]; ?>" name= "<?php echo $keyArray[2]; ?>">

<br><br><br><br><br>




<span style="font-size:110%; text-align:left; font-weight:bold; color:#51A5BA;">  <?php echo $questionText[3]; ?> </span>
<span id="<?php echo $keyDisp[3]; ?>" readonly="readonly" style="border:0; color:#f6931f; font-weight:bold; font-size:110%"></span>

<br><br>


<div id="<?php echo $keySlider[3]; ?>"></div>
<divMin>Very Dissatisfied (0)</divMin> <divMax>Very Satisfied (10)</divMax>   
<input type="hidden" id="<?php echo $keyAmount[3]; ?>" name= "<?php echo $keyArray[3]; ?>">

<br><br><br><br><br>







<center>
<li class="buttons" >
<input type='submit' name='selfReportSubmit' value='Next'>
</li>
</center>


<!-- Hidden inputs": variables that I want to send from page 1 to the subsequent page -->	
<input type="hidden" name="page" value="2">
<input type="hidden" name="lang" value="<?php echo $_POST['lang']; ?>">
<input type="hidden" name="randurl" value="<?php echo $_POST['randurl']; ?>" >
<input type="hidden" name="ID" value="<?php echo $_POST['ID']; ?>" >
<input type="hidden" name="selfReport_startTime" value="<?php echo $selfReport_startTime; ?>" >




</ul>



</form>		

</div>


<img id="bottom" src="images/bottom.png" alt="">


</body>


</html>





