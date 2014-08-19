var xhr;

$(document).ready(function(){
	$('input[name=find_user]').keyup(function(){
		var username = $('#input-find-user').val();
		if (xhr) {
			xhr.abort();
		}
		if ($(this).val()=='') {
            $("#find-result").empty();
        } else {
            xhr = $.ajax({
			url: '/find_user',
			type:'POST',
			data:{"username":username},
			success:function(response){
			  $('#find-result').html(response);
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
  	});
  	
  	$(document).on('click', '.find_user_list', function(){
  		var followee = $(this).data('userId')
  		$.ajax({
			url: '/following',
			type:'POST',
			data:{"followee":followee},
			success:function(response){
			  if (response.trim()==''){
				alert("You already follow him(her)");
				}
			  else {
			  $('#followee').append(response);
			  console.log('success')
			}},
			error: function(){
			  console.log('error');
			},
			complete:function(){
			  console.log('complete');
			}
		});
  	});
});