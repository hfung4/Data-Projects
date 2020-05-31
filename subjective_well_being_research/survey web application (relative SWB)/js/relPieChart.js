
function getChartUnemploy(unemploy, name){	 
 
// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChartUnemploy);

// Draw the chart and set the chart values
function drawChartUnemploy() {
	
	var subjectName = String(name);
	var employ = 100 -unemploy;
	var unemployLabel = 'Not working but looking for job';
	var employLabelTemp = 'Working';
	
	var nameStr = " (like " + subjectName + ")";
	
	employLabel = employLabelTemp + nameStr;
    
  var data = google.visualization.arrayToDataTable([
  ['Employed/Unemployed', 'Proportion'],
  [employLabel, employ],
  [unemployLabel, unemploy],
  
]);

  // Optional; add a title and set the width and height of the chart
  var options = {
		width:580, 
		height:200, 
		is3D: true, 
		legend: {position:'labeled', textStyle: {fontSize: '12', color: 'red'}}, 
		pieSliceText: 'none', 
		tooltip: {text: 'percentage'},
		colors: ['#ffb380', '#ffe0cc']
		
		
		};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechartUnemploy'));
  chart.draw(data, options);
}


}







function getChartPartner(partnerPer, name, partnerBool){	 
 
// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChartPartner);

// Draw the chart and set the chart values
function drawChartPartner() {
	
	var subjectName = String(name);
	var alonePer = 100 -partnerPer;
	var aloneLabelTemp = 'Lives alone';
	var partnerLabelTemp = 'Lives with a partner';
	
	var nameStr = " (like " + subjectName + ")";
	
	
	if(partnerBool ==1)
	{
		partnerLabel = partnerLabelTemp + nameStr;
		aloneLabel = aloneLabelTemp;
	}
	else
	{
		partnerLabel = partnerLabelTemp;
		aloneLabel = aloneLabelTemp + nameStr;
		
	}
	

  var data = google.visualization.arrayToDataTable([
  ['Live alone/Live with partner', 'Proportion'],
  [partnerLabel, partnerPer],
  [aloneLabel, alonePer],
  
]);

  // Optional; add a title and set the width and height of the chart
  var options = {
		width:580, 
		height:200, 
		is3D: true, 
		legend: {position:'labeled', textStyle: {fontSize: '12', color: 'blue'}}, 
		pieSliceText: 'none', 
		tooltip: {text: 'percentage'},
		colors: ['#99e6ff', '#ccf2ff']
		
		
		};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechartPartner'));
  chart.draw(data, options);
}


}






function getChartTrust(trustPer, name, trustBool){	 
 
// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChartTrust);

// Draw the chart and set the chart values
function drawChartTrust() {
	
	var subjectName = String(name);
	var notTrustPer = 100 -trustPer;
	var notTrustLabelTemp = 'Does not trust people';
	var trustLabelTemp = 'Trusts people';
	
	var nameStr = " (like " + subjectName + ")";
	
	
	if(trustBool ==1)
	{
		trustLabel = trustLabelTemp + nameStr;
		notTrustLabel = notTrustLabelTemp;
	}
	else
	{
		trustLabel = trustLabelTemp;
		notTrustLabel = notTrustLabelTemp + nameStr;
		
	}
	

  var data = google.visualization.arrayToDataTable([
  ['Reported Trust', 'Proportion'],
  [trustLabel, trustPer],
  [notTrustLabel, notTrustPer],
  
]);

  // Optional; add a title and set the width and height of the chart
  var options = {
		width:580, 
		height:200, 
		is3D: true, 
		legend: {position:'labeled', textStyle: {fontSize: '12', color: 'purple'}}, 
		pieSliceText: 'none', 
		tooltip: {text: 'percentage'},
		colors: ['#d1b3ff', '#e0ccff']
		
		
		};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechartTrust'));
  chart.draw(data, options);
}


}
