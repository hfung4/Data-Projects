<?php

/**dictionaries.php
 * 
 * The module contains different "question" and "prompt" arrays.  The elements of these arrays are texts for the webpages (ex: vignettes, Self Report Life Satisfication)
 * 
 * The variable $language is used to decide whether the English or French texts should be used
 * 
 * The question and prompt arrays will be used in the ShowVignettes, demographics_new, and various other modules to 
 * displayed text in the different survey pages.
 * 
 */


/*1. The text for the QUESTIONS in the Self Reported Life Satisfication Survey*/

$Questions_SelfReportLs_English = array(

"income" => "How satisfied are you with the total income of your household?", 

"job" => "How satisfied are you with your job and/or other daily activities?",

"social" => "How satisfied are you with your social contacts and family life?", 

"health" => "How satisfied are you with your overall health?", 

);



$Questions_SelfReportLs_French =array(

"income" => "Quel sentiment éprouvez-vous à l'égard de votre salaire total de votre ménage?", 

"job" => "Quel sentiment éprouvez-vous à l'égard de votre travail actuel et autres activités quotidiennes?", 

"social" => "Quel sentiment éprouvez-vous à l'égard de votre vie sociale et vos rapports familiaux? ", 

"health" => "Quel sentiment éprouvez-vous à l'égard de votre état de santé en général?" , 

"job1" => "Quel sentiment éprouvez-vous à l'égard de votre vie en général?"

);




/*2. The text for the PROMPTS in all Surveys*/


$Survey_Prompts_English = array(

"slider" => "Use the slider",

"title" => "Self Report on Life Satisfaction", 

"info"=>"Please use the sliders to answer the following questions.",

"warn" => "Warning: You have already submitted an answer for this vignette question. Any new answers you submit will NOT be recorded.",

"satisfaction" => "How satisfied are you with your life overall?", 

"progress1" => "You have completed ", 

"progress2" => " of the survey.", 

"lExtreme" => "Very Dissatisfied", 

"rExtreme" => "Very Satisfied", 

"next" => "Next", 

"vignettePrompt" => "This person's life satisfaction is:", 

"noresp" => "No response"

);


$Survey_Prompts_French = array(

"slider" => "Utilisez léchelle", 

"title" => "Rapport Personnel sur votre <br>Satisfaction de Vie", 

"info" => "Veuillez utiliser l'échelle ci-dessous en le faisant glisser sur la note appropriée qui va de 0 à 10. La note 0 indique un opinion très insatisfait et une note de 10 est très satisfait.", 

"warn" => "Avertissement: Actualiser cette page pendant le sondage perdriez toutes vos réponses.", 

"satisfaction" => "Quel sentiment éprouvez-vous à l'égard de votre vie en général?", 

"progress1" =>"Vous avez complété ", 

"progress2" =>" du sondage.", 

"lExtreme" => "Très Insatisfait", 

"rExtreme" => "Très Satisfait", 

"next" => "Prochain",

"vignettePrompt" => "La satisfaction à l’égard de la vie de cette personne est :", 

"noresp" => "Aucune Réponse"

); 







/*3. The text for the Vignette Questions*/


$Vignette_Prompts_English = array(

"note" => "The following vignette questions are the most important part of the survey. Please take the time to read each question and think about your answer carefully.",

"note2" => "You will be presented with five vignettes describing different hypothetical living situations. Use the slider to record what you believe each individual's life satisfaction is most likely to be.",

"note3" => "If you need information on how an individual compares to others in his/her community, click on the buttons below the vignette to get more information.",

"note4" => "For example, clicking on the Income button will reveal how the individual's household income compares to his/her community.",

"note5" => "Please use the slider to record what you believe this individual's life satisfaction is likely to be.",

"note6" => "Please be reminded that there are 12 buttons beneath the vignette description.  You can click on these buttons to reveal additional information on how this individual compares to his/her community.  Note the 3 seconds delay before the information appears.",

"warn" => "Warning: You have already submitted an answer for this vignette question. Any new answers you submit will NOT be recorded.",

"info" => "Please use the slider and rate on a scale from 0 to 10, what you believe this individual's life satisfaction is (with 0 being extremely dissatisfied and 10 being extremely satisfied).", 

"ref" => "For your reference, here are your answers to previous vignettes: ", 

"resp" => "Your Response: ", 

"almost" => "There are only two vignettes left!  We appreciate your effort!", 

"motivate" => "There are only two vignettes left!  We are very happy with your progress.  We will pay you an extra five cents for your great effort!"

);



$Vignette_Prompts_French = array(

"note" =>  "Notez: Les questions qui suivent sont les plus importantes de ce sondage. Veuillez, s’il vous plait, prendre le temps de lire chacune de ces questions et d’y réfléchir au préalable, avant d’y répondre.</i><br><br> 
Vous allez être présentés à six différentes vignettes dont chacune décrivant une situation de vie hypothétique bien particulière. Veuillez utiliser l’échelle en le faisant glisser sur la note appropriée qui va de 0 à 10. La note 0 indique un opinion très insatisfait et une note de 10 est très satisfait.<i><br><br> À la fin de cette section, vous allez devoir répondre à des questions de compréhension par rapport au contenu des vignettes. Il est donc très important que vous apportiez une attention particulière à chaque vignette pour répondre aux questions correctement.", 

"warn" => "Avertissement: Actualiser cette page pendant le sondage perdriez toutes vos réponses.</i></p>", 

"info" => "Veuillez utiliser l’échelle en le faisant glisser sur la note appropriée qui va de 0 à 10, qui correspond à la satisfaction à l’égard de la vie de cette personne. ", 

"ref" => "Pour votre reference, voici vos réponses aux vignettes prévues:", 

"resp" => "Votre Réponse: ", 

"almost" =>"Le sondage est presque terminée.", 

"motivate" => "Vouz serez payé cinq cents en plus pour faire un bon travail!"

);




/*4. The text for the Comprehension Tests*/

$Comprehension_Text_English = array( 
"title" => "Vignette Comprehension Questions", 

"note" => "Please answer the following comprehension questions about the previous vignettes. This is just to show us that you have read and understood the vignettes.", 

"note2" => "Don't worry, you do not need to get all the correct answers on these questions in order to receive payment, but please try your best.", 

"health" => "Question 1: Which of the following attributes related to the individual's health has appeared in at least one of the vignettes?", 

"social" => "Question 1: Which of the following attributes related to the individual's social and family life has appeared in at least one of the vignettes?", 

"attrQuestion" => "Question 2: Which of the attributes about the individuals' life has appeared in at least one of the vignettes?"

);


// French translation is incomplete!

$Comprehension_Text_French = array( 

"title" => "Questions de Compréhension ", 

"note" => "Veuillez s’il-vous-plait répondre aux questions de compréhensions suivantes.<br><b> Prenez note que vous ne devez pas recevoir cent pourcent sur ces questions pour recevoir votre paiement, mais s’il-vous-plait essayer de faire de votre mieux.", 

"health" => "Lesquelles des descriptions de santé suivantes ne sont apparues dans aucunes des vignettes que vous avez reçu?",

"marital"=>"Lesquelles des descriptions d'état civil suivantes sont apparues dans au moins une des vignettes que vous avez reçu?<br>",

"leisure" => "Lesquelles des descriptions suivantes sont apparues dans au moins une des vignettes que vous avez reçu?"

); 




/*5. The Text for Demographics Questions*/

$Demographics_Text_English = array(

"title" => "Respondent Demographics", 

"age" => "What is your age?", 

"sex" => "What is your gender?", 

"edu" => "What is the highest level of education you have completed?", 

"M" => "Male", 

"F" => "Female", 

"choose" => "Please choose only one of the following: <br>", 

"somehigh" => "Some high school", 

"highgrad" => "High school graduate", 

"somecollege" => "Some college or university", 

"bachelor" => "Bachelor's Degree", 

"master" => "Master's Degree", 

"doctor" => "Doctoral Degree", 

"pro" => "Professional Degree", 

"status" => "What is your martial status? <br>", 

"single" => "Single", 

"partner" => "Married or Cohabitating", 

"div" => "Divorced", 

"widow" => "Widowed", 

"job" => "Are you currently employed?", 

"y" => "Yes", 

"nobut" => "No, and looking for a job", 

"no" => "No, and <u>not</u> looking for a job", 

"income" => "What is your own annual income (before taxes)? <br>", 

"choosecategory" => "Or, choose from one of the categories below<br>", 

"lessthan" => "Less than ", 

"morethan" => "More than ", 

"houseincome" => "What is your total annual household oncome (before taxes)? <br>",

"enterval" => "Please enter the value: <br>", 

"peoplecontributing" => "How many people contribute to the total annual household income?<br>", 

"onlyone" => "Please choose only one of the following: <br>", 

"housesize" => "How many people are there in your household?<br>", 

"ageagain" => "What is your age (again)?<br>", 

"placeslived" => "Please list any countries (up to 5) that you have lived in: <br>", 

"ifUSA" => "If you live in the US, please indicate which state you live in below. ", 

"indiaState" => "Which state in India do you reside in? ", 

"comment" => "Please enter comments you may have about the survey to help improve its usability: ", 

"prompt" => "Please answer the following questions on your demographic infomation.", 

"olderthan" => "Older than ", 

"youngerthan" => "Younger than ", 

"country" => "Country ", 

"code" => "To generate your completion code, please enter your age in years: <br> (Your code will be displayed on the next page.)",  

"finish" => "Click here to finish the survey and retrieve your completion code: <i><b>(Do not forget to submit the survey or you cannot receive payment.)</i></b><br>"

);


$Demographics_Text_French = array(

"age" => "Quel est votre âge?" , 

"title" => "Caractéristiques Démographiques<br>des Répondants", 

"sex" => "Quel est votre sexe?", 

"M" => "Male", 

"F" =>"Femelle", 

"edu" => "Quel est le plus haut niveau d’éducation que vous avez complété?", 

"choose" => "Choisisez seulment une des choix suivantes: <br>" , 

"somehigh" => "lycée partiellement complété" ,

"highgrad" => "diplôme de lycée obtenu", 

"somecollege" => "université partiellement complétée", 

"bachelor" => "Baccalauréat (License)", 

"master" => "Maitrise " , 

"doctor" => "Degré Doctoral", 

"pro" => "Degré Professionnel", 

"status" => "Quel est votre état matrimonial? <br>" ,

"single" => "célibataire" , 

"partner"=>"marié/conjoint de fait", 

"div"=>"divorcé(e)" , 

"widow"=>"veuf/veuve" , 

"job"=>"Occupez-vous un emploi aujourd’hui?" ,

"y"=> "Oui" , 

"nobut"=>"Non et je recherche un emploi", 

"no"=>"Non et <u>je ne recherche pas</u> un emploi", 

"income"=>"Quel est votre salaire annuel (avant imposition)?", 

"choosecategory"=> "Ou, choissisez une valeur des categories ci-dessous: <br>", 

"lessthan"=>"Moins de ", 

"morethan"=>" Plus de ", 

"houseincome"=>"Quel est le salaire annuel total de votre ménage avant l’imposition?" , 

"enterval" =>"<br>Entrez le valeur: <br>", 

"peoplecontributing"=>"Combien de personnes contribuent au salaire annuel total de votre ménage?<br>", 

"onlyone"=> "Choisissez seulment un des choix ci-dessous:<br>", 

"housesize"=>"Combien de personnes y-a-t’il dans votre ménage?<br>" , 

"ageagain"=>"Quel est votre âge (encore)? <br>" , 

"placeslived"=> "S’il-vous-plait énumérer (jusqu'a cinq) les pays où vous avez vécu.<br>" , 

"ifUSA"=>"Si vous vivez aux Etats-Unis, dans quel état vivez-vous?", 

"indiaState"=>"Donc quel état en Inde residez vous? ", 

"prompt"=>"Répondez aux questions suivantes.", 

"olderthan" => "Plus de ", 

"youngerthan"=> "Moins de ", 

"country"=>"Pays ", 

"code"=>"Pour recevoir votre code, s’il vous plait entrer votre âge en chiffres.<br> (Votre code va apparaitre sur la page suivante.)", 

"comment" =>"Veuillez nous faire part de vos impressions sur le questionnaire afin que nous puissions améliorer la qualité de celui-ci. <br>", 

"finish"=>"Cliquez ici pour finir ce questionnaire et obtenir votre code d’accès.<br> <i><b> (N'oubliez pas de soumettre le sondage ou vous ne pourrez pas recevoir le paiement.)</i><b><br>"

);


/* 6. Health Comprehension Questions for Vignettes */

$Health_Comp_English = array( 

"immune" => "has a weak immune system and gets sick quite often", 

"diabetes"=>"has diabetes and has difficulty managing it", 

"noprob" => "does not have mobility problems", 

"heart" => "has heart problems and tires easily", 

"asthma" =>"has asthma"

);

$Health_Comp_French = array ( 

"immune" => "un système immunitaire faible et tombe malade assez souvent", 

"diabetes"=>"souffre de diabète et à du mal a le gérer " ,

"noprob"=>"Pas de problèmes de mobilité", 

"heart"=> "des problèmes avec son coeur et se fatigue facilement",

"asthma"=>"a de l'asthme"

);



/* 7. Text related to Leisure Questions*/

$Leisure_English= array(

"age"=>"age",

"mar"=>"marital status", 

"h"=>"health", 

"e"=>"education", 

"r"=>"religion",

"hrs"=>"working hours",

"prof"=>"profession",

"ci"=>"community involvement"

);


$Leisure_French= array(

"age"=>"âge", 

"mar"=>"état civil", 

"h"=>"santé physique", 

"e"=>"éducation", 

"r" => "religion", 

"hrs"=>"heures de travail", 

"prof"=>"profession", 

"ci"=>"participation dans la communauté"

);



/* 8. Text related to Marriage Questions */

$Marriage_Questions_English= array(

"single"=>"single",

"divorced2children0"=>"recently been divorced with no children", 

"widow0"=>"a widow who misses his/her spouse and has no children", 

"mar0childrenwell"=>"happily married with no children", 

"martwogood"=>"married for the second time, has two children from the first marriage and sees them often",

"divorced2children1"=>"divorced with two children and sees them often ", 

"martwo"=>"married for the second time, has one son from the first marriage but does not see him often ", 

"mar2childrenno"=>"married with two children and does not get along well with his/her spouse (they often have arguements) ", 

"divorced2children2"=>"divorced with two children who visit only once a year","widow"=>"a widow who misses his/her spouse and has two children ",

"marnoclose"=>"married with no children and does not spend much time with his/her spouse; they mostly lead their own lives",

"mar2childrenwell"=>"happily married with two children and gets along with them very well ", 

"wild1"=>"happily married with two children and enjoys hiking with his/her spouse",

"wild2"=>"a widow who misses his/her spouse but spends a lot of time traveling with friends"

);


$Marriage_Questions_French = array(

"single"=>"célibataire",

"divorced2children0"=>"recement divorcé" ,

"widow0" => " veuf et lui manque son épouse",

"mar0childrenwell"=> "heureusement marié sans enfants" , 

"martwogood"=> " marié pour la deuxième fois, a des enfants de leur second marriage, et les voit souvent", 

"divorced2children1"=> "divorcé avec deux enfants et les voit souvent" , 

"martwo"=>"marié pour la deuxième fois, a un enfant de la premiere mariage mais ne lui voit souvent" , 

"mar2childrenno"=>"marié avec deux enfants et ne s'entend pas avec son épouse (ils ont des arguments souvent)",

"divorced2children2"=>"divorcé avec deux enfants qui visitent seulment une fois par an" , 

"widow"=>" un veuf/veuve et il/elle lui manque" ,

"marnoclose"=>"marié sans enfants et ne prends pas beaucoup de temps avec son épouse; pour la plupart, ils vivent leurs propres vies", 

"mar2childrenwell"=>"heureusement marié avec deux enfants et s'entend très bien avec eux", 

"wild1"=>"heureusement marié avec deux enfants et aime la randonnée avec son épouse",

"wild2"=>"veuf/veuve qui leur epouse lui manque mais qui voyage souvent avec ses amis"

);



/* 9. Text on the EXIT page */


$Exit_English = array(

"thanks"=>"Thank you for completing the survey. Your completion code is:" , 

"payment"=>"To receive payment, enter the completion code above in MTurk"

);

$Exit_French = array(

"thanks" => "Merci pour avoir fini le sondage. Votre code d'achèvement est: ", 

"payment"=> "Pour recevoir paiement, veuillez rentrer ce même code sur MTurk."

);


$exit_all=array("en"=> $Exit_English, "fr"=>$Exit_French);



/* 10. Language Selection
 *  
 * Selects the language of the questions and prompts that are displayed 
 * on the survey pages.  This function is called in dictionaries.php to determine which
 * question and prompt text arrays should be used in the survey pages.
 */  
 
 $language = $_POST['lang']; // lanaguage selected (English or French)

 switch ($language)  
 {
	 //English is selected
	 case "en": 
	 
	 // English Self Reported Life Satisfication Questions
	 $Questions_SelfReportLs_Displayed = $Questions_SelfReportLs_English;
		
	 // English Prompts on All Surveys
	 $Survey_Prompts_Displayed = $Survey_Prompts_English;
		
	 // English Prompts on Vignettes  
	 $Vignette_Prompts_Displayed = $Vignette_Prompts_English;
		
	 // English Comprehension Text
	 $Comprehension_Text_Displayed = $Comprehension_Text_English;
		
	 // English Demographics Text
	 $Demographics_Text_Displayed = $Demographics_Text_English;
		
	 // English Health Comprehension Text in Vignettes
	 $Health_Comp_Displayed = $Health_Comp_English;
		
	 // English Leisure related Questions 
	 $Leisure_Displayed = $Leisure_English;
		
	 // English Marriage related Questions
	 $Marriage_Questions_Displayed = $Marriage_Questions_English;
		
	 // English Text on Exit Page
	 $Exit_Displayed = $Exit_English;

				
	break;
	
	
	 //French is selected
	 case "fr": 
	
	 // French Self Reported Life Satisfication Questions	
	 $Questions_SelfReportLs_Displayed = $Questions_SelfReportLs_French;
		
	 // French Prompts on All Surveys
	 $Survey_Prompts_Displayed = $Survey_Prompts_French;
		
	 // French Prompts on Vignettes  
	 $Vignette_Prompts_Displayed = $Vignette_Prompts_French;
		
	 // French Comprehension Text
	 $Comprehension_Text_Displayed = $Comprehension_Text_French;
		
	 // French Demographics Text
	 $Demographics_Text_Displayed = $Demographics_Text_French;
		
	 // French Health Comprehension Text in Vignettes
	 $Health_Comp_Displayed = $Health_Comp_French;
		
	 // French Leisure related Questions 
	 $Leisure_Displayed = $Leisure_French;
		
	 // French Marriage related Questions
	 $Marriage_Questions_Displayed = $Marriage_Questions_French;
		
	 // French Text on Exit Page
	 $Exit_Displayed = $Exit_French;
		
	break;	
}	






?>
