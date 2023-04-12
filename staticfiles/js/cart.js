var updateBtns = document.getElementsByClassName('update-cart');
var deleteBtns = document.getElementsByClassName('delete-btn');
var disableBtns = document.getElementsByClassName('disable-btn');

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}


for (i = 0; i < deleteBtns.length; i++) {
	deleteBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log(productId)
		console.log(action)

		if (user == 'AnonymousUser'){
			// addCookieItem(productId, action)
			console.log("AnonymousUser")
		}else{
			console.log("Not AnonymousUser")
			// updateUserOrder(productId, action)
		}
	})
}


for (i = 0; i < disableBtns.length; i++) {
	disableBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

		console.log(productId)
		console.log(action)
		// if (user == 'AnonymousUser'){
		// 	addCookieItem(productId, action)
		// }else{
		// 	updateUserOrder(productId, action)
		// }
	})
}