var dropdown = document.getElementById("dropdownMenu");
var inputDiv = document.getElementById("inputDiv");
var displayDiv = document.getElementById("displayDiv");
var lastData = null;
var lastPopup = null;
var queryTime = null;
const serverUrl = "http://localhost:8080/data";


function handleButtonClick(index, event) {
  console.log(`Handling ${index}`);
  if (!(lastData && lastData[index])) {
    console.log(`Not valid ${lastData} ${lastData[index]}`);
    return;
  }
  if(lastPopup)
  {
    lastPopup.remove();
  }

  const properties = Object.keys(lastData[index]);

  const popupHTML = `<div class="popup-header">
                        <span class="popup-close" onclick="closePopup()">X</span>
                    </div>
                    ${properties.map(property => `<p><strong>${property}:</strong> ${lastData[index][property]}</p>`).join('')}`;

  const popupDiv = document.createElement('div');
  popupDiv.innerHTML = popupHTML;
  popupDiv.classList.add('popup');

  popupDiv.style.left = `${event.pageX}px`;
  popupDiv.style.top = `${event.pageY}px`;
  popupDiv.style.zIndex = '1';
  popupDiv.style.position = 'absolute';

  document.body.appendChild(popupDiv);

  event.stopPropagation();

  document.addEventListener('click', closePopup);
  lastPopup = popupDiv;
}

function closePopup() {
  const popupDiv = document.querySelector('.popup');
  if (popupDiv) {
    document.body.removeChild(popupDiv);
    document.removeEventListener('click', closePopup);
    lastPopup = null;
  }
}


function removeEmptyStringAttributes(obj) {
    for (const key in obj) {
      if (obj.hasOwnProperty(key) && obj[key] === "") {
        delete obj[key];
      }
    }
  }

  function setErrorMessage(text)
  {
    displayDiv.innerHTML = `
    <div id="errorHolder">
        <h1>${text}</h1>
    </div>
    `
  }


  function generateAirlineHTML(id) {
    return `<div id="nameGrid">
      <div class="inputHolder">
        <label for="airlineId${id}">Airline ID</label>
        <input type="text" id="airlineId${id}" name="airlineId" class="inputField" required>
      </div>
  
      <div class="inputHolder">
        <label for="airlineName${id}">Name</label>
        <input type="text" id="airlineName${id}" class="inputField" name="airlineName" required>
      </div>
  
      <div class="inputHolder">
        <label for="airlineAlias${id}">Alias</label>
        <input type="text" id="airlineAlias${id}" class="inputField" name="airlineAlias">
      </div>
  
      <div class="inputHolder">
        <label for="iataCode${id}">IATA Code</label>
        <input type="text" id="iataCode${id}" class="inputField" name="iataCode">
      </div>
  
      <div class="inputHolder">
        <label for="icaoCode${id}">ICAO Code</label>
        <input type="text" id="icaoCode${id}" class="inputField" name="icaoCode">
      </div>
  
      <div class="inputHolder">
        <label for="callsign${id}">Callsign</label>
        <input type="text" id="callsign${id}" class="inputField" name="callsign">
      </div>
  
      <div class="inputHolder">
        <label for="country${id}">Country</label>
        <input type="text" id="country${id}" class="inputField" name="country" required>
      </div>
  
      <div class="inputHolder">
        <label for="active${id}">Active (Y/N)</label>
        <input type="text" id="active${id}" class="inputField" name="active" maxlength="1" required pattern="[YNyn]">
      </div>
    </div>`;
  }
  
  



  function generateAirportHTML(id, extra = "") {
    return `<div id="nameGrid">
      <div class="inputHolder">
        <label for="airportId${id}">Airport ID</label>
        <input type="text" id="airportId${id}" class="inputField" name="airportId" required>
      </div>
  
      <div class="inputHolder">
        <label for="airportName${id}">Name</label>
        <input type="text" id="airportName${id}" class="inputField" name="airportName" required>
      </div>
  
      <div class="inputHolder">
        <label for="city${id}">City</label>
        <input type="text" id="city${id}" class="inputField" name="city" required>
      </div>
  
      <div class="inputHolder">
        <label for="country${id}">Country</label>
        <input type="text" id="country${id}" class="inputField" name="country" required>
      </div>
  
      <div class="inputHolder">
        <label for="iataCode${id}">IATA Code</label>
        <input type="text" id="iataCode${id}" class="inputField" name="iataCode">
      </div>
  
      <div class="inputHolder">
        <label for="icaoCode${id}">ICAO Code</label>
        <input type="text" id="icaoCode${id}" class="inputField" name="icaoCode">
      </div>
  
      <div class="inputHolder">
        <label for="timezone${id}">Timezone</label>
        <input type="text" id="timezone${id}" class="inputField" name="timezone" required>
      </div>
  
      <div class="inputHolder">
        <label for="dst${id}">DST</label>
        <input type="text" id="dst${id}" class="inputField" name="dst"  required pattern="[EASOZNUeasoznu]">
      </div>
  
      <div class="inputHolder">
        <label for="tzDatabase${id}">Tz Database Timezone</label>
        <input type="text" id="tzDatabase${id}" class="inputField" name="tzDatabase" required>
      </div>

      ${extra}

    </div>`;
  }
  
  function findTripHTML(id){
    return `<div id="nameGrid">
    <div class="inputHolder">
      <label for="sourceAirport${id}">Source Airport</label>
      <input type="text" id="sourceAirport${id}" name="sourceAirport" class="inputField" required>
    </div>
    <div class="inputHolder">
      <label for="destinationAirport${id}">Destination Airport</label>
      <input type="text" id="destinationAirport${id}" name="destinationAirport" class="inputField" required>
    </div>
    </div>`;
  }
  


  function findDHopsCitiesHTML(id) {
    return generateAirportHTML(id, `<div class ="inputHolder"><label for="hopCount${id}">Hop Count</label>
    <input type="number" id="hopCount${id}" class="inputField" name="hopCount" required></div>`);
        
  }
  
  


function getAirportFormData(id) {
const airportId = document.getElementById(`airportId${id}`).value;
const airportName = document.getElementById(`airportName${id}`).value;
const city = document.getElementById(`city${id}`).value;
const country = document.getElementById(`country${id}`).value;
const iataCode = document.getElementById(`iataCode${id}`).value;
const icaoCode = document.getElementById(`icaoCode${id}`).value;
const timezone = document.getElementById(`timezone${id}`).value;
const dst = document.getElementById(`dst${id}`).value;
const tzDatabase = document.getElementById(`tzDatabase${id}`).value;


return {
    "Airport ID": airportId,
    "Name": airportName,
    "City": city,
    "Country": country,
    "IATA": iataCode,
    "ICAO": icaoCode,
    "Timezone": timezone,
    "DST": dst,
    "Tz database time zone": tzDatabase,
};
}

function getFindTripFormData(id){
  const sourceAirport = document.getElementById(`sourceAirport${id}`).value;
  const destinationAirport = document.getElementById(`destinationAirport${id}`).value;

  return{
    "Source Airport" : sourceAirport,
    "Destination Airport" : destinationAirport,
  };
}
  

function getAirlineFormData(id) {
    const airlineId = document.getElementById(`airlineId${id}`).value;
    const airlineName = document.getElementById(`airlineName${id}`).value;
    const airlineAlias = document.getElementById(`airlineAlias${id}`).value;
    const iataCode = document.getElementById(`iataCode${id}`).value;
    const icaoCode = document.getElementById(`icaoCode${id}`).value;
    const callsign = document.getElementById(`callsign${id}`).value;
    const country = document.getElementById(`country${id}`).value;
    const active = document.getElementById(`active${id}`).value;
    return {
      "Airline ID" : airlineId,
      "Name" : airlineName,
      "Alias" : airlineAlias,
      "IATA" : iataCode,
      "ICAO" : icaoCode,
      "Callsign" : callsign,
      "Country" : country,
      "Active" : active
    };
}

function findDHopsCitiesData(id) {
    var data = getAirportFormData(id);
    const hopCount = document.getElementById(`hopCount${id}`).value;
    data["Hop Count"] = hopCount;
    return data;
}




// function generateRouteHTML(id) {
//     return `<div id="nameGrid">
//       <label for="airline${id}">Airline</label>
//       <input type="text" id="airline${id}" name="airline" required>
  
//       <label for="airlineId${id}">Airline ID</label>
//       <input type="text" id="airlineId${id}" name="airlineId" required>
  
//       <label for="sourceAirport${id}">Source Airport</label>
//       <input type="text" id="sourceAirport${id}" name="sourceAirport" required>
  
//       <label for="sourceAirportId${id}">Source Airport ID</label>
//       <input type="text" id="sourceAirportId${id}" name="sourceAirportId" required>
  
//       <label for="destinationAirport${id}">Destination Airport</label>
//       <input type="text" id="destinationAirport${id}" name="destinationAirport" required>
  
//       <label for="destinationAirportId${id}">Destination Airport ID</label>
//       <input type="text" id="destinationAirportId${id}" name="destinationAirportId" required>
  
//       <label for="codeshare${id}">Codeshare (Y/N)</label>
//       <input type="text" id="codeshare${id}" name="codeshare" maxlength="1" required pattern="[YNyn]">
  
//       <label for="stops${id}">Stops</label>
//       <input type="text" id="stops${id}" name="stops" required>
  
//       <label for="equipment${id}">Equipment</label>
//       <input type="text" id="equipment${id}" name="equipment" required>
//     </div>`;
// }

// function getRouteFormData(id) {
//     const airline = document.getElementById(`airline${id}`).value;
//     const airlineId = document.getElementById(`airlineId${id}`).value;
//     const sourceAirport = document.getElementById(`sourceAirport${id}`).value;
//     const sourceAirportId = document.getElementById(`sourceAirportId${id}`).value;
//     const destinationAirport = document.getElementById(`destinationAirport${id}`).value;
//     const destinationAirportId = document.getElementById(`destinationAirportId${id}`).value;
//     const codeshare = document.getElementById(`codeshare${id}`).value;
//     const stops = document.getElementById(`stops${id}`).value;
//     const equipment = document.getElementById(`equipment${id}`).value;
  
//     return {
//       "Airline": airline,
//       "Airline ID": airlineId,
//       "Source Airport": sourceAirport,
//       "Source Airport ID": sourceAirportId,
//       "Destination Airport": destinationAirport,
//       "Destination Airport ID": destinationAirportId,
//       "Codeshare": codeshare,
//       "Stops": stops,
//       "Equipment": equipment
//     };
//   }

  
{/* <div class="inputHolder">
<label for="latitude${id}">Latitude</label>
<input type="text" id="latitude${id}" class="inputField" name="latitude" required>
</div>

<div class="inputHolder">
<label for="longitude${id}">Longitude</label>
<input type="text" id="longitude${id}" class="inputField" name="longitude" required>
</div>

<div class="inputHolder">
<label for="altitude${id}">Altitude</label>
<input type="text" id="altitude${id}" class="inputField" name="altitude" required>
</div> */}

  
function changeInputOptions() {
    var selectedOption = dropdown.value;
    displayDiv.innerHTML = "";

    inputDiv.innerHTML = "";

    switch (selectedOption) {
        case "0":
            inputDiv.innerHTML = generateAirlineHTML(0);
            break;
        case "1":
            inputDiv.innerHTML = generateAirportHTML(0);
            break;
        case "2":
            inputDiv.innerHTML = findDHopsCitiesHTML(0);
            break;
        case "3":
          inputDiv.innerHTML = findTripHTML(0);
          break
        default:
            break;
    }
}


function handleSubmit() {
    var selectedOption = dropdown.value;
    switch (selectedOption) {
        case "0":
            handleFindAirline();
            break;
        case "1":
            handleFindAirports();
            break;
        case "2":
            // handlefindRoutes();
            handleFindDHops();
            break;
        case "3":
            handleFindTrip();
        default:
            break;
    }
}



function displayData(data)
{

	// displayDiv.innerHTML = "";
    var newString;
    console.log(data);
  if(data.length === 0 || JSON.stringify(data) === '{}')
  {
      newString = "<h1 style=\"text-align: center;\">No Results Found.</h1>";
      displayDiv.innerHTML = newString;
      return;
  }
  var newString = `<h1 id = "queryResult" style = "padding-left: 10px;">${data.length} results found in ${queryTime} seconds </h1>`;

  newString += "<div id = \"nameGrid\">";
	for(let i = 0; i < data.length; ++i)
    {
        newString += `<button class="nameButton" onclick="handleButtonClick(${i},event)">${data[i]["Name"]}</button>`
    }
  newString += "</div>";
    displayDiv.innerHTML = newString;
}




function displayDHops(data, time) {
  var newString;
  var seenCities = new Set();
  
  if (data.length === 0 || JSON.stringify(data) === '{}') {
      newString = "<h1 style=\"text-align: center;\">No Results Found.</h1>";
      displayDiv.innerHTML = newString;
      return;
  }

  let previousLevel = 0;
  let i = 0;
  newString = `<h1 id="queryResult" style="padding-left: 10px;">${data.length} results found in ${queryTime} seconds </h1>`;
  
  while (i < data.length) {
      newString += "<div id=\"nameGrid\" style=\"border: 1px solid black; padding: 10px;\">";
      
      for (; i < data.length; ++i) {
          if (data[i]["Level"] == 0 && i != 0) {
              continue;
          }

          if (data[i]["Level"] != previousLevel) {
              previousLevel = data[i]["Level"];
              break;
          }

          const city = data[i]["City"];

          // Skip if the city has already been seen
          if (seenCities.has(city)) {
              continue;
          }

          seenCities.add(city);

          newString += `<p style="padding: 5px; background-color: rgb(152, 204, 250); border-radius: 5px;">${city} : ${data[i]["Level"]}</p>`;
      }

      newString += "</div>";
  }

  displayDiv.innerHTML = newString;
}

function displayDataTrip(data,time) {
  if (data.length === 0 || JSON.stringify(data) === '{}') {
      displayDiv.innerHTML = "<h1>No Results Found.</h1>";
      return;
  }
  let journeyPath = data.map((route, index) => {
      if (index === 0) {
          return (route["Source airport"] || 'Unknown') + 
                 (data.length > 1 ? " -> " : ""); // Add "->" only if there's more than one route
      } else {
          return route["Destination airport"] || 'Unknown';
      }
  }).join(" -> ");

  // Include destination of the last route if there's only one route
  if (data.length === 1) {
      journeyPath += " -> " + (data[0]["Destination airport"] || 'Unknown');
  }
  journeyPath = journeyPath.replace("->  ->", "->");

  let routeDetails = data.map(route => 
      `<tr>
          <td>${route["RouteID"] || 'N/A'}</td>
          <td>${route["Airline"] || 'N/A'} (${route["Airline ID"] || 'N/A'})</td>
          <td>${route["Source airport"] || 'N/A'}</td>
          <td>${route["Destination airport"] || 'N/A'}</td>
          <td>${route["Stops"] !== undefined ? route["Stops"] : 'N/A'}</td>
          <td>${route["Equipment"] || 'N/A'}</td>
          <td>${route["Codeshare"] || 'None'}</td>
      </tr>`
  ).join("");

  let tableHeader = `<tr><th>Route ID</th><th>Airline</th><th>Source</th><th>Destination</th><th>Stops</th><th>Equipment</th><th>Codeshare</th></tr>`;

  displayDiv.innerHTML = `
      <h1 id = "queryResult" style = "padding-left: 10px;">${data.length} results found in ${queryTime} seconds </h1>
      <div id='journeyGrid'>
          <p class="journey-path" style = "padding-left: 10px;">Journey Path: ${journeyPath}</p>
          <table class="route-details-table">
              ${tableHeader}
              ${routeDetails}
          </table>
      </div>
  `;
}




function handleFindAirline()
{
	var inputInfo = getAirlineFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findAirline", "conditions" : JSON.stringify(inputInfo)}, displayData);
}

function handleFindAirports()
{
	
    var inputInfo = getAirportFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findAirports", "conditions" : JSON.stringify(inputInfo)}, displayData);

}
function handlefindRoutes()
{
	
    var inputInfo = getRouteFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findRoutes", "conditions" : JSON.stringify(inputInfo)}, displayData);

}

function handleFindDHops()
{
    var inputInfo = findDHopsCitiesData(0);
    removeEmptyStringAttributes(inputInfo);
    var hopCount;
    if(!('Hop Count' in inputInfo))
    {
        setErrorMessage("No Hop Count");
        return;
        
    }
    hopCount = inputInfo["Hop Count"];
    delete inputInfo["Hop Count"];
    postData({"function" : "findDHopsCities", "conditions" : JSON.stringify(inputInfo), "Hop Count" : hopCount}, displayDHops);
}


function handleFindTrip(){
  var inputInfo = getFindTripFormData(0);
  removeEmptyStringAttributes(inputInfo);
  if(!('Destination Airport' in inputInfo))
  {
    setErrorMessage("No destination Airport");
    return;
  }
  if(!('Source Airport' in inputInfo))
  {
    setErrorMessage("No source Airport");
    return;
  }
  sourceAirport = inputInfo["Source Airport"]
  destinationAirport = inputInfo["Destination Airport"]
  postData({"function" : "findTrip", "Source Airport" : sourceAirport, "Destination Airport" : destinationAirport}, displayDataTrip)
}



function postData(data, callback)
{
	fetch(serverUrl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	})
	.then(response => response.json())
	.then(data => {
    console.log(data);
    console.log(data.hasOwnProperty('result'));
    if(data.hasOwnProperty('result'))
    {
      lastData = data['result'];
      queryTime = Number(data['time'].toPrecision(4));
      callback(data['result']);
    }
    else
    {
      lastData = data;
      callback(data);
    }

	})
	.catch((error) => {
		console.error('Error:', error);
	});
}

// Add an event listener to the dropdown
dropdown.addEventListener("change", changeInputOptions);
submitButton.addEventListener("click", handleSubmit);
changeInputOptions();