function openConfirmBox(){
  var reserveBtn = document.getElementById("reserve-btn");
  var confirmBox = document.getElementById("confirm-box");
  reserveBtn.addEventListener("click", function(){
      confirmBox.style.display = 'block';
  }, false);

}

function closeConfirmBox(){
  var closeConfirmBtn = document.getElementById("close-confirm-btn");
  var confirmBox = document.getElementById("confirm-box");
  closeConfirmBtn.addEventListener("click", function(){
      confirmBox.style.display = 'none';
  }, false);

}



openConfirmBox();
closeConfirmBox();
