//
// (function($) {
//     //--------------------------------------------------------------------------
//     // 사용자가 지정한 시간을 검사하고 지정 시간을 최종 결정하고 타임블록에 표시하는 함수..
//     Drupal.behaviors.searchTime = function() {
//         // 선택된 블록이 예약된 블록이면 false를 리턴하고 종료.
//         if( !Drupal.settings.studyroom_reservation.StartTimeBlock || !Drupal.settings.studyroom_reservation.EndTimeBlock ) return false;
//         if( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).hasClass( "reserved" ) ) return false;
//         if( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).hasClass( "unavailable" ) ) return false;
//
//         var start_datetime = parseInt( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime' ) );
//         var end_datetime = parseInt( $( Drupal.settings.studyroom_reservation.EndTimeBlock ).data( 'end_datetime' ) );
//
//         var reservation_limit_day_time = Drupal.settings.studyroom_reservation.reservation_limit_day_time * Drupal.settings.studyroom_hour;
//         var current_start_time = current_end_time = reservation_time = 0;
//         var last_time_block = false;
//
//         var reserved_flag = false;
//         var block = $( '#reservation_time_block td' );
//
//         var i = 0;
//         while( $( block[i] ).data( 'start_datetime' ) != start_datetime ) i++;
//
//         if( $( block[i] ).hasClass( 'reserved' ) || $( block[i] ).hasClass( 'unavailable' ) ) {
//             Drupal.settings.studyroom_reservation.StartTimeBlock = false;
//             Drupal.settings.studyroom_reservation.EndTimeBlock = false;
//             Drupal.settings.studyroom_reservation.StartSelection = false;
//             return false;
//         }
//
//         last_time_block = block[i];
//         $( block[i] ).addClass( 'selected' );
//
//         while( $( block[i] ).data( 'end_datetime' ) <= end_datetime && i < block.length ) {
//             if( $( block[i] ).data( 'end_datetime' ) < ( start_datetime + reservation_limit_day_time ) && ( !$( block[i] ).hasClass( 'reserved' ) && !$( block[i] ).hasClass( 'unavailable' ) ) ) {
//                 $( block[i] ).addClass( 'selected' );
//                 last_time_block = block[i];
//             }
//             else if( $( block[i] ).hasClass( 'reserved' ) || $( block[i] ).hasClass( 'reserved' ) ) {
//                 break;
//             }
//             i++;
//         }
//         Drupal.settings.studyroom_reservation.EndTimeBlock = block[i];
//         Drupal.settings.studyroom_reservation.EndTimeBlock = last_time_block;
//         return true;
//     };
//
//     //--------------------------------------------------------------------------
//     // 지정된 시간을 입력란에 표시하는 함수.
//     Drupal.behaviors.setTime = function() {
//         if( Drupal.behaviors.searchTime() ) {
//             $( '#start_datetime_span' ).html( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime_str' ) )
//             $( '#end_datetime_span' ).html( $( Drupal.settings.studyroom_reservation.EndTimeBlock ).data( 'end_datetime_str' ) )
//             $( '#edit-start-datetime' ).val( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime_str' ) );
//             $( '#edit-end-datetime' ).val( $( Drupal.settings.studyroom_reservation.EndTimeBlock ).data( 'end_datetime_str' ) );
//         }
//     };
//
//     //--------------------------------------------------------------------------
//     // 마우스 버튼을 눌렀을 때 처리하는 함수.
//     Drupal.behaviors.mouseDown = function() {
//         // 시간 블록이 지정된 것이 없는 경우 클릭한 시간 블록을 시작 시간과 종료 시간을 결정한다.
//         // 그리고 타임블록에서 selected 클래스를 제거하고 현재 타임블록을 선택시간으로 표시한다.
//         if( !Drupal.settings.studyroom_reservation.StartTimeBlock || !Drupal.settings.studyroom_reservation.EndTimeBlock ) {
//             Drupal.settings.studyroom_reservation.StartTimeBlock = this;
//             Drupal.settings.studyroom_reservation.EndTimeBlock = this;
//             $( '#reservation_time_block td' ).removeClass( 'selected' );
//             Drupal.behaviors.setTime();
//         }
//
//         // 초기 시간은 선택되었으나 선택 중이 아닌 경우.
//         if( !Drupal.settings.studyroom_reservation.StartSelection ) {
//             var reservation_limit_day_time = Drupal.settings.studyroom_reservation.reservation_limit_day_time * Drupal.settings.studyroom_hour;
//             var start_datetime = parseInt( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime' ) );
//             var end_datetime = parseInt( $( Drupal.settings.studyroom_reservation.EndTimeBlock ).data( 'end_datetime' ) );
//             var current_end_time = parseInt( $(this).data( 'end_datetime' ) );
//
//             // 클릭한 시간 블록이 기존 시작시간, 종료시간 안에 들어 있는 경우
//             // 클릭한 시간 블록이 기존 시작시간 이전인 경우
//             // 처음부터 다시 시간을 설정함.
//             if( current_end_time >= start_datetime && current_end_time <= end_datetime || current_end_time < start_datetime || current_end_time >= ( start_datetime + reservation_limit_day_time ) ) {
//                 Drupal.settings.studyroom_reservation.StartTimeBlock = this;
//                 Drupal.settings.studyroom_reservation.EndTimeBlock = this;
//                 $( '#reservation_time_block td' ).removeClass( 'selected' );
//                 Drupal.behaviors.setTime();
//             }
//
//             // 현재 클릭한 시간 블록이 기존 시작시간 + 하루 이용 제한시간 범위 안에 있는 경우 종료 시간만 지정한다.
//             if( current_end_time < ( start_datetime + reservation_limit_day_time ) ) {
//                 Drupal.settings.studyroom_reservation.EndTimeBlock = this;
//                 Drupal.behaviors.setTime();
//             }
//         }
//
//         Drupal.settings.studyroom_reservation.StartSelection = true;
//     };
//
//     //--------------------------------------------------------------------------
//     // 마우스 포인트가 현재 셀 위로 이동했을 때 호출되는 함수.
//     Drupal.behaviors.mouseOver = function() {
//         if( Drupal.settings.studyroom_reservation.StartSelection ) {
//             var start_datetime = parseInt( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime' ) );
//             var end_datetime = parseInt( $(this).data( 'end_datetime' ) );
//
//             if( start_datetime < end_datetime ) {
//                 Drupal.settings.studyroom_reservation.EndTimeBlock = this;
//                 Drupal.behaviors.setTime();
//             }
//         }
//     };
//
//     Drupal.behaviors.mouseUp = function() {
//         if( Drupal.settings.studyroom_reservation.StartSelection ) {
//             var start_datetime = parseInt( $( Drupal.settings.studyroom_reservation.StartTimeBlock ).data( 'start_datetime' ) );
//             var end_datetime = parseInt( $(this).data( 'end_datetime' ) );
//             if( start_datetime < end_datetime ) {
//                 Drupal.settings.studyroom_reservation.EndTimeBlock = this;
//                 Drupal.behaviors.setTime();
//                 Drupal.behaviors.reservation_user_validation();
//             }
//             Drupal.settings.studyroom_reservation.StartSelection = false;        }
//     }
//     //--------------------------------------------------------------------------
//     // 마우스 엑션을 설정하는 함수
//     Drupal.behaviors.setMouseAction = function() {
//         // 마우스 버튼을 눌렀을 때 처리하는 함수.
//         $( '#reservation_time_block td' ).mousedown( Drupal.behaviors.mouseDown );
//
//         // 마우스가 드래그된 상태로 핸재 타임블록에 위치한 경우 종료 시간을
//         $( '#reservation_time_block td' ).mouseover( Drupal.behaviors.mouseOver );
//
//         $( '#reservation_time_block td' ).mouseup( Drupal.behaviors.mouseUp );
//         $( '#reservation_time_block td' ).css({'-moz-user-select':'-moz-none',
//                                                 '-moz-user-select':'none',
//                                                 '-o-user-select':'none',
//                                                 '-khtml-user-select':'none',
//                                                 '-webkit-user-select':'none',
//                                                 '-ms-user-select':'none'
//                                             });
//     };
//
//     //--------------------------------------------------------------------------
//     // 마우스 엑션을 설정하는 함수
//     Drupal.behaviors.initTimeBlock = function() {
//         var block = $( '#reservation_time_block td' );
//         for( i = 0 ; i < block.length ; i++ ) {
//             if( $( block[i] ).data( 'start_datetime_str' ) == $( '#edit-start-datetime' ).val() ) Drupal.settings.studyroom_reservation.StartTimeBlock = block[i];
//             if( $( block[i] ).data( 'end_datetime_str' ) == $( '#edit-end-datetime' ).val() ) Drupal.settings.studyroom_reservation.EndTimeBlock = block[i];
//         }
//         Drupal.behaviors.setTime();
//     }
//
//     //--------------------------------------------------------------------------
//     // 마우스 엑션을 설정하는 함수
//     $(document).ready( function() {
//         Drupal.behaviors.initTimeBlock();
//         Drupal.behaviors.setMouseAction();
//     });
//
//     // Ajax가 호출된 후 예약 인원수를 정가시킴니다.
//     $(document).ajaxComplete( function() {
//         var user_count = 0;
//         $( '.user_name_form_field' ).each( function( index ) {
//             username = $(this).val();
//             if( username != '' ) user_count++;
//         } );
//         // 2016.11.05 아래 라인 주석처리 - 예약 FORM에서 Reserved 값 '1'로 강제 세팅 금지
//         // $( '#edit-user-reserved' ).val( user_count );
//         document.getElementById('edit-user-reserved').readOnly = true;	// 2016.11.05 추가
//         Drupal.behaviors.setMouseAction();
//     });
//
//     Drupal.behaviors.reservation_user_validation = function() {
//         var user_name = $('input[name=user_name_0]').val();
//         var user_real_name = $('input[name=user_real_name_0]').val();
//         var start_datetime = $('#edit-start-datetime').val();
//         var end_datetime = $('#edit-end-datetime').val();
//
//
//         $.ajax( {
//             url : "/services/study_rooms/owner_validation",
//             type : "POST",
//             dataType : "json",
//             data : {
//                 "user_name" : user_name,
//                 "user_real_name" : user_real_name,
//                 "start_datetime" : start_datetime,
//                 "end_datetime" : end_datetime,
//                 "place_entity_id" : Drupal.settings.studyroom_reservation.place_entity_id
//             },
//             success : function( result ) {
//                 $( "#validate_message_0" ).html( result.message );
//             },
//             error : function( xhr, ajaxOptions, thrownError ) {
//                 console.log( 'error' );
//             }
//         } );
//     }
// }(jQuery))

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

// $(document).ready(function() {
//     var timeBlock = document.getElementsByClassName("time-block");
//     var startBlock;
//     var endBlock;
//
//     $('.reserved').click(function() {
//         var num = timeBlock.indexOf(this);
//         if(this.className == "reserved"){
//             this.className = "selected time-block";
//             this.innerHTML = "<input type='hidden' name='select' value='" + this.getAttribute('name')  + "'/>";
//             // this.innerHTML = "hi";
//         }
//         else {
//             this.className = "reserved";
//             this.innerHTML = "";
//         }
//     });
// });
//


$(document).ready(function() {

    $('.reserved').click(function() {
        if(this.className == "reserved time-block"){
            var index = $(".time-block").index(this);
            var timeBlock = document.getElementsByClassName("time-block");
            var i=-2;
            var flag=0;
            while(i<3)
            {
              if(timeBlock[index+i].className == "selected time-block")
                flag=i;
              i++;
            }

            var j;
            for(j=0; j<index-2; j++)
            {
                if(timeBlock[j].className == "selected time-block")
                  timeBlock[j].className = "reserved time-block";
            }
            for(j=index+2; j<72; j++)
            {
                if(timeBlock[j].className == "selected time-block")
                  timeBlock[j].className = "reserved time-block";
            }

            while(flag>0)
            {
              timeBlock[index+flag].className = "selected time-block";
              flag--;
            }
            while(flag<0)
            {
              timeBlock[index+flag].className = "selected time-block";
              flag++;
            }
            this.className = "selected time-block";
            this.innerHTML = "<input type='hidden' name='select' value='" + this.getAttribute('name')  + "'/>";
        }
        else {
            this.className = "reserved time-block";
            this.innerHTML = "";
        }

        //background-color: #0088ff //blue #d8d8d8 : grey
    });

    $('.reserved').click(function () {
        console.log("CLICKED");
    });



});



openConfirmBox();
closeConfirmBox();
