var repo = "http://bliss.dtdns.net/proj/repo/"	
	
var storageDir = cordova.file.externalApplicationStorageDirectory || cordova.file.dataDirectory;

var message;

var errorHandler = function (fileName, e) {  
	var msg = '';

	switch (e.code) {
		case FileError.QUOTA_EXCEEDED_ERR:
			msg = 'Storage quota exceeded';
			break;
		case FileError.NOT_FOUND_ERR:
			msg = 'File not found';
			break;
		case FileError.SECURITY_ERR:
			msg = 'Security error';
			break;
		case FileError.INVALID_MODIFICATION_ERR:
			msg = 'Invalid modification';
			break;
		case FileError.INVALID_STATE_ERR:
			msg = 'Invalid state';
			break;
		default:
			msg = 'Unknown error';
			break;
	};

	console.log('Error '+e.code+' (' + fileName + '): ' + msg);
}

function listClickFunction(name) {
	return function(event) {
		event.stopPropagation();
		loadPackage(name);
	};
}


function init() {
	var packages = loadJSON(repo+'packages.json');

	// generate package list
	var list = document.getElementById('package_list');
	for (var i = 0; i < packages.names.length; i++) {
		var entry = document.createElement("div");
		entry.id = 'package_list_entry_'+i;
		entry.className = 'package_list_entry';
		entry.innerHTML = packages.names[i];
		entry.onclick = listClickFunction(packages.names[i]);
		list.appendChild(entry);
	}
	message.innerHTML = '';
}

var fetchedJSON;

var pack;
var target;
var page;
var slide;

var completed;

var imgWritten = document.createEvent('Event');
imgWritten.initEvent('image_written', true, true)
document.addEventListener('image_written', imageSave, false);
var packDownloaded = document.createEvent('Event');
packDownloaded.initEvent('package_downloaded', true, true)
document.addEventListener('package_downloaded', packDone, false);

function loadPackage(name) {	
	
	pack = name;
	target = repo+name+'/';
	slide = 0;
	page = 0;
	
	completed = 0;
	
	fetchedJSON = loadJSON(target+'data.json');
	console.log('Pages to write: '+fetchedJSON.pages.length);
	writeToFileJSON(name+'.json', fetchedJSON);
	
	var total = 0;
	for (var i = 0; i < fetchedJSON.pages.length; i++) {
		for (var j = 0; j < fetchedJSON.pages[i].slides.length; j++) {
			total++;
		}
	}
	
	message.innerHTML = 'Downloading...';
	document.getElementById('complete').innerHTML = completed;
	document.getElementById('slash').innerHTML = '/';
	document.getElementById('toComplete').innerHTML = total;
	

	
	imageSave();
	
}

function imageSave() {
	loadImage(target+page+'/'+slide+'.png', function(data){
		writeToFileImage(pack+'.image.'+page+'.'+slide, data);
	});
}
function packDone() {
	localStorage.setItem("currentPackage", pack);
	localStorage.setItem("packageLoaded", 1);
	localStorage.setItem(pack, 1);
	localStorage.setItem("currentPage", -1);
	localStorage.setItem("currentSlide", -1);
	message.innerHTML = 'Download complete.';
}

	
function loadImage(url, callback){
	var img = new Image();
	img.crossOrigin = 'Anonymous';
	img.onload = function(){
		var canvas = document.createElement('CANVAS');
		var ctx = canvas.getContext('2d');
		var dataURL;
		canvas.height = this.height;
		canvas.width = this.width;
		ctx.drawImage(this, 0, 0);
		dataURL = canvas.toDataURL('image/png');
		callback(dataURL);
		canvas = null; 
	};
	img.src = url;
}


function readJSONFromFile(fileName) {
	console.log('attempting a JSON read');
	var pathToFile = storageDir + fileName;
	window.resolveLocalFileSystemURL(pathToFile, function (fileEntry) {
		fileEntry.file(function (file) {
			var reader = new FileReader();

			reader.onloadend = function (e) {
				message.innerHTML = this.result;
			};

			reader.readAsText(file);
		}, errorHandler.bind(null, fileName));
	}, errorHandler.bind(null, fileName));
}

	
function loadJSON(target) {
	var data;

	var xobj = new XMLHttpRequest();
		xobj.overrideMimeType("application/json");
	xobj.open('GET', target, false); 
	xobj.onreadystatechange = function () {
		  if (xobj.readyState == 4 && xobj.status == "200") {
			data = JSON.parse(xobj.responseText);
		  }
	};
	xobj.send(null);  
	
	return data;
 }

function readImageFromFile(fileName) {
	console.log('attempting an image read');
	var pathToFile = storageDir + fileName;
	console.log(pathToFile);
	window.resolveLocalFileSystemURL(pathToFile, function (fileEntry) {
		fileEntry.file(function (file) {
			var reader = new FileReader();

			reader.onloadend = function (e) {
				console.log("image read was:"+this.result)
				document.getElementById('image').src = this.result;
			};

			reader.readAsText(file);
		}, errorHandler.bind(null, fileName));
	}, errorHandler.bind(null, fileName));
}

function incCompleted() {
	completed++
	document.getElementById('complete').innerHTML = completed;
}

function writeToFileImage(fileName, data) {
	console.log('attempting an image write to '+fileName);
	window.resolveLocalFileSystemURL(storageDir, 
	
	function (directoryEntry) {
		directoryEntry.getFile(fileName, { create: true }, function (fileEntry) {
			fileEntry.createWriter(function (fileWriter) {
				fileWriter.onwriteend = function (e) {
					console.log('Write of file ' + fileName + ' completed.');
					if (slide+1 < fetchedJSON.pages[page].slides.length) {
						slide++;
						incCompleted();
						document.dispatchEvent(imgWritten);
					} else if (page+1 < fetchedJSON.pages.length) {
						page++;
						slide = 0;
						incCompleted();
						document.dispatchEvent(imgWritten);
					} else {
						incCompleted();
						document.dispatchEvent(packDownloaded);
					}
					
				};

				fileWriter.onerror = function (e) {
					console.log('Write failed: ' + e.toString());
				};
				try {
					var blob = new Blob([data], { type: 'image/png' });
				} catch(err) {
					try {
						var bBuilder = new BlobBuilder();
					} catch (err2) {
						var bBuilder = new WebKitBlobBuilder();

					}
					bBuilder.append(data);
					var blob = bBuilder.getBlob('image/png');
				}
				fileWriter.write(blob);
			}, errorHandler.bind(null, fileName));
		}, errorHandler.bind(null, fileName));
	}, 
	
	errorHandler.bind(null, fileName));
}

function writeToFileJSON(fileName, data) {
	console.log('attempting a JSON write');
	data = JSON.stringify(data, null, '\t');
	window.resolveLocalFileSystemURL(storageDir, 
	
	function (directoryEntry) {
		directoryEntry.getFile(fileName, { create: true }, function (fileEntry) {
			fileEntry.createWriter(function (fileWriter) {
				fileWriter.onwriteend = function (e) {
					console.log('Write of file "' + fileName + '"" completed.');
				};

				fileWriter.onerror = function (e) {
					console.log('Write failed: ' + e.toString());
				};
				try {
					var blob = new Blob([data], { type: 'text/plain' });
				} catch(err) {
					try {
						var bBuilder = new BlobBuilder();
						bBuilder.append(data);
						var blob = bBuilder.getBlob('text/plain');
					} catch (err2) {
						var bBuilder = new WebKitBlobBuilder();
						bBuilder.append(data);
						var blob = bBuilder.getBlob('text/plain');
					}
				}
				fileWriter.write(blob);
			}, errorHandler.bind(null, fileName));
		}, errorHandler.bind(null, fileName));
	}, 
	
	errorHandler.bind(null, fileName));
}

document.addEventListener('deviceready', onDeviceReady, false);  
function onDeviceReady() {  
	message = document.getElementById('message');
	init();
}
	