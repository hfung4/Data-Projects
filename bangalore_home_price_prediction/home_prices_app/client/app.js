

function getAvailValue() {
    var uiAvail = document.getElementsByName("uiAvail");
    for (var i in uiAvail) {
        if (uiAvail[i].checked) {
            return parseInt(i); //return "index of button" -1: np.nan, 0: Super built-up area, 1: Built-up area, 2: Plot area, 3: Carpet area
        }
    }
    return -1; // Invalid Value
}


function getAreaValue() {
    var uiArea = document.getElementsByName("uiArea");
    for (var i in uiArea) {
        if (uiArea[i].checked) {
            return parseInt(i); //return "index of button" -1: np.nan, 0: Ready to Move In, 1: Not Ready to Move In
        }
    }
    return -1; // Invalid Value
}


function onClickedEstimatePrice() {
    console.log("User clicked estimate button");
    var total_sqft = document.getElementById("uiSqft");
    var bedrooms = document.getElementById("uiBHK");
    var bathrooms = document.getElementById("uiBathrooms");
    var location = document.getElementById("uiLocations");
    var availability = getAvailValue();
    var area_type = getAreaValue();
    var estPrice = document.getElementById("uiEstimatedPrice");

    //endpoint for price prediction
    var url = "http://127.0.0.1:5000/predict_home_price"; //NOT using nginx
    //var url = "/api/predict_home_price"; // using nginx

    //make post call
    $.post(url, {
        total_sqft: parseFloat(total_sqft.value), //use .value if I get value using getElementById()
        size: bedrooms.value,
        bath: bathrooms.value,
        location: location.value,
        availability: availability,
        area_type: area_type
    }, function (data, status) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakhs</h2>";
        console.log(status);
    });
}





// Get the location names from "/get_possible_locations" and use it
// to populate the drop-down menu
function onPageLoad() {
    console.log("document loaded");
    var url = "http://127.0.0.1:5000/get_possible_locations"; // Use if NOT using nginx
    //var url = "/api/get_possible_locations"; // Use this if using nginx
    $.get(url, function (data, status) {
        console.log("We have responses from get_possible_locations request");
        if (data) {
            var locations = data.possible_locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for (var i in locations) {
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
}

window.onload = onPageLoad;