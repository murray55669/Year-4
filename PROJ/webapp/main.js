var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
var height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

var currentSlide = 0;

var slideImages = [];
var data = [];

function slideObj (id, image, title, text, labels) {
    this.id = id;
    this.image = image;
    this.title = title;
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
function generate(slides) {
    data = slides
    
    var imgRoot = document.getElementById('images_wrapper');
    var navRoot = document.getElementById('nav_list');
    var first = true; 
    
    var slideImg;
    var navEntry;
    
    for (var i = 0; i < data.length; i++) {
        slideImg = document.createElement('img');
        slideImg.src = data[i].image;
        
        if (first) {
            first = false;
            slideImg.className = 'base_layer';
        } else {
            slideImg.className = 'layer';
        }
        
        slideImages.push(slideImg);
        imgRoot.appendChild(slideImg);
        
        navEntry = document.createElement('div');
        navEntry.className = 'slide_list_entry noselect';
        navEntry.innerHTML = data[i].id;
        navEntry.onclick = navClickFunction(data[i].id);
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
    var prevButton = document.getElementById('prev_button');
    var navButton = document.getElementById('nav_button');
    var nextButton = document.getElementById('next_button');
    var textButton = document.getElementById('text_button');
    
    var enabled = 'button noselect bold';
    var disabled = 'button noselect bold disabled';
    if (currentSlide == 0) {
        prevButton.className = disabled;
        nextButton.className = enabled;
    } else if (currentSlide == data.length-1) {
        prevButton.className = enabled;
        nextButton.className = disabled;
    } else {
        prevButton.className = enabled;
        nextButton.className = enabled;
    }
    
    if (data.len == 1) {
        navButton.className = disabled;
    }
    
    if (data[currentSlide].text == '') {
        textButton.className = disabled; 
    } else {
        textButton.className = enabled;
    }
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
            document.getElementById('title').innerHTML = data[currentSlide].title;
            document.getElementById('text').innerHTML = data[currentSlide].text;
        }
    }
}
function addLabel(xPos, yPos, text) {
    //xPos, yPos should be precentages
    if (xPos < 50) {
        var label = document.createElement("div");
        label.className = "label";
        label.style = "top:"+yPos+"%; left:"+xPos+"%; max-width: "+(100-xPos)+"%;";
        
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
        label.style = "top:"+yPos+"%; right:"+(100-xPos)+"%; max-width: "+xPos+"%;";
        
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
function pageInit() {
    generate(exampleContent);
    goToSlide(0);
}