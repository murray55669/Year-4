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

var currentSlide = 0;
var currentPage = 0;

var slideImages = [];

var packageName;

var slides = [];

var navList;
var pageList;
var textWrap;

var textButton;
var navButton;
var pageButton;

var labels = [];

var data;

var storageDir; 

var packLoaded = document.createEvent('Event');
packLoaded.initEvent('pack_loaded', true, true)
document.addEventListener('pack_loaded', generateContent, false);

var imageLoaded = document.createEvent('Event');
imageLoaded.initEvent('image_loaded', true, true)

document.addEventListener('deviceready', onDeviceReady, false);  
function onDeviceReady() { 
	storageDir = cordova.file.externalApplicationStorageDirectory || cordova.file.dataDirectory;
	
	pageInit();
}

function readJSONFromFile(fileName) {
	console.log('attempting a JSON read');
	var pathToFile = storageDir + fileName;
	window.resolveLocalFileSystemURL(pathToFile, function (fileEntry) {
		fileEntry.file(function (file) {
			var reader = new FileReader();

			reader.onloadend = function (e) {
				data = JSON.parse(this.result);
				document.dispatchEvent(packLoaded);
			};

			reader.readAsText(file);
		}, errorHandler.bind(null, fileName));
	}, errorHandler.bind(null, fileName));
}

function navClickFunction(slideId) {
    return function(event) {
		event.stopPropagation();
        goToSlide(slideId);
    };
}
function pageClickFunction(pageId) {
	return function(event) {
		event.stopPropagation();
        goToPage(pageId);
    };
}

function saveState() {
	localStorage.setItem("currentPage", currentPage);
	localStorage.setItem("currentSlide", currentSlide);
}
function loadState() {
	var cp = parseInt(localStorage.getItem("currentPage"));
	if (cp >= 0 && cp < data.pages.length) {
		goToPage(parseInt(cp));
	}
	else {
		goToPage(0);
	}
}

function goToPage(id) {
    //takes the id of a page and refreshes the app view to match
	if (id < 0) {
        id = 0;
    } else if (id >= data.pages.length) {
        id = data.pages.length-1;
    }
	
	currentPage = id;
	
	var title = document.getElementById('page_title');
	title.innerHTML = data.pages[currentPage].title;
	
	slides = data.pages[currentPage].slides;

    var imgRoot = document.getElementById('images_wrapper');
    var navRoot = document.getElementById('nav_list');
	
	//reset page
	slideImages = []
	while (imgRoot.firstChild) {	
		imgRoot.removeChild(imgRoot.firstChild);
	}
	imgRoot.innerHTML = '';
	while (navRoot.firstChild) {
		navRoot.removeChild(navRoot.firstChild);
	}
	navRoot.innerHTML = '';
	
	var imageIDTracker = 0;
	var fileNameTracker = packageName+'.image.'+currentPage+'.0';
	
	function readImageFromFile() {
		console.log('Loading image: '+fileNameTracker);
		//Images
        slideImg = document.createElement('img');
		slideImg.id = 'image_'+imageIDTracker;
        if (first) {
            first = false;
            slideImg.className = 'base_layer';
        } else {
            slideImg.className = 'layer';
        }
        slideImages.push(slideImg);
        imgRoot.appendChild(slideImg);
        //Nav menu (order reversed, so menu arranged with base layer button closest to control bar)
        navEntry = document.createElement('div');
        navEntry.className = 'slide_list_entry noselect';
        navEntry.innerHTML = ((slides.length-1)-imageIDTracker)+1;
        navEntry.onclick = navClickFunction((slides.length-1)-imageIDTracker);
        navRoot.appendChild(navEntry);
		
		var pathToFile = storageDir + fileNameTracker;
		window.resolveLocalFileSystemURL(pathToFile, function (fileEntry) {
			fileEntry.file(function (file) {
				var reader = new FileReader();

				reader.onloadend = function (e) {
					document.getElementById('image_'+imageIDTracker).src = this.result;
					imageIDTracker++;
					fileNameTracker = packageName+'.image.'+currentPage+'.'+imageIDTracker;
					
					if (imageIDTracker < slides.length) {
						document.dispatchEvent(imageLoaded);
					} else {
						document.removeEventListener('image_loaded', readImageFromFile);
						
						var clearDiv = document.createElement('div')
						clearDiv.className = 'clear'
						imgRoot.appendChild(clearDiv)

						goToSlide(0);
					}
				};

				reader.readAsText(file);
			}, errorHandler.bind(null, fileNameTracker));
		}, errorHandler.bind(null, fileNameTracker));
	}
	
    var first = true; 
    
    var slideImg;
    var navEntry;
    
	document.addEventListener('image_loaded', readImageFromFile, false);
	
	readImageFromFile()
}

function nextSlide() {
    goToSlide(currentSlide+1);
}
function previousSlide() {
    goToSlide(currentSlide-1);
}
function goToSlide(value) {	
    if (value < 0) {
        value = 0;
    } else if (value >= slides.length) {
        value = slides.length-1;
    }
	
	cleanScreen();
	window.scrollTo(0, 0);
	currentSlide = value;
	saveState();
	
	for (var i = 0; i < slides.length; i++) {
		if (i <= currentSlide) {
			slideImages[i].style.display = '';
		} else {
			slideImages[i].style.display = 'none';
		}
		if (i == currentSlide) {
			//Display labels
			for (var j = 0; j < slides[i].labels.length; j++) {
				
				addLabel(slides[i].labels[j]);
			}
		}
	}
	
	var enabled = 'button noselect bold';
	var disabled = 'button noselect bold disabled';
	
	if (slides.len == 1) {
		navButton.className = disabled;
	}
	
	if (slides[currentSlide].text == '') {
		textButton.className = disabled; 
	} else {
		textButton.className = enabled;
	}
	
	navButton.innerHTML = "Layer<br>("+(currentSlide+1)+"/"+slides.length+")"
	
	resizeWidth();
}


function toggleDisplay(element) {
	if (element.style.display == '') {
		element.style.display = 'none';
	} else {
		element.style.display = '';
	}
}
function hideDisplay(element) {
	element.style.display = 'none';
}
function showDisplay(element) {
	element.style.display = '';
}
function toggleHighlightButton(element) {
    if (element.style.background == '') {
		element.style.background = '#d0d0d0';
	} else {
		element.style.background = '';
	}
}
function highlightButton(element) {
    element.style.background = '#d0d0d0;'
}
function lowlightButton(element) {
    element.style.background = '';
}

function toggleSlidesList() {
	toggleDisplay(navList);
	hideDisplay(pageList);
	hideDisplay(textWrap);
    
    lowlightButton(textButton);
    toggleHighlightButton(navButton);
    lowlightButton(pageButton);
	
	if (navList.style.display == '') {
		var entries = document.getElementsByClassName('slide_list_entry');
		for (var i = 0; i < entries.length; i++) {
			entries[i].className = 'slide_list_entry noselect';
		}
		entries[(slides.length-1)-currentSlide].className = 'slide_list_entry noselect slide_list_entry_selected';
	}
}
function togglePagesList() {	
	toggleDisplay(pageList);
	hideDisplay(navList);
	hideDisplay(textWrap);
	
    lowlightButton(textButton);
    lowlightButton(navButton);
    toggleHighlightButton(pageButton);
    
	if (pageList.style.display == '') {
		var entries = document.getElementsByClassName('page_list_entry');
		for (var i = 0; i < entries.length; i++) {
			if (entries[i].id == currentPage) {
				entries[i].className = 'page_list_entry noselect page_list_entry_selected';
			} else {
				entries[i].className = 'page_list_entry noselect';	
			}
		}
	}
}
function toggleText() {
    if (slides[currentSlide].text != "") {		
		toggleDisplay(textWrap);
		hideDisplay(navList);
		hideDisplay(pageList);
        
        toggleHighlightButton(textButton);
        lowlightButton(navButton);
        lowlightButton(pageButton);
		
		if (textWrap.style.display == '') {
			var text = document.getElementById('text');
			var breaks = slides[currentSlide].text.replace(/\n/g, "<br>");
            text.innerHTML = breaks;
		}
    }
}
function toggleLabels() {
    alert("toggling labels");
    for (var i = 0; i < labels.length; i++) {
        if (labels[i].style.display == '') {
            labels[i].style.display = 'none'
        } else {
            labels[i].style.display = ''
        }
    }
}

function addLabel(labelData) {
	var xPos = labelData.xPos;
	var yPos = labelData.yPos;
	var text = labelData.text;
	var flipped = false;
	if (labelData.flipped === true) {
		flipped = true;
	}
	
    //xPos, yPos should be percentages
    if ((xPos < 50 && flipped === false) || (xPos >= 50 && flipped === true)) {
        var label = document.createElement("div");
        label.className = "label";
        label.style.top = labelTopOffset(yPos)+"%";
        label.style.left = xPos+"%";
        label.style.maxWidth = (100-xPos)+"%";
        
        var label_marker = document.createElement("div");
        label_marker.className = "label_marker llabel_marker";
        var label_dot = document.createElement("div");
        label_dot.className = "label_dot llabel_dot";
        var label_line = document.createElement("div");
        label_line.className = "label_line llabel_line";
        label_marker.appendChild(label_dot);
        label_marker.appendChild(label_line);
        
        var label_text = document.createElement("div");
        label_text.className = "label_text llabel_text";
        label_text.innerHTML = text;
        
        label.appendChild(label_marker);
        label.appendChild(label_text);
    } else {
        var label = document.createElement("div");
        label.className = "label";
        label.style.top = labelTopOffset(yPos)+"%";
        label.style.right = (100-xPos)+"%";
        label.style.maxWidth = xPos+"%";
        
        var label_marker = document.createElement("div");
        label_marker.className = "label_marker rlabel_marker";
        var label_dot = document.createElement("div");
        label_dot.className = "label_dot rlabel_dot";
        var label_line = document.createElement("div");
        label_line.className = "label_line rlabel_line";
        label_marker.appendChild(label_dot);
        label_marker.appendChild(label_line);
        
        var label_text = document.createElement("div");
        label_text.className = "label_text rlabel_text";
        label_text.innerHTML = text;
        
        label.appendChild(label_marker);
        label.appendChild(label_text);
    }
    labels.push(label)
    document.getElementById('images_wrapper').appendChild(label);
}
function labelTopOffset(pct) {
	var imageWrapper = document.getElementById('images_wrapper');
	var padSize = 50;
	var wrapSize = imageWrapper.scrollHeight;
	var retPct = (pct * (wrapSize - padSize)) / wrapSize;
	return retPct;
}
function removeLabels() {
    var activeLabels = document.getElementsByClassName('label');
    for (var i = activeLabels.length-1; i >= 0; i--) {
        activeLabels[i].parentNode.removeChild(activeLabels[i]);
    }
}
function cleanScreen() {
    removeLabels();
    hideOverlays();
}
function hideOverlays() {
	hideDisplay(textWrap);
	hideDisplay(navList);
	hideDisplay(pageList);
    
    lowlightButton(textButton);
    lowlightButton(navButton);
    lowlightButton(pageButton);
}
function hideTutorial() {
	localStorage.setItem("skipTutorial", 1)
	document.getElementById('tutorial_splash').style.display = 'none';
}
function resizeWidth() {
	var lMarkers = document.getElementsByClassName('label_marker');
	var lDots = document.getElementsByClassName('label_dot');
	var lLines = document.getElementsByClassName('label_line');
	var lLLines = document.getElementsByClassName('llabel_line');
	var rLLines = document.getElementsByClassName('rlabel_line');
	var lText = document.getElementsByClassName('label_text');
	
	for (var i = 0; i < lMarkers.length; i++) {
		lMarkers[i].style.height = vw(0.5);
	}
	for (var i = 0; i < lDots.length; i++) {
		lDots[i].style.height = vw(1);
		lDots[i].style.width = vw(1);
	}
	for (var i = 0; i < lLines.length; i++) {
		lLines[i].style.height = vw(0.5);
		lLines[i].style.marginLeft = vw(0.25);
		lLines[i].style.marginRight = vw(0.25);
	}
	for (var i = 0; i < lLLines.length; i++) {
		lLLines[i].style.marginLeft = vw(0.5);
	}
	for (var i = 0; i < rLLines.length; i++) {
		rLLines[i].style.marginRight = vw(0.5);
	}
	for (var i = 0; i < lText.length; i++) {
		lText[i].style.fontSize = vw(4);
	}
	for (var i = 0; i < lMarkers.length; i++) {
		var target_width = lMarkers[i].offsetWidth;
		var dot = lMarkers[i].getElementsByClassName('label_dot')[0]
		var line = lMarkers[i].getElementsByClassName('label_line')[0]
		line.style.width = (target_width - (dot.offsetWidth*3))+"px";
	}
}
function vw(val) {
	return ((window.innerWidth*val)/100)+'px';
}	
function filterPageList(term) {
	var page_items = document.getElementsByClassName('page_list_entry');
	for (var i = 0; i < page_items.length; i++) {
		if (page_items[i].innerHTML.toLowerCase().indexOf(term.toLowerCase()) == -1) {
			page_items[i].style.display = 'none';
		} else {
			page_items[i].style.display = '';
		}
	}
}
function pageInit() {	
	var skipTutorial = parseInt(localStorage.getItem("skipTutorial"))
	if (skipTutorial === 1) {
		hideTutorial();
	}
	var loaded = parseInt(localStorage.getItem("packageLoaded"))
	var downloadSplash = document.getElementById('download_splash');
	downloadSplash.style.display = 'none';
	if (loaded === 1) {
		packageName = localStorage.getItem("currentPackage");
		readJSONFromFile(packageName+'.json')
	} else {
		downloadSplash.style.display = '';
		document.getElementById('loading_splash').style.display = 'none';
	}
}
function generateContent() {
	document.getElementById('loading_splash').style.display = 'none';
	
	//setup page list 
	var pageRoot = document.getElementById('page_list');
	
	for (var i = 0; i < data.pages.length; i++) {
		pageEntry = document.createElement('div');
		pageEntry.id = i;
		pageEntry.className = 'page_list_entry noselect';
		pageEntry.innerHTML = data.pages[i].title;
		pageEntry.onclick = pageClickFunction(i);
		pageRoot.appendChild(pageEntry);
	}
	
	navList = document.getElementById('nav_list');
	pageList = document.getElementById('page_list');
	textWrap = document.getElementById('text_wrap');
    
    textButton = document.getElementById('text_button');
    navButton = document.getElementById('nav_button');
    pageButton = document.getElementById('page_button');

	loadState();
}