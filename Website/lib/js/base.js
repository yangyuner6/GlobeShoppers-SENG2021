

function offerhelpfunc() {
  var x = document.getElementById("offer-help");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
 
function confirmationFunction() {
	alert("Item added!")
}
function confirmationFunction2() {
	alert("Offer made!")
}
function trips_confirmation() {
    alert("Trip added!")
}
function openForm() {
  	document.getElementById("myForm").style.display = "block";
}
function closeForm() {
  	document.getElementById("myForm").style.display = "none";
}
function openForm2() {
  	document.getElementById("myForm2").style.display = "block";
}
function closeForm2() {
  	document.getElementById("myForm2").style.display = "none";
}
function trips_confirmation() {
    alert("Trip added!")
}

function openaddPForm() {
      document.getElementById("addpro-form").style.display = "block";
  }
  function closeaddPForm() {
      document.getElementById("addpro-form").style.display = "none";
  }


  function switchhowitworks() {
        var a = document.getElementById("traveller-pov");
        var b = document.getElementById("customer-pov");
        var c = document.getElementById("hww1");
        var d = document.getElementById("hww2");

        if (a.style.display === "none") {
            a.style.display = "block";
            b.style.display = "none";
            c.style.color = "#F76C6C";
            c.style.backgroundColor = "white";
            d.style.color = "white";
            d.style.backgroundColor = "#F76C6C";
        } else {
            a.style.display = "none";
            b.style.display = "block";
            c.style.color = "white";
            c.style.backgroundColor = "#F76C6C";
            d.style.color = "#F76C6C";
            d.style.backgroundColor = "white";
        }

    }

    function showtermsandcond() {
      var win = window.open('http://127.0.0.1:5050/tandc', '_blank');
      win.focus();
    }

    function hidetermsandcond() {
      var a = document.getElementById("addpro-form");
        var b = document.getElementById("terms-and-c");

        b.style.display = "none";
        a.style.display = "block";
    }

    function confirmationFunction3() {
      if (document.getElementById("name").value === ""){
        alert("Enter the name of your product");
        return false;
      } else if (document.getElementById("prices").value === "") {
        alert("Enter the price");
        return false;
      } else if (document.getElementById("proquan").value === "") {
        alert("Select the quantity you want");
        return false;
      } else if (document.getElementById("catpro").value === "") {
        alert("Select the category for your product");
        return false;
      } else if (document.getElementById("countrypro").value === "") {
        alert("Select the country your product is in");
        return false;
      } else {
        alert("Your product has been added!");
        return true;
      }
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

