function closetag() {
        
    var x = document.getElementById("welcome-tagline");

    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
} 

function switchhowitworksCustomer() {
    var a = document.getElementById("traveller-pov");
    var b = document.getElementById("customer-pov");
    var c = document.getElementById("hww1");
    var d = document.getElementById("hww2");

    a.style.display = "none";
    b.style.display = "block";
    c.style.color = "white";
    c.style.backgroundColor = "#F76C6C";
    d.style.color = "#F76C6C";
    d.style.backgroundColor = "white";
    

}

function switchhowitworksTraveller() {
    var a = document.getElementById("traveller-pov");
    var b = document.getElementById("customer-pov");
    var c = document.getElementById("hww1");
    var d = document.getElementById("hww2");

    a.style.display = "block";
    b.style.display = "none";
    c.style.color = "#F76C6C";
    c.style.backgroundColor = "white";
    d.style.color = "white";
    d.style.backgroundColor = "#F76C6C";
}

window.smoothScroll = function(target) {
    var scrollContainer = target;
    do { 
        scrollContainer = scrollContainer.parentNode;
        if (!scrollContainer) return;
        scrollContainer.scrollTop += 1;
    } while (scrollContainer.scrollTop == 0);

    var targetY = 0;
    do {
        if (target == scrollContainer) break;
        targetY += target.offsetTop;
    } while (target = target.offsetParent);

    scroll = function(c, a, b, i) {
        i++; if (i > 30) return;
        c.scrollTop = a + (b - a) / 30 * i;
        setTimeout(function(){ scroll(c, a, b, i); }, 20);
    }
    
    scroll(scrollContainer, scrollContainer.scrollTop, targetY, 0);
}
