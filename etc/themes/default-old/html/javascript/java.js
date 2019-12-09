<!--

// Break out of frames if used - we don't like feeling enclosed

if (document.getElementById) { supportdhtml = 1; flavour = 'mozz'; }
else if (document.all) { var supportdhtml = 1; flavour = 'msie'; }
else { supportdhtml = 0; var flavour='none' }

function moveOver(image) {
	if(document.images) {
		image.src = image.src.substring(0,(image.src.indexOf(".gif"))) + "-h.gif";
	}
}

function moveOut(image) {
	if(document.images) {
		image.src = image.src.substring(0,(image.src.indexOf("-h.gif"))) + ".gif";
	}
}

function fade (elementToFade,fadeAmount) {
	activeElement = document.getElementById(elementToFade);
	
	if (document.all) {
		activeElement.style.filter="alpha(opacity="+fadeAmount+")";
	}
	else {
		fadeAmount = fadeAmount / 100;
		activeElement.style.MozOpacity = fadeAmount;
	}
}

//-->

