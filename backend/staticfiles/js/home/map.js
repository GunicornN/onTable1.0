
function getCoordinate(address){
    const url_api = 'https://maps.googleapis.com/maps/api/geocode/json?address=';
    var value = 'address=42190+charlieu';
    var settings = {
      
      "url": "https://maps.googleapis.com/maps/api/geocode/json?address="+value+'&key=REDACTED_GOOGLE_MAPS_KEY',
      "method": "GET",
      "timeout": 0,
    };

    $.ajax(settings).done(function (response) {
      console.log(response);
    });

}



// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 46.169940925680805, lng: 4.123306276442684 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }