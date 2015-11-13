var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
var height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

var currentSlide = 1;

/*
var slides = ["image_0", "image_1", "image_2"];
var images = ["cat0.png", "cat1.png", "cat2.png"];
var titles = ["Title 1", "Title 2", "Title 3"];
var texts = ["Slide text 1.", "", "Slide text 3."];
var labels = [[[10, 10, "L1S1"], [10, 20, 'L2S1']], [[10, 10, "L1S2"], [10, 20, 'L2S2']], [[10, 10, "L1S3"], [10, 20, 'L2S3']]];
*/

var slideImages = [];
var data = [];

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
        
        //TODO: broken af
        navEntry = document.createElement('div');
        navEntry.className = 'slide_list_entry noselect';
        navEntry.innterHTML = i+1;
        navEntry.onclick = function(){ goToSlide(i+1); };
        navRoot.appendChild(navEntry);
    }
}
function nextSlide() {
    goToSlide(currentSlide+1);
}
function previousSlide() {
    goToSlide(currentSlide-1);
}
function goToSlide(value) {
    cleanScreen();
    if (value < 1) {
        value = 1;
    } else if (value > data.length) {
        value = data.length;
    }
    currentSlide = value;
    for (var i = 1; i < data.length; i++) {
        if (i < currentSlide) {
            slideImages[i].style.display = '';
        } else {
            slideImages[i].style.display = 'none';
        }
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
    if (data[currentSlide-1].text != "") {
        if (document.getElementById('text_wrap').style.display == '') {
            document.getElementById('text_wrap').style.display = 'none'
        } else {
            document.getElementById('text_wrap').style.display = ''
            document.getElementById('title').innerHTML = data[currentSlide-1].title;
            document.getElementById('text').innerHTML = data[currentSlide-1].text;
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
    document.getElementById('text_wrap').style.display = 'none';
    for (var i = 1; i < slideImages.length; i++) {
        slideImages[i].style.display = 'none';
    }
    toggleSlidesList();
}