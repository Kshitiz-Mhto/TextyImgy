var scrollDownButton = document.getElementById("headerButton");

scrollDownButton.addEventListener("click", function() {
    var scrollPosition = 890; 
    window.scrollTo({
      top: scrollPosition,
      behavior: "smooth"});
});