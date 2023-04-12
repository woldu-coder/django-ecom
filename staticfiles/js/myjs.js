// function signUp(){
// 	let fname = document.querySelector('.firstname').value;
// 	let lname = document.querySelector('.lastname').value;
// 	let phone = document.querySelector('.phonenumber').value;
// 	let email = document.querySelector('.email').value;
// 	let pass1 = document.querySelector('.password1').value;
// 	let pass2 = document.querySelector('.password2').value;

// 	console.log(fname, lname, phone, email, pass1, pass2);

// }



function userLocations(lat, lng){
	const url = '/location/'

	fetch(url, {
		method: "POST",
		headers:{
			"Content-Type": 'application/json',
			"X-CSRFToken": csrftoken
		},
		body:JSON.stringify({'lat':lat, 'lng':lng}),
	}).then((response)=>{
		return response.json();
	}).then((data)=>{
		console.log('Successfully completed'); 
	})
}
function success(position){
	const lat = position.coords.latitude;
	const lng = position.coords.longitude;
	console.log("User's Position could accessed!")
	console.log("Latitude: ", lat);
	console.log("Longitude: ", lng);
	userLocations(lat, lng);
}
function error(err){
	console.log("Cannot access the user's locations");
}

function locations(){
	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(success, error, {
			enableHighAccuracy:true,
			timeout: 5000,
			maximumAge: 1000
		});
	}
}
locations();