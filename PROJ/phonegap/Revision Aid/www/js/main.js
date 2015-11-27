var windowWidth = window.innerWidth
var windowHeight = window.innerHeight

var currentSlide = 0;
var currentPage = "";

var slideImages = [];
var data = [];

/*
	TODO:
	-be able to load full packages as opposed to pages
*/

function pageObj (title, slides) {
	this.title = title;
	this.slides = slides;
}
function slideObj (text, labels) {
    this.text = text;
    this.labels = labels;
}
function labelObj (xPos, yPos, text) {
    this.xPos = xPos;
    this.yPos = yPos;
    this.text = text;
}
function navClickFunction(slideId) {
    return function() {
        goToSlide(slideId);
    };
}
function generate(p, id) {
    //takes a page object and it's id in the list generates the app content
	data = p.slides;
	currentPage = id;
	
    var imgRoot = document.getElementById('images_wrapper');
    var navRoot = document.getElementById('nav_list');
    var first = true; 
    
    var slideImg;
    var navEntry;
    
    for (var i = 0; i < data.length; i++) {
        //Images
        slideImg = document.createElement('img');
		// img/0/0.png for slide 0 of page 0
        slideImg.src = 'img/'+id+'/'+i+'.png';
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
        navEntry.innerHTML = (data.length-1)-i;
        navEntry.onclick = navClickFunction((data.length-1)-i);
        navRoot.appendChild(navEntry);
    }
    
    var clearDiv = document.createElement('div')
    clearDiv.className = 'clear'
    imgRoot.appendChild(clearDiv)
}
function nextSlide() {
    goToSlide(currentSlide+1);
}
function previousSlide() {
    goToSlide(currentSlide-1);
}
function goToSlide(value) {
    cleanScreen();
    if (value < 0) {
        value = 0;
    } else if (value >= data.length) {
        value = data.length-1;
    }
    currentSlide = value;
    for (var i = 0; i < data.length; i++) {
        if (i <= currentSlide) {
            slideImages[i].style.display = '';
        } else {
            slideImages[i].style.display = 'none';
        }
        if (i == currentSlide) {
            //Add labels
            for (var j = 0; j < data[i].labels.length; j++) {
                addLabel(data[i].labels[j].xPos, data[i].labels[j].yPos, data[i].labels[j].text);
            }
        }
    }
    var navButton = document.getElementById('nav_button');
    var textButton = document.getElementById('text_button');
    
    var enabled = 'button noselect bold';
    var disabled = 'button noselect bold disabled';
    
    if (data.len == 1) {
        navButton.className = disabled;
    }
    
    if (data[currentSlide].text == '') {
        textButton.className = disabled; 
    } else {
        textButton.className = enabled;
    }
	resizeWidth();
	localStorage.setItem("currentSlide", currentSlide);
}
function toggleSlidesList() {
    if (document.getElementById('nav_list').style.display == '') {
        document.getElementById('nav_list').style.display = 'none'
    } else {
        document.getElementById('nav_list').style.display = ''
    }
}
function toggleText() {
    //Toggles text box overlay on slide on and off.
    if (data[currentSlide].text != "") {
        if (document.getElementById('text_wrap').style.display == '') {
            document.getElementById('text_wrap').style.display = 'none'
        } else {
            document.getElementById('text_wrap').style.display = ''
			//todo: pull title from page
            document.getElementById('title').innerHTML = data[currentSlide].title;
            document.getElementById('text').innerHTML = data[currentSlide].text;
        }
    }
}
function togglePagesList() {
	//TODO
}
function goToPage(value) {
	//TODO
	//save state to local storage
	localStorage.setItem("currentPage", currentPage);
}
function selectPackage(input) {
	//TODO
	/*
	-allow user to browse for ZIP file
	
	-AJAX the zip file to some page where we can...
	-unpack ZIP
	-check if zip contains valid layout file - if not, throw an alert and return
	
	-get size of unpacked content
	-request that size plus 1MB as storage quota
	-save the contents of the zip file to persistent storage
	-save a web variable 
	
	*/
	if (input) {
		alert(input.value);
		localStorage.setItem("packageDir", "something");
	}
}
function addLabel(xPos, yPos, text) {
    //xPos, yPos should be precentages
    if (xPos < 50) {
        var label = document.createElement("div");
        label.className = "label";
        label.style.top = yPos+"%";
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
        label.style.top = yPos+"%";
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
    document.getElementById("images_wrapper").appendChild(label);
}
function addLabelClick(clickEvent, text) {
    var xPos = clickEvent.clientX;
    var yPos = clickEvent.clientY;
    var height = document.getElementById('images_wrapper').clientHeight;
    var width = document.getElementById('images_wrapper').clientWidth;
    
    addLabel((xPos/width)*100, ((yPos)/height)*100, text);
}
function removeLabels() {
    var activeLabels = document.getElementsByClassName('label');
    for (var i = activeLabels.length-1; i >= 0; i--) {
        activeLabels[i].parentNode.removeChild(activeLabels[i]);
    }
}
function cleanScreen() {
    removeLabels();
    document.getElementById('text_wrap').style.display = 'none';
    document.getElementById('nav_list').style.display = 'none';
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
}
function vw(val) {
	return ((windowWidth*val)/100)+'px';
}	
function pageInit() {
	//TODO: use HTML5 storage to store a package to be loaded - if none exists, ask user to select one?
	generate(testPage);
	
	var cp = localStorage.getItem("currentPage");
	if (cp) {
		goToPage(parseInt(cp));
	}
	else {
		goToPage(0);
	}
	
	var cs = localStorage.getItem("currentSlide");
	if (cs) {
		goToSlide(parseInt(cs));
	}
	else {
		goToSlide(0);
	}
}