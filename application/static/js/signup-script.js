$(document).ready(function(){
  $('input[name=email]').change(function(){
    var email = $('#myemail').val();
    if($('#myemail').val().match(/^[a-zA-Z0-9\.\_]+\@[a-zA-Z0-9-]+\.(com|net|ac.kr|co.kr)$/)){
      $.ajax({
      url: '/email_check',
      type:'POST',
      data:{"email":email},
      success:function(response){
        var result = $.parseJSON(response);
        if(result['message']=="error"){
          $('#email_err').text("입력하신 이메일은 이미 사용중입니다.");
          $('#email_ok').empty(); 
        }
        else {
          $('#email_ok').text("사용 가능합니다."); 
          $('#email_err').empty(); 
        }
        console.log('success')
      },
      error: function(){
        console.log('error');
      },
      complete:function(){
        console.log('complete');
      }
      });
    }
    else {
      $('#email_err').text('이메일 주소를 정확히 입력해주세요.')
      $('#email_ok').empty();
    }
  });
  $('input[name=password]').change(function(){
    if((8 <= ($('#mypw').val()).length) & (($('#mypw').val()).length <= 20)){
      if($('#mypw').val().match(/[a-zA-Z]+/)){
        if($('#mypw').val().match(/[0-9]+/)){
          if($('#mypw').val().match(/\W+/)){
            $('#pw_ok').text('OK');
            $('#pw_err').empty();
          }
          else {
            $('#pw_err').text('비밀번호에는 특수문자가 포함되어야 합니다.');
            $('#pw_ok').empty(); 
          }
        }
        else {
          $('#pw_err').text('비밀번호에는 숫자가 포함되어야 합니다.');
          $('#pw_ok').empty();
        }
      }
      else {
        $('#pw_err').text('비밀번호에는 영어 알파벳이 포함되어야 합니다.');
        $('#pw_ok').empty();
      }
    }
    else {
      $('#pw_err').text('비밀번호 길이는 8~20자 사이어야 합니다.');
      $('#pw_ok').empty();
    }
  });
  $('input[name=password_check]').change(function(){
    if(($('#mypw').val())==($('#mypwcheck').val())){
      $('#pwcheck_ok').text('OK');
      $('#pwcheck_err').empty();	
    }
    else {
      $('#pwcheck_err').text('위에 입력하신 비밀번호와 일치하지 않습니다.');	
      $('#pwcheck_ok').empty();  
    }
  });
  $('input[name=phone]').change(function(){
    var phone = $('#myphone').val();
    if($('#myphone').val().match(/^\d{3}[\-]\d{4}[\-]\d{4}$/)){
      $.ajax({
      url: '/phone_check',
      type:'POST',
      data:{"phone":phone},
      success:function(response){
        var result = $.parseJSON(response);
        if(result['message']=="error"){
          $('#mobile_err').text("입력하신 핸드폰 번호는 이미 사용중입니다.");
          $('#mobile_ok').empty();
        }
        else {
          $('#mobile_ok').text("중복여부: 사용 가능합니다."); 
          $('#mobile_err').empty();
        }
        console.log(result['message']);
      },
      error: function(){
        console.log('error');
      },
      complete:function(){
        console.log('complete');
      }
      });
    }
    else {
      $('#mobile_err').text('000-0000-0000형태로 입력해주세요.');
      $('#mobile_ok').empty();
    }
  });
});