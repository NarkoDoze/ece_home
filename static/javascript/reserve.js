function openConfirmBox(){
  var reserveBtn = document.getElementById("reserve-btn");
  var confirmBox = document.getElementById("confirm-box");
  reserveBtn.addEventListener("click", function(){
      confirmBox.style.display = 'block';
  }, false);

}


openConfirmBox();
