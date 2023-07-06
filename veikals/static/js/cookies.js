// prece count element
$(function() {
  // Assuming you have a cookie named 'Prece_Count'
  var cookieValue = getCookie('Prece_Count');
  if (cookieValue > 0) {
      // create product count element
      $("<span>")
          .text(cookieValue)
          .addClass("product-count")
          .appendTo("#grozs");
  }
});



// Function to set a cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
  }
  
  // Function to get the value of a cookie
  function getCookie(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      while (cookie.charAt(0) === ' ') {
        cookie = cookie.substring(1, cookie.length);
      }
      if (cookie.indexOf(nameEQ) === 0) {
        return cookie.substring(nameEQ.length, cookie.length);
      }
    }
    return null;
  }
  
  // Function to delete a cookie
  function deleteCookie(name) {
    setCookie(name, "", -1);
  }