function memberOf(string, list) {
	if (list.indexOf(string) >= 0) {
		return true;
	}
	return false;
}

function getString(array) {
	var newString = '';
	for (var i = 0; i < array.length; i++) {
		newString = newString + array[i] + ';';
	}
	return newString;
}

function getArray(string) {
	try {
		var ret = string.split(';');
		ret.pop()
		return ret;
	} catch (e) {
		return [];
	}
}

function getInstalled() {
	return getArray(localStorage.getItem("installedPackages"));
}

function checkAndAddPack(name) {
	var currentArray = getArray(localStorage.getItem("installedPackages"));
	
	if (!memberOf(name, currentArray)) {
		currentArray.push(name);
		localStorage.setItem("installedPackages", getString(currentArray));
	}
}

function checkAndRemovePack(name) {
	var currentArray = getArray(localStorage.getItem("installedPackages"));
	
	if (memberOf(name, currentArray)) {
		var newArray = [];
		
		for (var i = 0; i < currentArray.length; i++) {
			if (!(currentArray[i] == name)) {
				newArray.push(currentArray[i])
			}
		}
		localStorage.setItem("installedPackages", getString(newArray));
	}
}