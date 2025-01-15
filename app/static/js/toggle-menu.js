let menu = document.getElementById("menu");
let img = document.getElementById("icon");

img.onclick = toggleMenu;

console.log(menu);
console.log(img);

toggle = 0;
menu.style.display = "none";


function toggleMenu(){
	if(toggle == 0){
		menu.style.display = "flex";
		toggle = 1;
	}
	else{
		menu.style.display = "none";
		toggle = 0;
	}
	
}