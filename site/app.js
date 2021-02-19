let intro = document.querySelector('.intro');
let logo = document.querySelector('.logo-header');
let logoSpan = document.querySelectorAll('.logo');

window.addEventListener('DOMContentLoaded', ()=>{

	setTimeout(() => {

			logoSpan.forEach((span, idx) => {
				setTimeout(() => {
					span.classList.add('active');
				}, (idx + 1) * 400)
			});

			setTimeout(() => {
				logoSpan.forEach((span, idx) => {

					setTimeout(() => {
						span.classList.remove('active');
						span.classList.add('fade');
					}, (idx + 1) * 50)
				})
			}, 2000);

			setTimeout(() => {
					intro.style.top = '-100vh';
			}, 2300)
	})
})

/*
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 
*/