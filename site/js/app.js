let intro = document.querySelector('.intro');
let logo = document.querySelector('.logo-header');
let logoSpan = document.querySelectorAll('.logo');
var button = document.getElementById('menu-button');

window.addEventListener('DOMContentLoaded', ()=>{

	button.style.display ="none";

	setTimeout(() => {

			logoSpan.forEach((span, idx) => {
				setTimeout(() => {
					span.classList.add('active');
				}, (idx + 1) * 50)
			});

			setTimeout(() => {
				logoSpan.forEach((span, idx) => {

					setTimeout(() => {
						span.classList.remove('active');
						span.classList.add('fade');
					}, (idx + 1) * 50)
				})
			}, 1000);

			setTimeout(() => {
					intro.style.top = '-100vh';
			}, 1000)

			setTimeout(() => {
					button.style.display ="block";
			}, 1650)
	})

})
