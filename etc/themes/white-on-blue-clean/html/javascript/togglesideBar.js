
function toggleSideBar () {
	if (document.getElementById) {
		sideBarElement = document.getElementById("sideBar");
		sideStripElement = document.getElementById("sideStrip");
		mainBodyElement = document.getElementById("mainBody");
		if (sideBarElement.style.display != "none") {
			sideBarElement.style.display = "none";
			sideStripElement.style.display = "none";
			mainBodyElement.style.left = "0px";
			setCookie("drunkit_sideBar", false, 500);
		}
		else {
			sideBarElement.style.display = "";
			sideStripElement.style.display = "";
			mainBodyElement.style.left = "130px";
			setCookie("drunkit_sideBar", true, 500);
		}
	}
}

function setCookie (cookieName, cookieValue, nDays) {
	var today = new Date();
	var expire = new Date();
	if ((nDays == null) || (nDays == 0)) {
		nDays=1;
	}
	expire.setTime(today.getTime() + 3600000*24*nDays);
	document.cookie = cookieName+"="+escape(cookieValue) + ";expires="+expire.toGMTString();
}

function getCookie (cookieName) {
	if(document.cookie) {
		var index = document.cookie.indexOf(cookieName);
		if (index != -1) {
			var countbegin = (document.cookie.indexOf(cookieName+"=", index) + 1);
			var countend = document.cookie.indexOf(";", index);
			if (countend == -1) {
				countend = document.cookie.length;
			}
			return document.cookie.substring(countbegin + cookieName.length, countend);
		}
	}
	return null;
}

function checkSideBar () {
	if (getCookie("drunkit_sideBar") == "false") {
		toggleSideBar();
	}
}